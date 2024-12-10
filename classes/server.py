from pathlib import Path
import json
import csv


class Server:
    def __init__(self, server_id=None, name=None, ip=None, os_type=None, location=None, roles=None):
        self.server_id = server_id
        self.name = name
        self.ip = ip
        self.os_type = os_type
        self.location = location
        self.roles = roles

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
                servers = json.load(f)
                return servers
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
    
    def load_servers(self):
        if self.data_file.exists() and self.data_file.stat().st_size > 0:
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []
    
    def save_servers(self, servers):
        with open(self.data_file, "w") as f:
            json.dump(servers, f, indent=4)

    def is_unique(self, server_list, ip, name):
        for server in server_list:
            if server["ip"] == ip or server["name"] == name:
                return False
        return True