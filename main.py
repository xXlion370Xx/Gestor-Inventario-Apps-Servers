from rich.console import Console
from rich.table import Table
import uuid
import logging
from pathlib import Path
from classes.server import Server
from classes.application import Application
import csv
import json

# Configurar logging
log_file = Path("logs/inventory.log")
log_file.parent.mkdir(exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def query_server_status():
    print("Option: Query the State of a Server and its Applications selected.")

def modify_server_or_app():
    print("Option: Modify Server or Application Information selected.")

def delete_server_or_app():
    print("Option: Delete a Server or an Application from Inventory selected.")

def generate_inventory_report():
    print("Option: Generate an Inventory Report selected.")

def audit_inventory_changes():
    print("Option: Audit Inventory Changes selected.")

def main_menu():
    while True:
        print("\nInventory Management System")
        print("1. Register a Server in the Inventory")
        print("2. Register an Application in a Server")
        print("3. Query the State of a Server and its Applications")
        print("4. Modify Server or Application Information")
        print("5. Delete a Server or an Application from Inventory")
        print("6. Generate an Inventory Report")
        print("7. Audit Inventory Changes")
        print("0. Exit")
        choice = input("Select an option: ")

        try:
            if choice == "1":
                server = Server()
                servers = Server.get_all_servers()

                # Solicitar datos al usuario
                name = input("Enter server name: ").strip()
                ip = input("Enter server IP (e.g., 192.168.1.1): ").strip()
                os_type = input("Enter server operating system: ").strip()
                location = input("Enter server location: ").strip()
                roles = input("Enter server roles (comma-separated): ").strip().split(",")

                # Validar unicidad
                if not server.is_unique(servers, ip, name):
                    raise ValueError(f"Server with IP '{ip}' or Name '{name}' already exists.")

                # Crear nuevo servidor usando la clase Server
                new_server = Server(
                    server_id=str(uuid.uuid4()),
                    name=name,
                    ip=ip,
                    os_type=os_type,
                    location=location,
                    roles=[role.strip() for role in roles]
                )

                # Guardar servidor y registrar la operación
                servers.append(new_server.to_dict())
                new_server.save_servers(servers)
                logging.info(f"Server registered: {new_server}")

                print("Server registered successfully!")
                
            elif choice == "2":
                servers = Server.get_all_servers()
                
                app = Application()
                aplications = app.get_all_applications()
                
                if not servers:
                    print("No servers available. Please register a server first.")
                    return
                
                print("\nAvailable Servers:")
                for server in servers:
                    print(f"ID: {server['id']}, Name: {server['name']}, IP: {server['ip']}")

                server_id = input("Enter the ID of the server to associate the application: ").strip()
                selected_server = next((server for server in servers if server["id"] == server_id), None)
                if not selected_server:
                    print("Invalid server ID. Operation aborted.")
                    return
                
                
                # Solicitar datos de la aplicación
                name = input("Enter application name: ").strip()
                version = input("Enter application version: ").strip()
                install_date = input("Enter installation date (YYYY-MM-DD): ").strip()
                status = input("Enter application status (e.g., Active, Inactive): ").strip()
                
                new_application = Application(
                    name=name,
                    version=version,
                    install_date=install_date,
                    status=status,
                    server_id=server_id
                )

                if not new_application.is_application_unique(aplications, name, server_id):
                    raise ValueError(f"Application with name '{name}' already exists on server '{selected_server['name']}'.")
                # Guardar la aplicación y registrar la operación
                new_application.save_application(new_application.to_dict())
                
                logging.info(f"Application registered: {new_application}")

                print("Application registered successfully!")
                
            elif choice == "3":
                # Crear una consola para mostrar la salida
                console = Console()

                # Obtener todos los servidores
                servers = Server.get_all_servers()

                if not servers:
                    console.print("[bold red]No servers available to display.[/bold red]")
                else:
                    for server in servers:
                        # Crear la tabla para el servidor actual
                        server_table = Table(title=f"Server: {server['name']} ({server['id']})", show_header=True, header_style="bold magenta")
                        server_table.add_column("Name", justify="left")
                        server_table.add_column("IP", justify="left")
                        server_table.add_column("OS", justify="left")
                        server_table.add_column("Location", justify="left")
                        server_table.add_column("Roles", justify="left")

                        server_table.add_row(
                            server["name"],
                            server["ip"],
                            server["os_type"],
                            server["location"],
                            ", ".join(server["roles"]),
                        )

                        # Mostrar la tabla del servidor
                        console.print(server_table)

                        # Obtener las aplicaciones asociadas al servidor
                        applications = Server().get_server_applications(server["id"])

                        if not applications:
                            console.print("[dim]No applications associated with this server.[/dim]")
                        else:
                            # Crear la tabla para las aplicaciones asociadas
                            app_table = Table(title="Associated Applications", show_header=True, header_style="bold cyan")
                            app_table.add_column("Name", justify="left")
                            app_table.add_column("Version", justify="center")
                            app_table.add_column("Install Date", justify="center")
                            app_table.add_column("Status", justify="center")

                            for app in applications:
                                app_table.add_row(
                                    app["name"],
                                    app["version"],
                                    app["install_date"],
                                    app["status"],
                                )

                            # Mostrar la tabla de aplicaciones asociadas
                            console.print(app_table)
            elif choice == "4":
                console = Console()

                print("\nModify Information")
                print("1. Edit Server")
                print("2. Edit Application")
                sub_choice = input("Select an option: ").strip()

                if sub_choice == "1":
                    servers = Server.get_all_servers()
                    if not servers:
                        print("No servers available to edit.")
                    else:
                        print("[bold magenta]Available Servers:[/bold magenta]")
                        for idx, server in enumerate(servers, 1):
                            print(f"{idx}. {server['name']} (IP: {server['ip']})")

                        try:
                            server_index = int(input("Select the server to edit (by number): ").strip()) - 1
                            if server_index < 0 or server_index >= len(servers):
                                print("Invalid selection.")
                            else:
                                selected_server = servers[server_index]
                                print(f"Selected Server: {selected_server['name']} (IP: {selected_server['ip']})")

                                # Ask user for field to edit
                                print("Fields available to edit: name, ip, os_type, location, roles")
                                field_to_edit = input("Enter the field to edit: ").strip().lower()
                                
                                if field_to_edit not in selected_server:
                                    print("Invalid field.")
                                else:
                                    # Ask user for new value
                                    if field_to_edit == "roles":
                                        new_value = input(f"Enter the new roles as a comma-separated list: ").strip().split(',')
                                        new_value = [role.strip() for role in new_value]
                                    else:
                                        new_value = input(f"Enter the new value for {field_to_edit}: ").strip()

                                    confirm = input(f"Confirm change {field_to_edit} from '{selected_server[field_to_edit]}' to '{new_value}'? (yes/no): ").strip().lower()
                                    
                                    if confirm == "yes":
                                        # Log changes before applying
                                        logging.basicConfig(filename='logs/servers.log', level=logging.INFO, 
                                                            format='%(asctime)s - %(levelname)s - %(message)s')
                                        
                                        old_value = selected_server[field_to_edit]
                                        servers[server_index][field_to_edit] = new_value
                                        
                                        # Save changes back to the JSON file
                                        Server.save_all_servers(servers)
                                        
                                        logging.info(f"Modified server '{selected_server['name']}': {field_to_edit} changed from '{old_value}' to '{new_value}'.")
                                        print(f"{field_to_edit.capitalize()} updated successfully.")
                                    else:
                                        print("Change cancelled.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                elif sub_choice == "2":
                    # List all applications
                    applications = Application.get_all_applications()
                    if not applications:
                        print("No applications available to edit.")
                    else:
                        print("[bold cyan]Available Applications:[/bold cyan]")
                        for idx, app in enumerate(applications, 1):
                            print(f"{idx}. {app['name']} (Version: {app['version']})")
                        
                        try:
                            app_index = int(input("Select the application to edit (by number): ").strip()) - 1
                            if app_index < 0 or app_index >= len(applications):
                                print("Invalid selection.")
                            else:
                                selected_app = applications[app_index]
                                print(f"Selected Application: {selected_app['name']} (Version: {selected_app['version']})")
                                
                                # Ask user for field to edit
                                print("Fields available to edit: name, version, install_date, status, server_id")
                                field_to_edit = input("Enter the field to edit: ").strip().lower()
                                
                                if field_to_edit not in selected_app:
                                    print("Invalid field.")
                                else:
                                    # Ask user for new value
                                    new_value = input(f"Enter the new value for {field_to_edit}: ").strip()
                                    confirm = input(f"Confirm change {field_to_edit} from '{selected_app[field_to_edit]}' to '{new_value}'? (yes/no): ").strip().lower()
                                    
                                    if confirm == "yes":
                                        # Log changes before applying
                                        logging.basicConfig(filename='logs/inventory.log', level=logging.INFO, 
                                                            format='%(asctime)s - %(levelname)s - %(message)s')
                                        
                                        old_value = selected_app[field_to_edit]
                                        applications[app_index][field_to_edit] = new_value
                                        
                                        # Save changes back to the CSV file
                                        Application.save_all_applications(applications)
                                        
                                        logging.info(f"Modified application '{selected_app['name']}': {field_to_edit} changed from '{old_value}' to '{new_value}'.")
                                        print(f"{field_to_edit.capitalize()} updated successfully.")
                                    else:
                                        print("Change cancelled.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")

            elif choice == "5":
                print("\nWhat would you like to do?")
                print("1. Delete a server (and its applications)")
                print("2. Delete a specific application")
                print("3. Exit")
                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    # Delete a server
                    servers = Server.get_all_servers()
                    if not servers:
                        print("No servers available to delete.")
                    else:
                        print("\n[bold magenta]Available Servers:[/bold magenta]")
                        for idx, server in enumerate(servers, 1):
                            print(f"{idx}. {server['name']} (IP: {server['ip']})")

                        try:
                            server_index = int(input("Select the server to delete (by number): ").strip()) - 1
                            if server_index < 0 or server_index >= len(servers):
                                print("Invalid selection.")
                            else:
                                selected_server = servers[server_index]
                                server_id = selected_server["id"]

                                # Confirm deletion
                                confirm = input(f"Are you sure you want to delete server '{selected_server['name']}' and all its applications? (yes/no): ").strip().lower()
                                if confirm == "yes":
                                    # Remove associated applications
                                    Server.remove_server_applications(server_id)

                                    # Remove the server from the list
                                    servers.pop(server_index)

                                    # Save updated server list
                                    Server.save_all_servers(servers)

                                    print(f"Server '{selected_server['name']}' and all its applications have been deleted.")
                                else:
                                    print("Deletion cancelled.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                
                elif choice == "2":
                    applications = []
                    
                    if Server.applications_file.exists() and Server.applications_file.stat().st_size > 0:
                        with open(Server.applications_file, mode="r") as file:
                            reader = csv.DictReader(file)
                            applications = list(reader)

                    if not applications:
                        print("No applications available to delete.")
                    else:
                        print("\nAvailable Applications:")
                        for idx, app in enumerate(applications, 1):
                            print(f"{idx}. {app['name']} (Version: {app['version']}, Server ID: {app['server_id']})")

                        try:
                            app_index = int(input("Select the application to delete (by number): ").strip()) - 1
                            if app_index < 0 or app_index >= len(applications):
                                print("Invalid selection.")
                            else:
                                selected_app = applications[app_index]
                                app_name = selected_app["name"]

                                # Confirm deletion
                                confirm = input(f"Are you sure you want to delete application '{app_name}'? (yes/no): ").strip().lower()
                                if confirm == "yes":
                                    Application.remove_application(app_name)
                                else:
                                    print("Deletion cancelled.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                
                elif choice == "3":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            elif choice == "6":
                report_type = input("Enter the report type (csv/json): ").strip().lower()
                report_file = None

                if report_type not in ["csv", "json"]:
                    print("Invalid report type. Please choose 'csv' or 'json'.")
                else:
                    servers = Server.get_all_servers()
                    if not servers:
                        print("No servers available to generate a report.")
                    else:
                        report_data = []

                        # Collect server and application data
                        for server in servers:
                            server_id = server["id"]
                            applications = Server.get_server_applications(server_id)

                            server_info = {
                                "Server Name": server["name"],
                                "IP": server["ip"],
                                "OS Type": server["os_type"],
                                "Location": server["location"],
                                "Applications": [{"name": app["name"], "version": app["version"]} for app in applications]
                            }
                            report_data.append(server_info)

                        # Generate the report
                        report_path = Path("data/")
                        report_path.mkdir(exist_ok=True)

                        if report_type == "csv":
                            report_file = report_path / "server_applications_report.csv"
                            with open(report_file, mode="w", newline="", encoding="utf-8") as file:
                                writer = csv.writer(file)
                                # Write headers
                                writer.writerow(["Server Name", "IP", "OS Type", "Location", "Applications"])
                                # Write data
                                for server_info in report_data:
                                    app_list = "; ".join([f"{app['name']} (v{app['version']})" for app in server_info["Applications"]])
                                    writer.writerow([server_info["Server Name"], server_info["IP"], server_info["OS Type"], server_info["Location"], app_list])
                        elif report_type == "json":
                            report_file = report_path / "server_applications_report.json"
                            with open(report_file, mode="w", encoding="utf-8") as file:
                                json.dump(report_data, file, indent=4)

                        print(f"Report successfully generated and saved at: {report_file}")
                        
            elif choice == "7":
                audit_inventory_changes()
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main_menu()
