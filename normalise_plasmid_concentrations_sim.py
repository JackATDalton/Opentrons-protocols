from opentrons import protocol_api
import csv
metadata = {
    "protocolName": "Plasmid concentration Normalisation",
    "description": "A protocol to normalise plasmid concentrations in a 96 well plate using Opentrons Flex",
    "author": "JATD"
}

requirements = {
    "robotType": "Flex", # Ensure the robot type is Flex,
    "apiLevel": "2.16",
    }

def simulate_buffer_usage(csv_path, initial_volume, target_concentration):
    concentrations = {}
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            well = row["well"]
            conc = float(row["conc"])
            concentrations[well] = conc

    total_buffer_used = 0.0
    for well_name, c1 in concentrations.items():
        if c1 <= target_concentration:
            continue
        v2 = (c1 * initial_volume) / target_concentration
        buffer_volume = v2 - initial_volume
        total_buffer_used += buffer_volume

    print(f"[SIMULATION] Total buffer required: {round(total_buffer_used, 2)} µL")
buffer_used_tracker = {"total": 0.0}

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
        "flex_1channel_50ul",
        mount="left",
        tip_racks=[tips]
    )

    initial_volume = 49  # µL
    target_concentration = 20  # ng/µL
    buffer_volume = 1000  # µL
    buffer_tube = tubes.wells()[0]

    for well_name, c1 in concentrations.items():
        if c1 <= target_concentration:
            continue  # skip wells that don't need dilution

        v2 = (c1 * initial_volume) / target_concentration
        buffer_volume = v2 - initial_volume
        buffer_used_tracker["total"] += buffer_volume

        if buffer_volume > 0:
            dest_well = plate1.wells_by_name()[well_name]
            left_pipette.pick_up_tip()
            left_pipette.transfer(buffer_volume, buffer_tube, dest_well, new_tip='never')
            left_pipette.drop_tip()

    protocol.comment(f"Total buffer used: {round(buffer_used_tracker['total'], 2)} µL")

if __name__ == "__main__":
    simulate_buffer_usage("PlateLayout362025.csv", initial_volume=49, target_concentration=20)