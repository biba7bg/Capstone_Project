import socket
import sys
import os
import getpass
import scapy
import subprocess
from contextlib import contextmanager
import paramiko



import main
import services_options
from printtxtslow import print_slow
from printtxtslow import separate




# this function is suppresing the print out to the screen, this way when sudo password is entered, it doesn't show on the screen
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# error logging function
def errorexit(str):
    main.log.error(str)
    print("ERROR: {}".format(str))
    print("Exiting...")
    main.logging.shutdown()
    os._exit(1)

# Linux server restart function
def linux_restart(server_name, username, password):
      # This linux  server reboot choice function, program creates the ssh connection, sudo elevates the user and send the restart command 
        #main.log.info("Initiating server reboot process.")
        sudo_password = getpass.getpass("Enter your sudo password: ")
        print(f" Restarting server: {server_name}")
        main.log.info(f"Restarting server: {server_name}")
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
                main.log.info(f"Successfully connected to {server_name} as {username}.")
            except paramiko.AuthenticationException:
                ssh_client
                main.log.info(f"Successfully connected to {server_name} as {username}.")
                print("Bad Password! Connectionclose to {}".format(server_name))
                #errorexit("Bad password, connection Failed! ({})".format(server_name))
            except Exception as e:
                main.log.info(f"Error occured while connecting to {server_name}: {str(e)}")
                print(f"Error occured: {str(e)}")
                #errorexit("Connection Failed {} ({})".format(str(e), server_name))
            try:    
                stdin, stdout, stderr = ssh_client.exec_command("sudo -i /sbin/reboot", get_pty=True)
                stdin.write(sudo_password + "\n")
                stdin.flush()
                with suppress_stdout():
                    print(stdout.read().decode())
                main.log.info("Reboot command executed successfully.")
            except Exception as e:    
                main.log.info((f"Error occurred while executing reboot command: {str(e)}"))
                print(f"Error occurred: {str(e)}")
                # Close the SSH client session
                ssh_client.close()
                print("Server is rebooting...")
                return linux_server_interaction()
        else:
            main.log.info("Server reboot cancelled by user.")
            return linux_server_interaction()
       
# Linux server shutdown function
def linux_shutdown(server_name, username, password):
        #linux shutdown function
        main.log.info("Initiating server shutdown process.")
        sudo_password = getpass.getpass("Enter your sudo password: ")
        print(f"Shutting down server: {server_name}")
        confirm = input("Are you sure you want to shutdown the server? (yes/no): ")
        if confirm.lower() == 'yes':
            try:
                # Establish an SSH client session
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
                main.log.info(f"Successfully connected to {server_name} as {username}.")   
            except paramiko.AuthenticationException:
                ssh_client
                main.log.info(f"Successfully connected to {server_name} as {username}.")
                print("Bad Password! Connectionclose to {}".format(server_name))
                errorexit(
                    "Bad password, connection Failed! ({})".format(server_name))
            except Exception as e:
                main.log.info(f"Error occured while connecting to {server_name}: {str(e)}")
                print(f"Error occured: {str(e)}")
                errorexit("Connection Failed {} ({})".format(str(e), server_name))
            try:        
                # Execute the sudo elevation and shutdown command            
                stdin, stdout, stderr = ssh_client.exec_command("sudo -i /sbin/shutdown -h now", get_pty=True)                  
                stdin.write(sudo_password + "\n")
                stdin.flush()
                with suppress_stdout():
                    print(stdout.read().decode())
                main.log.info("Reboot command executed successfully.")    
            except Exception as e:
                main.log.info((f"Error occurred while executing reboot command: {str(e)}"))
                print(f"Error occurred: {str(e)}")
                # Close the SSH client session
                ssh_client.close()
                print_slow(f"Sent shutdown command to server {server_name}.")
                return main.linux_server_menu()
        else:
            main.log.info("Server shutfown cancelled by user.")
            return linux_server_interaction()

# Windowsserver restart function
def windows_server_reboot(servers):
    username, password = main.get_credentials()
    confirm = input("Are you sure you want to shutdown the server? (yes/no): ")
    if confirm.lower() == "yes":
        try:
            session = services_options.windows_session(servers, username, password)
            main.log.info("Initiating server reboot process.")
            # execture reboot
            reboot_command = "shutdown /r /t 0"
            result = session.run_cmd(reboot_command)
            if result.status_code == 0:
                main.log.info("Reboot command executed successfully.")
            else:
                main.log.error(f"Reboot command failed with status code {result.status_code}.") 
            # Return the results          
            return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()
        except Exception as e:
            print(f"Error connecting to {servers}: {str(e)}")
            main.log.error(f"An error occurred during server restart: {e}")
            return windows_server_interaction()   
  
