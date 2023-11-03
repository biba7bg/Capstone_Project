import paramiko
import winrm

import main


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
    server_name = input("Enter server name: ")
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
    finally:
        ssh_client.close()
    return main.linux_service_choice()


def linux_last5_reboots():
    print("I am linux server all services dislay function")
    # server_name = "192.168.1.126"
    server_name, username, password = main.get_credentials()

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(
            "uptime && last reboot | head -n 5")
        services = str(stdout.read().decode('utf-8'))
        print(services)
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
    # This is JVM restart function and is called form the choice 3 under  Linux services functions in the main.py file
    print("I am JVM restart finction and I am under construction")


def linx_resources():
    print(" I am linux resources display")


# WINDOWS OS SERVICES FUNCTIONS


def windows_allservices():
    # This is windows functions wich is calling all windows  service

    # Get connection details from the user
    # server_name = input("Enter the remote server IP: ").strip()
    server_name, username, password = main.get_credentials()

    # Create a WinRM session
    session = create_session(server_name, username, password)

    # PowerShell command to get all running services
    # get_running_services_cmd = 'Get-Service | Where-Object { $_.Status -eq "Running" } | Format-Table DisplayName, Status -AutoSize'
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
        return main.windows_server_menu()


def windows_IIS():

    print("I am IIS restart")
    # Get connection details from the user
    # server_name = input("Enter the remote server IP: ").strip()
    server_name, username, password = main.get_credentials()

    # Create a WinRM session
    session = create_session()  # winrm.Session(
    # f"http://{server_name}:5985/wsman", auth=(username, password), transport='ntlm')

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
    session = create_session()
    app_pool_services = 'Import-Module WebAdministration; Get-WebAppPool | Select-Onject -ExpandProperty Name'
    output = session.run_ps(
        app_pool_services).std_out.decode().strip().splitlines()
    return output


def windows_service_input():
    print(" I am windows service input display")
