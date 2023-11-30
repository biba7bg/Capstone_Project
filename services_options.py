import paramiko
import getpass
import winrm

import main
import menu_options
import printtxtslow


# remopte windows function which is connecting remote windows host
def windows_session(server_name, username, password, port=5985, server_cert_validation='ignore'):
    # this functions is for creating remote connection to windows server
    session_url = f"http://{server_name}:{port}/wsman"
    session = winrm.Session(
        session_url,
        auth=(username, password),
        transport='ntlm',
        server_cert_validation=server_cert_validation
    )
    return session


# LINUX SERVICES FUNCTIONS
def linux_allservices():
    # lists all services function 
    main.log.info("Starting linux server all services display function")
    print("I am linux server all services dislay function")
    # collecting server name and login info
    server_name = input("Enter Server Name: ") 
    username, password = main.get_credentials()
    try:
        #created the session
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        main.log.info(f"Attempting to connect to server: {server_name}")
        ssh_client.connect(server_name, username=username, password=password)
        main.log.info("SSH connection established successfully")
        #sends the command
        stdin, stdout, stderr = ssh_client.exec_command(
            "systemctl --type=service")
        services = str(stdout.read().decode('utf-8'))
        print(services)
        main.log.info("Successfully retrieved services list")
    except paramiko.AuthenticationException:
        #exception errors collection
        error_message = "Authentication failed, please verify your credentials."
        print(error_message)
        main.log.error(error_message)
    except paramiko.SSHException as e:
        error_message = f"Unable to establish SSH connection: {str(e)}"
        print(error_message)
        main.log.error(error_message)
    except Exception as e:
        print(f"Error occured: {str(e)}")
        main.log.error(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
        main.log.info("SSH connection closed")
    return main.linux_service_choice()


def linux_last5_reboots():
    # lists 5 last reboots function 
    main.log.info("Starting linux last 5 reboots  display function")
    server_name = input("Enter Server Name: ")
    username, password = main.get_credentials()
    try:
        #created the session
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
        main.log.info("SSH connection established successfully")
        #sends the command
        stdin, stdout, stderr = ssh_client.exec_command("uptime && last reboot | head -n 5")
        services = str(stdout.read().decode('utf-8'))
        print(services)
        main.log.info("Successfully retrieved services list")
        #exception errors collection
    except paramiko.AuthenticationException:
        error_message = "Authentication failed, please verify your credentials."
        print(error_message)
        main.log.error(error_message)
    except paramiko.SSHException as e:
        error_message = f"Unable to establish SSH connection: {str(e)}"
        print(error_message)
        main.log.error(error_message)
    except Exception as e:
        print(f"Error occured: {str(e)}")
        main.log.error(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
        main.log.info("SSH connection closed")
    return main.linux_service_choice()


def linux_JVM():
    server_name = input("Enter Server Name: ") 
    username, password = main.get_credentials()
    sudo_password = getpass.getpass("Enter your sudo password: ")
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
        # ask user to put the JVM name
        jvm_name = input("Enter the JVM name: ")
        stdin, stdout, stderr = ssh_client.exec_command(f"ps -ef | grep {jvm_name}")
        jvm_info = stdout.read().decode().strip().split()
        if jvm_info:
            jvm_pid = jvm_info[0]
            print(f"JVM Name: {jvm_name}")
            print(f"JVM PID: {jvm_pid}")
            print(f"JVM Status: Running")
        else:
            print(f"No JVM found with this name: {jvm_name}") 
            menu_options.errorexit(f"No JVM found with this name: {jvm_name}")
            #return main.linux_service_choice()
        ask_user_action = input("Choose an JVM action (restart/stop/start): ").lower()
        if ask_user_action == "restart":
            stdin, stdout, stderr = ssh_client.exec_command(f" sudo -i /usr/local/bin .\jvmRestart {jvm_name}", get_pty=True)
            stdin.write(sudo_password + "\n")
            stdin.flush()
            print(stdout.read().decode())
            print(stderr.read().decode())
        elif ask_user_action == "stop":
            stdin, stdout, stderr = ssh_client.exec_command(f" sudo -i /usr/local/bin .\jvmRestart {jvm_name} stop", get_pty=True)
            stdin.write(sudo_password + "\n")
            stdin.flush()
            print(stdout.read().decode())
            print(stderr.read().decode())
        elif ask_user_action == "start":
                stdin, stdout, stderr = ssh_client.exec_command(f" sudo -i /usr/local/bin .\jvmRestart {jvm_name} start", get_pty=True)
                stdin.write(sudo_password + "\n")
                stdin.flush()
                print(stdout.read().decode())
                print(stderr.read().decode())
        else:
            print("Invalid coice of restart/stop/start options")
            
        # Display JVM's new pid and status
        stdin, stdout, stderr = ssh_client.exec_command(f"ps  -ef | grep {jvm_name}")
        new_jvm_info = stdout.read().decode().strip().strip()

        if new_jvm_info:
            new_jvm_info = new_jvm_info[0]
            print(f"New JVM PID: {new_jvm_info}")
            print(f"Updated JVM Starus: Running")
        else:
            print(f"No JVM with this name found: {jvm_name}")
    except  paramiko.AuthenticationException:
        print("Bad Password! Connectionclose to {}".format(server_name))
        menu_options.errorexit("Bad password, connection Failed! ({})".format(server_name))
    except Exception as e:
                print(f"Error occured: {str(e)}")
                menu_options.errorexit("Connection Failed {} ({})".format(str(e), server_name))
    finally:
        ssh_client.close()
    return main.linux_service_choice()


def linux_resources():
    # lists 5 last reboots function 
    main.log.info("Starting linux list all resources function")
    server_name = input("Enter Server Name: ")
    username, password = main.get_credentials()
    try:
        #created the session
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
        main.log.info("SSH connection established successfully")
        # Commands to list resources 
        commands = ["cat /proc/cpuinfo", "free -m", "df -h", "top -b -n 1"]
        for command in commands:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            print(f"Output of '{command}':")
            print(stdout.read().decode())
            print(stderr.read().decode())
        main.log.info("Successfully retrieved services list")
        printtxtslow.print_slow("This is the end of the list")
        printtxtslow.separate()
        #exception errors collection
    except paramiko.AuthenticationException:
        error_message = "Authentication failed, please verify your credentials."
        print(error_message)
        main.log.error(error_message)
    except paramiko.SSHException as e:
        error_message = f"Unable to establish SSH connection: {str(e)}"
        print(error_message)
        main.log.error(error_message)
    except Exception as e:
        print(f"Error occured: {str(e)}")
        main.log.error(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
        main.log.info("SSH connection closed")
    return main.linux_service_choice()



# WINDOWS SERVICES FUNCTIONS
def windows_allservices():
    # This is windows functions wich is calling all windows  service
    main.log.info("Starting windows all services display")
    server_name = input("Enter Server Name: ") 
    username, password = main.get_credentials()
    main.log.info(f"Credentials for server: {server_name}")
    # Create a WinRM session
    main.log.info("Creating winrm session")
    session = windows_session(server_name, username, password)
    # PowerShell command to get all running services
    get_services = 'Get-Service | Format-Table DisplayName, Status -AutoSize'
    # Execute the command on the remote server
    main.log.info("Executing command to display services")
    response = session.run_ps(get_services)
    print("This is the end of the list ")
    printtxtslow.separate()
    # Check the output and error
    if response.status_code == 0:
        main.log.info("Successfully display running services")
        print("\nList of Running Services:\n")
        print(response.std_out.decode())
    else:
        error_message = "Failed to fetch running services. Error: " + response.std_err.decode()
        print(error_message)
        main.log.error(error_message)
    input("Press enter to continue...")    
    return main.windows_service_choice()


def windows_IIS():
    print("I am IIS restart")
    # Get connection details from the user
    # server_name = input("Enter the remote server IP: ").strip()
    server_name = input("Enter Server Name: ")
    username, password = main.get_credentials()

    # Create a WinRM session
    session = windows_session(server_name, username, password)  # winrm.Session(

    # PowerShell command to restart IIS
    restart_iis = 'iisreset /restart'
    # this is to be tested for improved IIS restart aproach 'iisreset /stop /timeout:60 |taskkill /F /FI "SERVICES eq was" | iisreset /start'

    # Execute the command on the remote server
    response = session.run_ps(restart_iis)

    # Check the output and error
    if response.status_code == 0:
        print("IIS restarted successfully.")
        print("Output:", response.std_out.decode())
    else:
        print("Failed to restart IIS.")
        print("Error:", response.std_err.decode())
    return main.windows_service_choice()


def windows_app_pools():
    # This is windows functions which restarts app pool services
    main.log.info("Starting windows all services display")
    server_name = input("Enter Server Name: ") 
    username, password = main.get_credentials()
    main.log.info(f"Credentials for server: {server_name}")
    # Create a WinRM session
    main.log.info("Creating winrm session")
    try:
        session = windows_session(server_name, username, password)
        # PowerShell command to get all running services
        ps_script = "Import-Module WebAdministration; Get-WebAppPoolState"
        response = session.run_ps(ps_script)
        # Execute the command on the remote server
        main.log.info("Executing command to display services")
        if response.status_code == 0:
            print("List of Application Pools:\n")
            print(response.std_out.decode())
        else:
            print("Failed to list application pools.")
            print("Error:", response.std_err.decode())
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")
    input("Press enter to continue...")    
    return main.windows_service_choice()


def windows_service_input():
    # This is windows functions allows user to restart service on demand
    main.log.info("Starting windows all services display")
    server_name = input("Enter Server Name: ") 
    username, password = main.get_credentials()
    service_name = input("Enter the service name: ")
    main.log.info(f"Credentials for server: {server_name}")
    # Create a WinRM session
    main.log.info("Creating winrm session")
    try:
        session = windows_session(server_name, username, password)
        # Check current service status
        ps_script = f"Get-Service -Name {service_name} | Select-Object -Property Status"
        response = session.run_ps(ps_script)
        if response.status_code == 0:
            print(f"Current status of {service_name}: {response.std_out.decode().strip()}")
        else:
            print("Failed to get service status.")
            print("Error:", response.std_err.decode())
            return

        # Ask user for action
        action = input(f"What action would you like to perform on {service_name} (start/stop/restart): ").lower()

        # Perform the action
        if action in ["start", "stop", "restart"]:
            ps_script = f"{action.capitalize()}-Service -Name {service_name}"
            response = session.run_ps(ps_script)
            if response.status_code == 0:
                print(f"Service {service_name} {action}ed successfully.")
            else:
                print(f"Failed to {action} service {service_name}.")
                print("Error:", response.std_err.decode())
        else:
            print("Invalid action.")
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")
    input("Press enter to continue...")    
    return main.windows_service_choice()

    


    return main.windows_service_choice()

