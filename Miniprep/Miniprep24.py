from opentrons import protocol_api
metadata = {
    'protocolName': 'Vacuum miniprep 24 samples',
    'description': 'Miniprep 24 samples using 3D printed vacuum manifold. Start with resuspended cells in a deep 24 well plate.',
    'author': 'JATD'
    }

requirements = {
    "robotType": "Flex",
    "apiLevel": "2.23",
}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips1 = protocol.load_labware("opentrons_flex_96_tiprack_50ul", location = "A2") 
    tips2 = protocol.load_labware("opentrons_flex_96_tiprack_50ul", location = "C1")
    trash = protocol.load_trash_bin(location="A3")
    left_pipette = protocol.load_instrument(
        "flex_1channel_50",
        mount="left",
        tip_racks=[tips1,tips2]
    )

    # define reagents and labware 
    cells = protocol.load_labware("nest_24_wellplate_10.4ml", "B2")
    VacManifold = protocol.load_labware('jdvacuum_24_tuberack_500ul', 'B3')
    buffers = protocol.load_labware('jd_6_falconrack_50ml', 'C2')
    elution_tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 'C3')

    ### 1. Lyse cells by adding 250ul Lysis buffer to resuspended cells ### 
    # this block adds lysis buffer to each well at the top
    left_pipette.pick_up_tip()
    for i in range(24):  
        left_pipette.transfer(
            250,
            buffers["A1"], 
            cells.wells()[i].top(0),
            new_tip="never",
        )
    left_pipette.drop_tip()
    # this block mixes each well after adding lysis buffer getting  new tip each time
    for i in range(24):
        left_pipette.pick_up_tip()
        left_pipette.mix(3,45, cells.wells()[i])
        left_pipette.drop_tip()

    protocol.comment("Neutralising samples")

    ### 2. Neutralize by adding 350ul Neutralisation buffer ###
    for i in range(24):
        left_pipette.pick_up_tip()
        left_pipette.transfer(
            350,
            buffers["A3"], 
            cells.wells()[i].top(0),
            new_tip="never"
        )
        left_pipette.mix(3,45, cells.wells()[i])
        left_pipette.drop_tip()

    ### Pause for user to spin down samples and load into vacuum manifold ###
    protocol.pause("Please spin down samples and load into vacuum manifold. Click Resume when ready.")

    ### 3. Bind DNA to the column ###
    left_pipette.pick_up_tip()
    for i in range(24):
        left_pipette.transfer(
            500,
            buffers["B1"], 
            cells.wells()[i].top(1),
            new_tip="never",
        )
    for i in range(24):
        left_pipette.transfer(
            500,
            buffers["A3"], 
            cells.wells()[i].top(1),
            new_tip="never",
        )
    left_pipette.drop_tip()
    protocol.pause("Please transfer samples to elution tubes. Click Resume when ready.")

    left_pipette.distribute(
            50,
            buffers["B2"], 
            elution_tubes.wells(),
        )
    # End of protocol
    protocol.comment("Protocol complete, spind down samples and store elutions at -20C")







    