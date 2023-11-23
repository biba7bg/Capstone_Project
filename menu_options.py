import sys
import os
import getpass
import socket
import subprocess
import ipaddress
import paramiko

from contextlib import contextmanager
from printtxtslow import print_slow

import main
import services_options


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
def lunux_restart():
      # This linux  server reboot choice function, program creates the ssh connection, sudo elevates the user and send the restart command 
        main.log.info("Initiating server reboot process.")
        server_name, username, password = main.get_credentials()
        sudo_password = getpass.getpass("Enter your sudo password: ")
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
                errorexit("Bad password, connection Failed! ({})".format(server_name))
            except Exception as e:
                main.log.info(f"Error occured while connecting to {server_name}: {str(e)}")
                print(f"Error occured: {str(e)}")
                errorexit("Connection Failed {} ({})".format(str(e), server_name))
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
            print(" Server is rebooting...")
            return linux_server_interaction()
        else:
            main.log.info("Server reboot cancelled by user.")
            return linux_server_interaction()

        
# Linux server shutdown function
def linux_shutdown():
    #linux shutdown function
    main.log.info("Initiating server shutdown process.")
    server_name, username, password = main.get_credentials()
    sudo_password = getpass.getpass("Enter your sudo password: ")
    confirm = input(
        "Are you sure you want to shutdown the server? (yes/no): ")
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
def windows_server_reboot(session):
    try:
        # functions which intiates windows server restart
        main.log.info("Initiating server reboot process.")
        #execture reboot
        reboot_command = "shutdown /r /t 0"
        result = session.run_cmd(reboot_command)
        if result.status_code == 0:
            main.log.info("Reboot command executed successfully.")
        else:
            main.log.error(f"Reboot command failed with status code {result.status_code}.") 
        # Return the results          
        return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()
    except Exception as e:
        main.log.error(f"An error occurred during server restart: {e}")
        raise  

# Windows server shutdown function
def windows_server_shutdown(session):
    # functions which intiates windows server shutdown
    try:
        main.log.info("Initiating server shutdown process.")
        #execture shutdown
        shutdown_command = "shutdown /s /t 0"
        result = session.run_cmd(shutdown_command)
        
        if result.status_code == 0:
            main.log.info("Shutdown command executed successfully.")
        else:
            main.log.error(f"Shutdown command failed with status code {result.status_code}.") 
        # Return the results          
        result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()
    except Exception as e:
        main.log.error(f"An error occurred during server shutdown: {e}")
        raise  

# LINUX SERVER MENU FUNCTIONS
def linux_server_interaction():
      # This linux  server interaction menu 
    print("                             ")
    print_slow("Linux Server Actions Menu, please use only numbers (1/2/3/4) for this menu")
    print("*****************************")
    print("1. Linux Server Restart\n2. Linux Server Shutdown\n3. Previous Menu\n4. Quit")
    print("*****************************")
    choice = input("Enter desired action: ")
    if choice == "1":
        #linux reastart function called here
        lunux_restart()
    elif choice == "2":
        #linux shutdown function called here
        linux_shutdown()
    elif choice == "3":
        return main.linux_server_menu()
    elif choice == "4":
        print_slow("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        print("Linux Server Actions Menu")
        exit(0)
    else:
        main.logging.debug("Invalid server menu")
        errorexit("Wrong choice of the menu.")
    return int(choice)


# WINDOWS SERVER MENU FUNCTIONS
def windows_server_interaction():
    # This windows server menu function, which displays the server options given to the user
    print("                             ")
    print_slow("Windows Server Actions Menu, please use only numbers (1/2/3/4) for this menu")
    print("*****************************")
    print("1. Windows Restart\n2. Windows Shutdown\n3. Previus Menu\n4. Quit")
    print("*****************************")
    choice = input("Enter desired action: ")
    if choice == "1":
        # credentials defined 
        server_name, username, password = main.get_credentials()
        # here the program calls the windows session function, which is locted is services_options.py file
        session = services_options.windows_session(server_name, username, password)
        # Make confurmation that user would like to proceed with the choice
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            try:
                # if the user confirms the reboot, the following command runs, which calls server reboot function
                status_code, stdout, stderr = windows_server_reboot(session)
                # this print is showning execution status if status is 0, that mean the command has been executed successfuly
                print(f"Command executed with status code: {status_code}")
                main.log.error(f"Output: {stdout}")
                if stderr:
                    print(f"Error: {stderr}")                
            except Exception as e:
                    print(f"Error occured: {str(e)}")
                    errorexit("Connection Failed {} ({})".format(str(e), server_name))
        return windows_server_interaction()
    elif choice == "2":
        # credentials defined 
        server_name, username, password = main.get_credentials()
        # here the program calls the windows session function, which is locted is services_options.py file
        session = services_options.windows_session(server_name, username, password)
        confirm = input(
            "Are you sure you want to shutdown the server? (yes/no): ")
        if confirm.lower() == "yes":
            try:
                # if the user confirms the shutdown, the following command runs, which calls server shutdown function         
                status_code, stdout, stderr = windows_server_shutdown(session)
                print(f"Command executed with status code: {status_code}")
                main.log.error(f"Output: {stdout}")
                if stderr:
                    print(f"Error: {stderr}")
            except Exception as e:
                    print(f"Error occured: {str(e)}")
                    errorexit("Connection Failed {} ({})".format(str(e), server_name))
        return windows_server_interaction()
    elif choice == "3":
        # choice 3 takes user to the previous menu
        return main.windows_server_menu()
    elif choice == "4.":
        # choice 4 exits the program
        print_slow("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        print("*****************************")
        exit(0)
    else:
        main.logging.error("Invalid server menu option")
        errorexit("Wrong choice of the menu.")
    return int(choice)


# NETWORK MENU FUNCTIONS
def pathping_scan():
    # pathping functionction
    ip_address = input("Please provide the IP Address or hostname: ")
    #defining pathping command 
    pathping_command = ["pathping", ip_address]
    #running the pathping command
    try:
        print("Running pathping, this may take couple of minutes...")
        result = subprocess.run(pathping_command, check=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        main.log.error("Please provde IP address in form of 4 octets(192.xxx.xxx.xxx), and try again.") 
        return f"Please provde IP address in form of 4 octets(192.xxx.xxx.xxx), and try again: {e.stderr}" 


def nslookup(ip_address):
       #this is nslookup function which is called from network menu, option 2
        results = {}
        for ip in ip_address:
            try:
                hostname, alias, addresslist = socket.gethostbyaddr(ip)
                results[ip] = hostname
            except socket.herror:
                results[ip] = "no host found"    
        return results      
        

def port_scan():
    print("I am port scanning function and I am under construction")
    return main.network_menu()
