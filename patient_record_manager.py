import csv
from datetime import datetime
from patient_record import PatientRecord
import matplotlib.pyplot as plt

class PatientRecordManager:
    def __init__(self, patient_file):
        self.patient_records = self.read_patient_data_from_csv(patient_file)

    def read_patient_data_from_csv(self, file_path):
        patient_records = {}
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                valid_keys = {key.replace(" ", "_"): value for key, value in row.items() if value.strip() != '' and key.strip() != ''}
                patient_record = PatientRecord(**valid_keys)
                patient_id = valid_keys['Patient_ID']
                if patient_id in patient_records:
                    patient_records[patient_id].append(patient_record)
                else:
                    patient_records[patient_id] = [patient_record]
        return patient_records

    def add_patient_record(self):
        patient_id = input("Enter Patient ID: ")
        visit_id = input("Enter Visit ID: ")
        visit_time = input("Enter Visit Time (yyyy-mm-dd): ")
        visit_department = input("Enter Visit Department: ")
        gender = input("Enter Gender: ")
        race = input("Enter Race: ")
        age = int(input("Enter Age: "))
        ethnicity = input("Enter Ethnicity: ")
        insurance = input("Enter Insurance: ")
        zip_code = input("Enter Zip Code: ")
        chief_complaint = input("Enter Chief Complaint: ")
        note_id = input("Enter Note ID: ")
        note_type = input("Enter Note Type: ")
        patient_record = PatientRecord(patient_id, visit_id, visit_time, visit_department, gender, race, age, ethnicity, insurance, zip_code, chief_complaint, note_id, note_type)
        if patient_id in self.patient_records:
            visit_id = str(len(self.patient_records[patient_id]) + 1)
            patient_record.Visit_ID = visit_id
            self.patient_records[patient_id].append(patient_record)
        else:
            self.patient_records[patient_id] = [patient_record]
        print("Patient record added successfully.")

    def remove_patient_record(self):
        patient_id = input("Enter Patient ID: ")
        if patient_id in self.patient_records:
            del self.patient_records[patient_id]
            print("Patient record removed successfully.")
        else:
            print("Patient ID not found.")

    def retrieve_patient_record(self):
        patient_id = input("Enter Patient ID: ")
        if patient_id in self.patient_records:
            return self.patient_records[patient_id]
        else:
            print("Patient ID not found.")
            return None

    def count_visits_on_date(self, date):
        total_visits = 0
        for patient_id, visits in self.patient_records.items():
            for visit in visits:
                visit_date = datetime.strptime(visit.Visit_time, "%Y-%m-%d")
                if visit_date.date() == date:
                    total_visits += 1
        return total_visits
        
    def generate_key_statistics(self):
        patient_records = [record for records in self.patient_records.values() for record in records]

        # Calculate key statistics here
        # For example:
        # 1. Temporal trend of the number of patients who visited the hospital
        visit_dates = [datetime.strptime(record.Visit_time, "%Y-%m-%d") for record in patient_records]
        plt.figure(figsize=(10, 6))
        plt.hist(visit_dates, bins=30, edgecolor='black')
        plt.title('Temporal Trend of Hospital Visits')
        plt.xlabel('Date')
        plt.ylabel('Number of Visits')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('hospital_visits.png')
        plt.close()

        # Other statistics...

    def generate_key_statistics(self):
        patient_records = [record for records in self.patient_records.values() for record in records]

        # 1. Temporal trend of the number of patients who visited the hospital
        visit_dates = [datetime.strptime(record.Visit_time, "%Y-%m-%d") for record in patient_records]
        plt.figure(figsize=(10, 6))
        plt.hist(visit_dates, bins=30, edgecolor='black')
        plt.title('Temporal Trend of Hospital Visits')
        plt.xlabel('Date')
        plt.ylabel('Number of Visits')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('hospital_visits.png')
        plt.close()

        # 2. Temporal trend of the number of patients who visited the hospital with different types of insurances
        insurance_counts = {}
        for record in patient_records:
            if record.Insurance in insurance_counts:
                insurance_counts[record.Insurance] += 1
            else:
                insurance_counts[record.Insurance] = 1
        plt.figure(figsize=(8, 6))
        plt.bar(insurance_counts.keys(), insurance_counts.values(), color='skyblue')
        plt.title('Temporal Trend of Patients with Different Insurances')
        plt.xlabel('Insurance Type')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('insurance_trend.png')
        plt.close()

        # 3. Temporal trend of the number of patients who visited the hospital in different demographics groups
        race_counts = {}
        gender_counts = {}
        age_groups = {}

        for record in patient_records:
            # Race
            if record.Race in race_counts:
                race_counts[record.Race] += 1
            else:
                race_counts[record.Race] = 1

            # Gender
            if record.Gender in gender_counts:
                gender_counts[record.Gender] += 1
            else:
                gender_counts[record.Gender] = 1

            # Age (assuming age groups are predefined)
            age = int(record.Age)
            age_group = self.get_age_group(age)
            if age_group in age_groups:
                age_groups[age_group] += 1
            else:
                age_groups[age_group] = 1

        plt.figure(figsize=(8, 6))
        plt.bar(race_counts.keys(), race_counts.values(), color='orange')
        plt.title('Temporal Trend of Patients by Race')
        plt.xlabel('Race')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('race_trend.png')
        plt.close()

        plt.figure(figsize=(8, 6))
        plt.bar(gender_counts.keys(), gender_counts.values(), color='green')
        plt.title('Temporal Trend of Patients by Gender')
        plt.xlabel('Gender')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('gender_trend.png')
        plt.close()

        plt.figure(figsize=(8, 6))
        plt.bar(age_groups.keys(), age_groups.values(), color='purple')
        plt.title('Temporal Trend of Patients by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('age_group_trend.png')
        plt.close()

    def get_age_group(self, age):
    # Define age groups and their ranges
        age_groups = {
        '0-20': range(0, 21),
        '21-40': range(21, 41),
        '41-60': range(41, 61),
        '61-80': range(61, 81),
        '81+': range(81, 150)
        }

        for group, age_range in age_groups.items():
            if age in age_range:
                return group
        return 'Unknown'
