import json
import uuid
import logging
from pathlib import Path
from classes.server import Server
from classes.application import Application

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
                servers = server.load_servers()

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
                server = Server()
                servers = server.load_servers()
                
                app = Application()
                aplications = app.load_applications()
                
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
                query_server_status()
            elif choice == "4":
                modify_server_or_app()
            elif choice == "5":
                delete_server_or_app()
            elif choice == "6":
                generate_inventory_report()
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
