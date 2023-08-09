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
from retina. resources import PatientResource

static_path = settings.STATIC_PATH


@login_required
def index(request):
    # ASSUMPTION: All files in static folder have an entry in db with filename as the patient_id (primary key)
    all_patients = Patient.objects.all()
    count = all_patients.count()
    print("Count  = : " + str(all_patients.count()))
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
        # In case partial pages were input earlier, make them null
        up.cf_x = 0
        up.cf_y = 0
        up.ma_x = ""
        up.ma_y = ""
        up.ma_r = ""
        up.rh_x = ""
        up.rh_y = ""
        up.rh_r = ""
        up.he_x = ""
        up.he_y = ""
        up.he_r = ""
        up.cws_x = ""
        up.cws_y = ""
        up.cws_r = ""
        up.nve_x = ""
        up.nve_y = ""
        up.nve_r = ""
        up.nvd_x = ""
        up.nvd_y = ""
        up.nvd_r = ""
        up.sh_x = ""
        up.sh_y = ""
        up.sh_r = ""
        up.vh_x = ""
        up.vh_y = ""
        up.vh_r = ""
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
def cf(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
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

        patient.save()
        # is_back = "0"
        my_x = patient.cf_x
        my_y = patient.cf_y
        template = loader.get_template('retina/cof.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y
        }
        return HttpResponse(template.render(context, request))

# Save VH data


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


def csv_write(patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    fields = ['Patient ID', 'WIDTH', 'HEIGHT', 'OD_X', 'OD_Y', 'CF_X', 'CF_Y',
              'MA_X', 'MA_Y', 'MA_R',
              'RH_X', 'RH_Y', 'RH_R',
              'HE_X', 'HE_Y', 'HE_R',
              'CWS_X', 'CWS_Y', 'CWS_R',
              'NVE_X', 'NVE_Y', 'NVE_R',
              'NVD_X, NVD_Y',  'NVD_R',
              'SH_X', 'SH_Y', 'SH_R',
              'VH_X', 'VH_Y', 'VH_R',
              'Comment', 'PROCESSED', 'UnderProcess']
    row = ([patient.patient_id,  patient.width, patient.height, patient.od_x, patient.od_y, patient.cf_x, patient.cf_y,
           patient.ma_x, patient.ma_y, patient.ma_r,
           patient.rh_x, patient.rh_y, patient.rh_r,
           patient.he_x, patient.he_y, patient.he_r,
           patient.cws_x, patient.cws_y, patient.cws_r,
           patient.nve_x, patient.nve_y, patient.nve_r,
           patient.nvd_x, patient.nvd_y, patient.nvd_r,
           patient.sh_x, patient.sh_y, patient.sh_r,
           patient.vh_x, patient.vh_y, patient.vh_r,
           patient.comment, patient.is_processed, patient.under_process])
    fname = "./" + patient_id + ".csv"
    with open(fname, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, lineterminator='\n')
        # writing the fields
        print(row)
        for elem in row:
            csvwriter.writerow([elem])


def detail(request, patient_id):
    # print("HK  " + str(pid))
    # myobj = Patient.objects.filter(patient_id= pid)
    patient = get_object_or_404(Patient, pk=patient_id)
    # Send the patient image filename along with ... ?
    pid_imgfn = str(static_path + "/" + patient_id + ".jpg")
    print("Pid : " + patient_id)
    print("Patient.patient_id = " + patient_id)
    # print("Patient.patient_name = " + patient.patient_name)
    print("pid_imgfn = " + pid_imgfn)
    return render(request, 'retina/detail.html', {'patient': patient, 'pid_imgfn': pid_imgfn})


def process(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    try:
        selected = patient(pk=request.POST['right'])
    except KeyError:
        return render(request, 'retina/detail.html', {
            'patient_id': patient_id,
            'error_message': "Error in selection",
        })
    else:
        selected.is_right = True
        selected.save()
        return render(request, 'retina/detail.html', {'patient_id': patient_id})


# Save CF data
def ma(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')

            # Dealing with no CF in ma view
            try:
                xx = int(my_x)
            except ValueError:
                xx = None

            try:
                yy = int(my_y)
            except ValueError:
                yy = None

            print("xx = " + str(xx))
            # Save the CF center
            patient.cf_x = xx
            patient.cf_y = yy
            patient.save()

        my_x = patient.ma_x
        my_y = patient.ma_y
        my_r = patient.ma_r
        template = loader.get_template('retina/ma.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y, 'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save MA data
def rh(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the MA data
            patient.ma_x = my_x
            patient.ma_y = my_y
            patient.ma_r = my_r
            patient.save()

        my_x = patient.rh_x
        my_y = patient.rh_y
        my_r = patient.rh_r
        template = loader.get_template('retina/rh.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y, 'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save RH Data
def he(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the RH data
            patient.rh_x = my_x
            patient.rh_y = my_y
            patient.rh_r = my_r
            patient.save()

        my_x = patient.he_x
        my_y = patient.he_y
        my_r = patient.he_r

        template = loader.get_template('retina/he.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y,
            'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save HE Data
def cws(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the HE data
            patient.he_x = my_x
            patient.he_y = my_y
            patient.he_r = my_r

            patient.save()

        my_x = patient.cws_x
        my_y = patient.cws_y
        my_r = patient.cws_r

        template = loader.get_template('retina/cws.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y,
            'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save CWS Data
def nve(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the CWS data
            patient.cws_x = my_x
            patient.cws_y = my_y
            patient.cws_r = my_r

            patient.save()
        my_x = patient.nve_x
        my_y = patient.nve_y
        my_r = patient.nve_r

        template = loader.get_template('retina/nve.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y,
            'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save NVE Data
def nvd(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the NVE data
            patient.nve_x = my_x
            patient.nve_y = my_y
            patient.nve_r = my_r

            patient.save()

        my_x = patient.nvd_x
        my_y = patient.nvd_y
        my_r = patient.nvd_r

        template = loader.get_template('retina/nvd.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y,
            'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save NVD Data
def sh(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the NVD data
            patient.nvd_x = my_x
            patient.nvd_y = my_y
            patient.nvd_r = my_r

            patient.save()

        my_x = patient.sh_x
        my_y = patient.sh_y
        my_r = patient.sh_r

        template = loader.get_template('retina/sh.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y,
            'my_r': my_r
        }
        return HttpResponse(template.render(context, request))


# Save SH Data
def vh(request):
    if request.method == 'POST':
        is_back = 'is_back' in request.POST and request.POST.get('is_back')
        patient_id = 'patient_id' in request.POST and request.POST.get(
            'patient_id')
        patient = Patient.objects.get(patient_id=patient_id)
        pid_imgfn = os.path.join(patient_id + ".jpg")

        if is_back == "0":
            my_x = 'my_x' in request.POST and request.POST.get('my_x')
            my_y = 'my_y' in request.POST and request.POST.get('my_y')
            my_r = 'my_r' in request.POST and request.POST.get('my_r')

            # Save the SH data
            patient.sh_x = my_x
            patient.sh_y = my_y
            patient.sh_r = my_r

            patient.save()

        my_x = patient.vh_x
        my_y = patient.vh_y
        my_r = patient.vh_r

        template = loader.get_template('retina/vh.html')
        context = {
            'patient_id': patient_id, 'pid_imgfn': pid_imgfn, 'is_back': is_back, 'my_x': my_x, 'my_y': my_y,
            'my_r': my_r
        }
        return HttpResponse(template.render(context, request))
