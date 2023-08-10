# Copyrights 2020,  Sankara Netralaya & BITS Pilani,
# Contact: sundaresan.raman@pilani.bits-pilani.ac.in

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from os import walk
import pathlib
import os.path
import json
from django.conf import settings
import csv
import re

from datetime import datetime
import os
from openpyxl import Workbook
from PIL import Image

from retina.models import Patient
from retina.resources import PatientResource

static_path = settings.STATIC_PATH


@login_required
def index(request):
    # ASSUMPTION: All files in static folder have an entry in db with filename as the patient_id (primary key)
    all_patients = Patient.objects.all()
    count = all_patients.count()
    # print("Count  = : " + str(all_patients.count()))
    all_over = True
    for i in range(count):
        if all_patients[i].is_processed == False:
            all_over = False
            curr_patient = all_patients[i]
            break
    # print("i = " + str(i))
    if all_over == True:
        return HttpResponse("<h2> All patients are annotated! </h2>")
    else:
        curr_patient = all_patients[i]
        patient_id = curr_patient.patient_id
        up = Patient.objects.get(patient_id=patient_id)
        up.under_process = True
        pid_imgfn = os.path.join(patient_id + ".jpg")
        # Get image dimensions
        im = Image.open(os.path.join(static_path, pid_imgfn))
        width, height = im.size
        print("width = " + str(width))
        print("height = " + str(height))
        up.width = width
        up.height = height

        up.save()

        is_back = "0"
        template = loader.get_template('retina/index.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back
        }
        return HttpResponse(template.render(context, request))

@login_required
def last(request):
    if request.method == 'POST':
        # Last page so no need to check for is_back
        # is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        # if is_back == "0":
        my_x = 'my_x' in request.POST and request.POST.get('my_x')
        my_y = 'my_y' in request.POST and request.POST.get('my_y')
        # Save the OD centers
        patient.od_x = my_x
        patient.od_y = my_y
        patient.is_processed = True
        patient.under_process = False
        patient.save()
        # Now save this patient onto a csv
        # csv_write(patient_id)
        all_patients = Patient.objects.all()
        count = all_patients.count()
        print("Count in ma = : " + str(all_patients.count()))
        all_over = True
        for i in range(count):
            if all_patients[i].is_processed == False:
                all_over = False
                curr_patient = all_patients[i]
                break
        # print("i = " + str(i))

        if all_over == True:
            patient_resource = PatientResource()
            dataset = patient_resource.export()
            wb = Workbook()
            ws = wb.active
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d%b%Y%H%M%S")
            title = "Database" + "_" + str(timestampStr)
            ws.title = "Annotation"
            field_names = patient_resource.get_fields()
            print(field_names)

            for row in dataset:
                ws.append(row)

            fname = title + ".xlsx"
            wb.save(fname)
            return HttpResponse("<h2> All patients are annotated! </h2>")
        else:
            curr_patient = all_patients[i]
            patient_id = curr_patient.patient_id
            pid_imgfn = os.path.join(patient_id + ".jpg")

            # Get image dimensions
            pp = Patient.objects.get(patient_id=patient_id)
            im = Image.open(os.path.join(static_path, pid_imgfn))
            width, height = im.size
            print("width = " + str(width))
            print("height = " + str(height))
            pp.width = width
            pp.height = height
            pp.save()
            template = loader.get_template('retina/index.html')
            context = {
                'patient_id': patient_id, 'pid_imgfn': pid_imgfn
            }
            return HttpResponse(template.render(context, request))


