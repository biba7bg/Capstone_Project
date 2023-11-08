import sys
import datetime
import os
import paramiko
import getpass
from contextlib import contextmanager

import main
import services_options


curr_date = datetime.datetime.now()
login_wait = 5

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


# WINDOWS SERVER RESTART FUNCTION
def windows_server_reboot(session):
    # functions which intioates windows server restart
    reboot_command = "shutdown /r /t 0"
    result = session.run_cmd(reboot_command)
    return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()

# WINDOWS SERVER SHUTDOWN FUNCTION
def windows_server_shutdown(session):
    # functions which intioates windows server shutdown
    shutdown_command = "shutdown /s /t 0"
    result = session.run_cmd(shutdown_command)
    return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()

# LINUX SERVER MENU FUNCTIONS
def linux_server_interaction():
    print("Linux Server Actions Menu")
    # This linux  server interaction menu 
    print("1. Linux Server Restart\n2. Linux Server Shutdown\n3. Previous Menu\n4. Quit")
    choice = input("Enter desired action: ")
    if choice == "1":
        # This linux  server reboot choice, program creates the ssh connection, sudo elevates the user and send the restart command 
        server_name, username, password = main.get_credentials()
        sudo_password = getpass.getpass("Enter your sudo password: ")
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
            except paramiko.AuthenticationException:
                ssh_client
                print("Bad Password! Connectionclose to {}".format(server_name))
                errorexit(
                    "Bad password, connection Failed! ({})".format(server_name))
            except Exception as e:
                print(f"Error occured: {str(e)}")
                errorexit("Connection Failed {} ({})".format(
                    str(e), server_name))
        stdin, stdout, stderr = ssh_client.exec_command("sudo -i /sbin/reboot", get_pty=True)
        stdin.write(sudo_password + "\n")
        stdin.flush()
        with suppress_stdout():
            print(stdout.read().decode())
        # here I would like to add funtion to catch what happens at the background
        print(" Server is rebooting...")
        return linux_server_interaction()
    elif choice == "2":
        #linux shutdown function 
        linux_shutdown()
    elif choice == "3":
        return main.linux_server_menu()
    elif choice == "4":
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        main.logging.debug("Invalid server menu")
        print("Invalid choice")
    return int(choice)


def linux_shutdown():
    print("I am linux shutdown function")
    server_name, username, password = main.get_credentials()
    sudo_password = getpass.getpass("Enter your sudo password: ")
    confirm = input(
        "Are you sure you want to restart the server? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            # Establish an SSH client session
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)   
        except paramiko.AuthenticationException:
                ssh_client
                print("Bad Password! Connectionclose to {}".format(server_name))
                errorexit(
                    "Bad password, connection Failed! ({})".format(server_name))
        except Exception as e:
                print(f"Error occured: {str(e)}")
                errorexit("Connection Failed {} ({})".format(
                    str(e), server_name))
    # Execute the sudo elevation and shutdown command            
    stdin, stdout, stderr = ssh_client.exec_command("sudo -i /sbin/shutdown -h now", get_pty=True)                  
    stdin.write(sudo_password + "\n")
    stdin.flush()
    with suppress_stdout():
        print(stdout.read().decode())
    # here I would like to add funtion to catch what happens at the background
    print(" Server is shuttingdown...")
     # Close the SSH client session
    ssh_client.close()
    print(f"Sent shutdown command to server {server_name}.")
    return main.linux_server_menu()


# WINDOWS SERVER MENU FUNCTIONS
def windows_server_interaction():
    # This windows server menu function, which displays the server options given to the user
    print("1. Windows Restart\n2. Windows Shutdown\n3. Previus Menu\n4. Quit")
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
            # if the user confirms the reboot, the following command runs, which calls server reboot function
            status_code, stdout, stderr = windows_server_reboot(session)
            # this print is showning execution status if status is 0, that mean the command has been executed successfuly
            print(f"Command executed with status code: {status_code}")
            main.log.error(f"Output: {stdout}")
        if stderr:
            print(f"Error: {stderr}")
            print("write code for windows server reboot")
            return windows_server_reboot()
    elif choice == "2":
        # credentials defined 
        server_name, username, password = main.get_credentials()
        # here the program calls the windows session function, which is locted is services_options.py file
        session = services_options.windows_session(server_name, username, password)
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            # if the user confirms the shutdown, the following command runs, which calls server shutdown function         
            status_code, stdout, stderr = windows_server_shutdown(session)
            print(f"Command executed with status code: {status_code}")
            print(f"Output: {stdout}")
        if stderr:
            print(f"Error: {stderr}")
            print("write code for windows server reboot")
            return windows_server_reboot()
    elif choice == "3":
        # choice 3 takes user to the previous menu
        return main.windows_server_menu()
    elif choice == "4.":
        # choice 4 exits the program
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        main.logging.error("Invalid server menu")
        print("Invalid choice")
    return int(choice)


# Network Meni functions
def bulkip_scan():
    print("I am Bulk IP scanning function and I am under construction")


def nslookup():
    print("I am Bulk IP scanning function and I am under construction")


def subnet_scan():
    print("I am Bulk IP scanning function and I am under construction")
