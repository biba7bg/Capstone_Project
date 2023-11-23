import paramiko
import getpass
import winrm

import main
import menu_options
from printtxtslow import print_slow


# rempte windows function wich is connecting remote windows host
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


# LINUX OS SERVICES FUNCTIONS
def linux_allservices():
    print("I am linux server all services dislay function")
    server_name, username, password = main.get_credentials()

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(
            "systemctl --type=service")
        services = str(stdout.read().decode('utf-8'))
        print(services)
    except paramiko.AuthenticationException:
        print(" Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {str(e)}")
    except Exception as e:
        print(f"Error occured: {str(e)}")
        main.log.error(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
    return main.linux_service_choice()


def linux_last5_reboots():
    print("I am linux server all services dislay function")
    server_name, username, password = main.get_credentials()
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password, look_for_keys=False, allow_agent=False)
        stdin, stdout, stderr = ssh_client.exec_command("uptime && last reboot | head -n 5")
        services = str(stdout.read().decode('utf-8'))
        print(services)
        main.log.error("Unknown command error occured")
    except paramiko.AuthenticationException:
        print(" Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {str(e)}")
    except Exception as e:
        print(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
    return main.linux_service_choice()


def linux_JVM():
    server_name, username, password = main.get_credentials()
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


def linx_resources():
    print_slow(" I am linux resources display, and I am under construction")
    return main.linux_service_choice()


# WINDOWS OS SERVICES FUNCTIONS
def windows_allservices():
    # This is windows functions wich is calling all windows  service
    server_name, username, password = main.get_credentials()
    # Create a WinRM session
    session = windows_session(server_name, username, password)
    # PowerShell command to get all running services
    get_services = 'Get-Service | Format-Table DisplayName, Status -AutoSize'
    # Execute the command on the remote server
    response = session.run_ps(get_services)
    # Check the output and error
    if response.status_code == 0:
        print("\nList of Running Services:\n")
        print(response.std_out.decode())
    else:
        print("Failed to fetch running services.")
        print("Error:", response.std_err.decode())
        main.log.error("Error:", response.std_err.decode())
    return main.windows_service_choice()


def windows_IIS():
    print("I am IIS restart")
    # Get connection details from the user
    # server_name = input("Enter the remote server IP: ").strip()
    server_name, username, password = main.get_credentials()

    # Create a WinRM session
    session = windows_session()  # winrm.Session(

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
        return main.windows_server_menu()


def windows_app_pools():
    print_slow("I am windows app pool service restart, and I am under construction.")
    '''session = windows_session()
    app_pool_services = 'Import-Module WebAdministration; Get-WebAppPool | Select-Onject -ExpandProperty Name'
    output = session.run_ps(
        app_pool_services).std_out.decode().strip().splitlines()
    return output'''
    return main.windows_service_choice()


def windows_service_input():
    print(" I am windows service input display, and I am under construction.")
    return main.windows_service_choice()

