from opentrons import protocol_api
metadata = {
    'protocolName': 'Vacuum miniprep 24 samples',
    'description': 'Miniprep 24 samples using 3D printed vacuum manifold. Start with spun down cells in 2ml tubes.',
    'author': 'JATD'
    }

requirements = {
    "robotType": "Flex",
    "apiLevel": "2.23",
}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips1 = protocol.load_labware("opentrons_flex_96_tiprack_50ul", location = "A2") 
    tips2 = protocol.load_labware("opentrons_flex_96_tiprack_50ul", location = "B1")
    trash = protocol.load_trash_bin(location="A3")
    left_pipette = protocol.load_instrument(
        "flex_1channel_50",
        mount="left",
        tip_racks=[tips1, tips2]
    )

    # define reagents and labware 
    cells = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_screwcap", "B2")
    VacManifold = protocol.load_labware('jdvacuum_24_tuberack_500ul', 'B3')
    buffers = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 'C2')
    elution_tubes = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_screwcap', 'C3')

    ### 1. Lyse cells by resuspending in 250ul Lysis buffer ### 
    for i in range(24):
        left_pipette.transfer(
            250,
            buffers["A1"], 
            cells.wells()[i],
            new_tip="once",
            mix_after=(5, 45)
        )
    

    ### 2. Neutralize by adding 350ul Neutralisation buffer ###
    for i in range(24):
        left_pipette.transfer(
            350,
            buffers["A2"], 
            cells.wells()[i],
            new_tip="once",
            mix_after=(5, 45)
        )

    ### Pause for user to spin down samples and load into vacuum manifold ###
    protocol.pause("Please spin down samples and load into vacuum manifold. Click Resume when ready.")

    ### 3. Bind DNA to the column ###
    left_pipette.pick_up_tip()
    for i in range(24):
        left_pipette.transfer(
            500,
            buffers["A3"], 
            cells.wells()[i].top(3),
            new_tip="never",
        )
    for i in range(24):
        left_pipette.transfer(
            500,
            buffers["A3"], 
            cells.wells()[i].top(3),
            new_tip="never",
        )
    left_pipette.drop_tip()
    protocol.pause("Please transfer samples to elution tubes. Click Resume when ready.")

    left_pipette.distribute(
            50,
            buffers["B1"], 
            VacManifold.wells(),
        )
    # End of protocol
    protocol.comment("Protocol complete")







    