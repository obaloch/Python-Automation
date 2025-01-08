from netmiko import ConnectHandler

# Define router connection details
router1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.162.138',  # Replace with Router1's IP address
    'username': 'admin',  # Replace with the username
    'password': 'cisco',  # Replace with the password
    'secret': 'cisco',
}

router2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.162.137',  # Replace with Router2's IP address
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco'
}

# OSPF configuration commands for Router1
ospf_config_router1 = [
    'router ospf 1',
    'network 0.0.0.0 0.0.0.0 area 0',  # Replace with the correct network
    #'network 192.168.1.0 0.0.0.255 area 0',   # Replace with the correct network
]

# OSPF configuration commands for Router2
ospf_config_router2 = [
    'router ospf 1',
    'network 0.0.0.0 0.0.0.0 area 0',  # Replace with the correct network
    #'network 192.168.2.0 0.0.0.255 area 0',   # Replace with the correct network
]

def configure_router(router, config_commands):
    try:
        print(f"Connecting to {router['ip']}...")
        connection = ConnectHandler(**router)
        print(f"Successfully connected to {router['ip']}.")

        #connection.send_command("enable")

        # Enter privileged EXEC mode
        connection.enable()
        print("Entered privileged EXEC mode.")
        
        print("Sending configuration commands...")
        connection.send_config_set(config_commands)
        
        print("Configuration applied. Verifying OSPF configuration...")


        output = connection.send_command("show ip ospf neighbor")
        print(output)

        connection.disconnect()
        print(f"Disconnected from {router['ip']}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Configure Router1 and Router2
configure_router(router1, ospf_config_router1)
configure_router(router2, ospf_config_router2)