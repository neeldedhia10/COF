import csv
from retina.models import Patient
from django.db import transaction
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cof.settings')


# Path to your CSV file
csv_file_path = 'scripts/sorted_image_links.csv'
Patient.objects.all().delete()
# Read the CSV file and populate data
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip the header row

    with transaction.atomic():
        for row in reader:
            if len(row) >= 2:
                filename = row[0]
                link = row[1]
                patient_id = filename.split('.')[0]

                # Check if a record with the same patient_id exists
                existing_patient = Patient.objects.filter(
                    patient_id=patient_id).first()

                if existing_patient:
                    # Update the existing record if needed
                    existing_patient.link = link
                    existing_patient.save()
                else:
                    # Create a new Patient instance and save it to the database
                    Patient.objects.create(
                        patient_id=patient_id,
                        link=link
                    )

print("Database updated successfully.")
