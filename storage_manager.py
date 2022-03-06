import json
import os


class StorageManager:

    faktura_path = ""
    dodavatele_path = ""
    odberatele_path = ""
    descriptions_path = ""

    def __init__(self):

        # Set parameters
        self.json_path = "storage/storage_file.txt"

        # If the file already exists
        if self.path_exists(self.json_path):
            data = self.read_storage_file()

        else:
            # Creating new storage file
            self.create_storage_file()
            data = self.read_storage_file()

        self.set_storage_paths(data)

    def read_storage_file(self):
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            return data

    def create_storage_file(self):
        json_default = {
            "files": {
                "faktura":  os.environ['HOMEPATH']+"\\Desktop\\ucetnictvi.xlsx",
                "dodavatele": "lists/dodavatele.csv",
                "odberatele": "lists/odberatele.csv",
                "descriptions": "lists/descriptions.csv"}
        }

        # Create the new file
        f = open(self.json_path, "x")

        # Write json default file
        self.write_storage_file(json_default)

    def write_storage_file(self, data):
        # Write json default file
        with open(self.json_path, 'w') as json_outfile:
            json.dump(data, json_outfile)

    def set_storage_paths(self, data):
        self.faktura_path = data["files"]["faktura"]
        self.dodavatele_path = data["files"]["dodavatele"]
        self.odberatele_path = data["files"]["odberatele"]
        self.descriptions_path = data["files"]["descriptions"]

    def files_path_validity(self):
        if self.path_exists(self.faktura_path) and self.path_exists(self.dodavatele_path) and self.path_exists(self.odberatele_path) and self.path_exists(self.descriptions_path):
            return True
        else:
            return False

    def path_exists(self, path):
        return os.path.isfile(path)

    def change_file_data(self, key, new_path):
        data = self.read_storage_file()
        data["files"][key] = new_path

        self.write_storage_file(data)
