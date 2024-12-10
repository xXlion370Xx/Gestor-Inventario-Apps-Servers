import csv
from pathlib import Path
from classes.server import Server
import logging

class Application:
    def __init__(self, name=None, version=None, install_date=None, status=None, server_id=None):
        self.name = name
        self.version = version
        self.install_date = install_date
        self.status = status
        self.server_id = server_id

    applications_file = Path("data/applications.csv")
    applications_file.parent.mkdir(exist_ok=True)
    if not applications_file.exists():
        with open(applications_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "version", "install_date", "status", "server_id"])  # Encabezados

    def __str__(self):
        return (f"Name: {self.name}, Version: {self.version}, "
                f"Install Date: {self.install_date}, Status: {self.status}")

    def update_version(self, new_version):
        self.version = new_version

    def update_status(self, new_status):
        self.status = new_status
        
    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "install_date": self.install_date,
            "status": self.status,
            "server_id": self.server_id
        }
        
    def is_application_unique(self, applications, name, server_id):
        for app in applications:
            if app["name"] == name and app["server_id"] == server_id:
                return False
        return True

    def load_applications(self):
        if self.applications_file.exists() and self.applications_file.stat().st_size > 0:
            with open(self.applications_file, mode='r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        return []

    def save_application(self, application):
        with open(self.applications_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([application["name"], application["version"],
                            application["install_date"], application["status"], application["server_id"]])
