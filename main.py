import os
from user_authentication import UserAuthentication
from patient_record_manager import PatientRecordManager
from datetime import datetime

def get_valid_file_path(prompt):
    while True:
        file_path = input(prompt)
        if os.path.exists(file_path):
            return file_path
        else:
            print("File not found. Please check the file path and try again.")

def main():
    credential_file = get_valid_file_path("Enter the path to the credential file: ")
    patient_file = get_valid_file_path("Enter the path to the patient data CSV file: ")

    user_authenticator = UserAuthentication(credential_file)

    username = input("Enter username: ")
    password = input("Enter password: ")

    role = user_authenticator.authenticate_user(username, password)

    if role is None:
        print("Invalid credentials.")
        return
    else:
        print("Welcome! You logged as ",role)

    manager = PatientRecordManager(patient_file)

    if role == "management":
        manager.generate_key_statistics()
        print("Generating key statistics")
    
    elif role == "admin":
        date_str = input("Enter the date (yyyy-mm-dd): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            total_visits = manager.count_visits_on_date(date)
            print("Total visits on {}: {}".format(date_str, total_visits))
        except ValueError:
            print("Invalid date format. Please enter date in yyyy-mm-dd format.")

    elif role in ["nurse", "clinician"]:
        while True:
            print("\n{} Menu:".format(role.capitalize()))
            print("1. Add patient record")
            print("2. Remove patient record")
            print("3. Retrieve patient record")
            print("4. Count visits on a specific date")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                manager.add_patient_record()
            elif choice == "2":
                manager.remove_patient_record()
            elif choice == "3":
                patient_record = manager.retrieve_patient_record()
                if patient_record:
                    print("Patient Information:")
                    for visit in patient_record:
                        print("Visit ID:", visit.Visit_ID)
                        print("Visit Time:", visit.Visit_time)
                        print("Visit Department:", visit.Visit_department)
                        print("Gender:", visit.Gender)
                        print("Race:", visit.Race)
                        print("Age:", visit.Age)
                        print("Ethnicity:", visit.Ethnicity)
                        print("Insurance:", visit.Insurance)
                        print("Zip Code:", visit.Zip_code)
                        print("Chief Complaint:", visit.Chief_complaint)
                        print("Note ID:", visit.Note_ID)
                        print("Note Type:", visit.Note_type)
            elif choice == "4":
                date_str = input("Enter the date (yyyy-mm-dd): ")
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    total_visits = manager.count_visits_on_date(date)
                    print("Total visits on {}: {}".format(date_str, total_visits))
                except ValueError:
                    print("Invalid date format. Please enter date in yyyy-mm-dd format.")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
