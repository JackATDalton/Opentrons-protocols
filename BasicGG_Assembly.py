from opentrons import protocol_api
metadata = {
    'protocolName': 'G block assembly',
    'description': 'Assembly og Gblocks into destination vector in opentrons thermocycler. Preparation of assemblies should occur by hand outside the robot',
    'author': 'JATD'
    }

requirements = {
    "robotType": "Flex",
    "apiLevel": "2.23",
}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware("opentrons_flex_96_tiprack_50ul", location = "C2") 
    trash = protocol.load_trash_bin(location="A3")
    # Load the thermocycler module
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    plate = tc_mod.load_labware(name="opentrons_96_wellplate_200ul_pcr_full_skirt")
    left_pipette = protocol.load_instrument(
        "flex_1channel_50",
        mount="left",
        tip_racks=[tips]
    )
    
    # Golden Gate cycling protocol
    tc_mod.close_lid()
    #heat lid to prevent condensation
    tc_mod.set_lid_temperature(105) 

    cycles = 90  # adjust as needed
    cut_temp = 37  # Change to 42 if your enzyme requires it
    lig_temp = 16  # ligation temperature, change to 20 if your enzyme requires it
    cut_time = 5   # minutes
    lig_time = 5   # minutes


    profile = [
        {"temperature": cut_temp, "hold_time_minutes": cut_time},
        {"temperature": lig_temp, "hold_time_minutes": lig_time}
    ]

    tc_mod.execute_profile(steps=profile, repetitions=cycles, block_max_volume=10)
    
    # Enzyme inactivation
    tc_mod.set_block_temperature(60, hold_time_minutes=10)
    # Hold at 12°C until retrieval
    tc_mod.set_block_temperature(12)
    tc_mod.deactivate_lid()
