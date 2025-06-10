from opentrons import protocol_api
metadata = {
    "protocolName": "Plasmid concentration Normalisation",
    "description": "A protocol to normalise plasmid concentrations in a 96 well plate using Opentrons Flex, should only use one tip. Requires a list of plasmid concentrations and locations. Run the associated notebook first to make the list and calculate the amount of buffer you need and to set the intial volumes low enough to prevent overflow in the 96 well plate",
    "author": "JATD"
}

requirements = {
    "robotType": "Flex", # Ensure the robot type is Flex,
    "apiLevel": "2.23",
    }


def run(protocol: protocol_api.ProtocolContext):
    concentrations = {'A1': 63.45, 'A2': 59.1, 'A3': 46.8, 'A4': 69.0, 'A5': 30.0, 'A6': 28.7, 'A7': 61.0, 'A8': 84.4, 'A9': 32.0, 'A10': 35.0, 'A11': 69.0, 'A12': 32.0, 'B1': 33.0, 'B2': 108.0, 'B3': 65.0, 'B4': 34.0, 'B5': 29.0, 'B6': 66.0, 'B7': 43.0, 'B8': 44.0, 'B9': 50.5, 'B10': 44.0, 'B11': 70.0, 'B12': 64.0, 'C1': 41.0, 'C2': 26.0, 'C3': 20.0, 'C4': 73.0, 'C5': 22.0, 'C6': 78.0, 'C7': 25.0, 'C8': 12.5, 'C9': 53.0, 'C10': 50.95, 'C11': 35.0, 'C12': 60.0, 'D1': 24.0, 'D2': 50.0, 'D3': 132.0, 'D4': 17.0, 'D5': 62.0, 'D6': 19.0, 'D7': 23.0, 'D8': 65.0, 'D9': 62.0, 'D10': 48.0, 'D11': 49.0, 'D12': 39.0, 'E1': 54.0, 'E2': 29.95, 'E3': 55.0, 'E4': 32.0, 'E5': 39.0, 'E6': 45.0, 'E7': 75.0, 'E8': 54.0, 'E9': 15.0, 'E10': 14.0, 'E11': 44.0, 'E12': 19.0, 'F1': 36.0, 'F2': 38.0, 'F3': 160.0, 'F4': 33.0}

    tips = protocol.load_labware("opentrons_flex_96_tiprack_50ul", "C2")
    tubes = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", "D2")
    trash = protocol.load_trash_bin("A3")
    
    temp_module = protocol.load_module("temperature module gen2", "D1")
    plate1 = temp_module.load_labware("corning_96_wellplate_360ul_flat")
    #temp_module.set_temperature(24)

    left_pipette = protocol.load_instrument(
        "flex_1channel_50",
        mount="left",
        tip_racks=[tips]
    )

    initial_volume = 25  # µL
    target_concentration = 20  # ng/µL
    buffer_volume_per_tube = 1000  # µL per tube initially
    tube_index = 0
    buffer_tube = tubes.wells()[tube_index]
    buffer_left_in_tube = buffer_volume_per_tube
    left_pipette.pick_up_tip()

    for well_name, c1 in concentrations.items():
        if c1 <= target_concentration:
            continue

        v2 = (c1 * initial_volume) / target_concentration
        buffer_volume = v2 - initial_volume

        if buffer_volume > 0:
            # Check if buffer left is enough, else switch tube
            if buffer_volume > buffer_left_in_tube or buffer_left_in_tube < 50:
                tube_index += 1
                if tube_index >= len(tubes.wells()):
                    raise RuntimeError("Not enough buffer in tubes to complete the protocol!")
                buffer_tube = tubes.wells()[tube_index]
                buffer_left_in_tube = buffer_volume_per_tube

            #left_pipette.pick_up_tip()
            left_pipette.transfer(buffer_volume, 
                                  buffer_tube, 
                                  plate1.wells_by_name()[well_name].top(-1),
                                    new_tip='never')
            #left_pipette.drop_tip()

            buffer_left_in_tube -= buffer_volume

