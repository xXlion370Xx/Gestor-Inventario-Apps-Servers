from pathlib import Path
import json
import csv
import logging

class Server:
    def __init__(self, server_id=None, name=None, ip=None, os_type=None, location=None, roles=None):
        self.server_id = server_id
        self.name = name
        self.ip = ip
        self.os_type = os_type
        self.location = location
        self.roles = roles
        
    log_file = Path("logs/inventory.log")
    log_file.parent.mkdir(exist_ok=True)
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Archivos de datos
    applications_file = Path("data/applications.csv")
    data_file = Path("data/servers.json")
    
    data_file.parent.mkdir(exist_ok=True)
    if not data_file.exists():
        data_file.write_text("[]")  
        
    @classmethod
    def get_all_servers(cls):
        if cls.data_file.exists() and cls.data_file.stat().st_size > 0:
            with open(cls.data_file, "r") as f:
                return json.load(f)
        return []

    @classmethod
    def get_server_applications(cls, server_id):
        if not cls.applications_file.exists() or cls.applications_file.stat().st_size == 0:
            return []

        applications = []
        with open(cls.applications_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["server_id"] == server_id:
                    applications.append(row)

        return applications
    
    @classmethod
    def remove_server_applications(cls, server_id):
        """Remove all applications associated with a specific server ID."""
        if not cls.applications_file.exists() or cls.applications_file.stat().st_size == 0:
            return

        applications = []
        removed_apps = []
        with open(cls.applications_file, mode="r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["server_id"] != server_id:
                    applications.append(row)
                else:
                    removed_apps.append(row)

        # Write updated applications back to the CSV file
        with open(cls.applications_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(applications)

        # Log removed applications
        for app in removed_apps:
            logging.info(f"Removed application: {app}")


    @staticmethod
    def save_all_servers(servers):
        """Overwrite the JSON file with updated servers."""
        try:
            with open('data/servers.json', mode='w') as file:
                json.dump(servers, file, indent=4)
        except Exception as e:
            print(f"Error saving servers: {e}")
            
    def __str__(self):
        return (f"ID: {self.server_id}, Name: {self.name}, IP: {self.ip}, "
                f"OS: {self.os_type}, Location: {self.location}, Roles: {', '.join(self.roles)}")

    def to_dict(self):
        return {
            "id": self.server_id,
            "name": self.name,
            "ip": self.ip,
            "os_type": self.os_type,
            "location": self.location,
            "roles": self.roles,
        }
    
    def save_servers(self, servers):
        with open(self.data_file, "w") as f:
            json.dump(servers, f, indent=4)

    def is_unique(self, server_list, ip, name):
        for server in server_list:
            if server["ip"] == ip or server["name"] == name:
                return False
        return True