# Windows server shutdown function
def windows_server_shutdown(servers):
    username, password = main.get_credentials()
    confirm = input("Are you sure you want to shutdown the server? (yes/no): ")
    if confirm.lower() == "yes":
        try:
            #creating session
            session = services_options.windows_session(servers, username, password)
            main.log.info("Initiating server shutdown.")
             #execture reboot
            shutdown_command = "shutdown /s /t 0"
            result = session.run_cmd(shutdown_command)
            if result.status_code == 0:
                main.log.info("Shutdown command executed successfully.")
            else:
                main.log.error(f"Shutdows command failed with status code {result.status_code}.") 
                # Return the results          
                return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()
        except Exception as e:
            print(f"Error connecting to {servers}: {str(e)}")
            main.log.error(f"An error occurred during server restart: {e}")
            return windows_server_interaction()     


# LINUX SERVER MENU FUNCTIONS
def linux_server_interaction():
      # This linux  server interaction menu 
    print("                             ")
    print("Linux Server Actions Menu, use only numbers: ")
    separate()
    print("1. Linux Server Restart\n2. Linux Server Shutdown\n3. Previous Menu\n4. Quit")
    separate()
    choice = input("Enter desired action: ")
    if choice == "1":
        #linux reastart function called here
        server_input = input("Eners server name or IP separeted by comma: ")
        server_input = [s.strip() for s in server_input.replace(",", " ").split()]
        username, password = main.get_credentials()
        for server_name in server_input:
            #linux reastart function called here
            linux_restart(server_name, username, password)
    elif choice == "2":
        #linux shutdown function called here
        server_input = input("Eners server name or IP separeted by comma: ")
        server_input = [s.strip() for s in server_input.replace(",", " ").split()]
        username, password = main.get_credentials()
        for server_name in server_input:
            linux_shutdown(server_name, username, password)
    elif choice == "3":
        return main.linux_server_menu()
    elif choice == "4":
        print_slow("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        main.logging.debug("Invalid server menu")
        print("Use only numbers /1/2/3/4 for this menu.")
        return linux_server_interaction()
    return int(choice)

# WINDOWS SERVER MENU FUNCTIONS
def windows_server_interaction():
    # This windows server menu function, which displays the server options given to the user
    print("                             ")
    print("Windows Server Actions Menu, use only numbers: ")
    separate()
    print("\n1. Windows Restart\n2. Windows Shutdown\n3. Previus Menu\n4. Quit")
    separate()
    choice = input("Enter desired action: ")
    if choice == "1":
        server_input = input("Enter the hostnames of the servers to restart (comma-separated): ").split(',')
        for server in server_input:
            windows_server_reboot(server)
    elif choice == "2":
        server_input = input("Enter the hostnames of the servers to restart (comma-separated): ").split(',')
        for server in server_input:
            windows_server_shutdown(server)
    elif choice == "3":
        # choice 3 takes user to the previous menu
        return main.windows_server_menu()
    elif choice == "4":
        # choice 4 exits the program
        print_slow("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        separate()
        exit(0)
    else:
        main.logging.error("Invalid server menu option")
        print("Use only numbers /1/2/3/4 for this menu.")
        return windows_server_interaction()
    return int(choice)

# NETWORK MENU FUNCTIONS
def pathping_scan():
    # pathping functionction
    ip_address = input("Please provide the IP Address or hostname: ")
    #defining pathping command 
    pathping_command = ["pathping -q 10 -p 100", ip_address]
    #running the pathping command
    try:
        print("Running pathping, this may take couple of minutes...")
        result = subprocess.run(pathping_command, check=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        main.log.error("Please provde IP address in form of 4 octets(192.xxx.xxx.xxx), and try again.") 
        return f"Please provde IP address in form of 4 octets(192.xxx.xxx.xxx), and try again: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}" 

def nslookup(ip_address):
       #this is nslookup function which is called from network menu, option 2
        results = {}
        for ip in ip_address:
            try:
                hostname, alias, addresslist = socket.gethostbyaddr(ip)
                main.log.info(f"successful command for {ip}: {hostname}")
                results[ip] = hostname
            except socket.herror:
                results[ip] = "no host found" 
                main.log.info(f"nslookup result for {ip}: host not found.")   
        return results      
        
def subnet_scan():
    # subnet scan
    input_ips = input("Enter IP addresses separated by comma: ")
    ip_list = input_ips.split(',')
    active_hosts = []
    for ip_address in ip_list:
         # removes white space
        ip_address = ip_address.strip()
        # Build ICMP packet 
        packet = IP(dst=ip_address)/ICMP()
        # Send the packet and wait for a reply
        reply = sr1(packet, timeout=3, verbose=False)
        if reply:
            print(f"Host {ip_address} is UP.")
            active_hosts.append(ip_address)
        else:
            print(f"Host {ip_address} is DOWN.")
    
    print("\nActive hosts:")
    for host in active_hosts:
        print(host)

    
    
    return main.network_menu()
