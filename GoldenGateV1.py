from opentrons import protocol_api
metadata = {
    "protocolName": "Golden Gate Assembly",
    "description": "A protocol for Golden Gate Assembly using Opentrons Flex",
    "author": "JATD"
}

requirements = {
    "robotYpe: "Flex",
    "apiLevel": "2.16",
    }

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_flex_96_tiprack_50ul", "B3")
    tubes = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_screwcap", "D2")
    trash = protocol.load_trash_bin("A3")
    plate1 = protocol.load_labware("corning_96_wellplate_360ul_flat", "D1")

    left_pipette = protocol.load_instrument(
        "flex_1channel_50ul",
        mount="left",
        tip_racks=[tips]
    )

    # Serial Dilution: 1:2 dilution across 5 tubes
    source = tubes.wells()[0]
    dilution_wells = tubes.wells()[1:6]
    diluent_volume = 10
    transfer_volume = 10

    # Add diluent to all dilution tubes
    for well in dilution_wells:
        left_pipette.pick_up_tip()
        left_pipette.transfer(diluent_volume, protocol.fixed_trash['A1'], well, new_tip='never')
        left_pipette.drop_tip()

    # Perform serial dilutions
    left_pipette.pick_up_tip()
    current_source = source
    for dest in dilution_wells:
        left_pipette.transfer(transfer_volume, current_source, dest, mix_after=(3, 20), new_tip='never')
        current_source = dest
    left_pipette.drop_tip()

   
