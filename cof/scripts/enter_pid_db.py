import os
from retina.models import Patient
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cof.settings')
# This script enters into db for each image in the input folder

base_dir = r"C:\BITS PILANI\4-1\SOP - PROF RAMAN\COF\cof\static"
# input_dir = str(base_dir + "\Clarus_25")
# input_dir = str(base_dir + "\Optos_25")
input_dir = base_dir
# print(input_dir)

for file_name in os.listdir(input_dir):
    pid = file_name
    ftype = ".jpg"
    if pid.endswith(ftype):
        print("Entering patient :" + file_name)
        res = pid[:-(len(ftype))]
        p = Patient(patient_id=res)
        p.save()
# print(input_dir)
