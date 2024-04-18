import csv

class UserAuthentication:
    def __init__(self, credential_file):
        self.credentials = self.read_credentials(credential_file)

    def read_credentials(self, credential_file):
        credentials = []
        with open(credential_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                credentials.append(row)
        return credentials

    def authenticate_user(self, username, password):
        for user in self.credentials:
            if user['username'] == username and user['password'] == password:
                return user['role']
        return None
