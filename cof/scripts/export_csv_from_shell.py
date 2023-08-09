from datetime import datetime
import csv
import os
from openpyxl import Workbook
from retina.models import Patient
from retina. resources import PatientResource

patient_resource = PatientResource()
dataset = patient_resource.export()
wb=Workbook()
ws=wb.active

dateTimeObj = datetime.now()

timestampStr = dateTimeObj.strftime("%d%b%Y%H%M%S")
title="Database" + "_"+ str(timestampStr)
ws.title="Annotation"
for row in dataset:
    ws.append(row)

fname=title+".xlsx"
wb.save(fname)



