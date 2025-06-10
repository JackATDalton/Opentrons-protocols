from opentrons import protocol_api
metadata = {
    "protocolName": "Heatblock Setup Test",
    "description": "A simple protocol to test the heatblock setup and prewarm or precool it for experiments.",
    "author": "JATD"
}

requirements = {
    "robotType": "Flex", # Ensure the robot type is Flex,
    "apiLevel": "2.23",
    }


def run(protocol: protocol_api.ProtocolContext):
    temp_module = protocol.load_module("temperature module gen2", "D1")
    temp_module.set_temperature(42)
    