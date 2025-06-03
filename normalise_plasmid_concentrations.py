from opentrons import protocol_api
import csv
metadata = {
    "protocolName": "Plasmid concentration Normalisation",
    "description": "A protocol to normalise plasmid concentrations in a 96 well plate using Opentrons Flex",
    "author": "JATD"
}

requirements = {
    "robotType": "Flex", # Ensure the robot type is Flex,
    "apiLevel": "2.23",
    }


def run(protocol: protocol_api.ProtocolContext):
    concentrations = {}
    with open("PlateLayout362025.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            well = row["well"]
            conc = float(row["conc"])
            concentrations[well] = conc

    tips = protocol.load_labware("opentrons_flex_96_tiprack_50ul", "B3")
    tubes = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_screwcap", "D2")
    trash = protocol.load_trash_bin("A3")
    plate1 = protocol.load_labware("corning_96_wellplate_360ul_flat", "D1")

    left_pipette = protocol.load_instrument(
        "flex_1channel_50",
        mount="left",
        tip_racks=[tips]
    )

    initial_volume = 49  # µL
    target_concentration = 20  # ng/µL
    buffer_volume_per_tube = 1000  # µL per tube initially
    tube_index = 0
    buffer_tube = tubes.wells()[tube_index]
    buffer_left_in_tube = buffer_volume_per_tube

    for well_name, c1 in concentrations.items():
        if c1 <= target_concentration:
            continue

        v2 = (c1 * initial_volume) / target_concentration
        buffer_volume = v2 - initial_volume

        if buffer_volume > 0:
            # Check if buffer left is enough, else switch tube
            if buffer_volume > buffer_left_in_tube or buffer_left_in_tube < 10:
                tube_index += 1
                if tube_index >= len(tubes.wells()):
                    raise RuntimeError("Not enough buffer in tubes to complete the protocol!")
                buffer_tube = tubes.wells()[tube_index]
                buffer_left_in_tube = buffer_volume_per_tube

            left_pipette.pick_up_tip()
            left_pipette.transfer(buffer_volume, buffer_tube, plate1.wells_by_name()[well_name], new_tip='never')
            left_pipette.drop_tip()

            buffer_left_in_tube -= buffer_volume

