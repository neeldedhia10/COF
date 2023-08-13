from django.db import models
from django.core.validators import int_list_validator


class Patient(models.Model):
    patient_id = models.CharField(max_length=15, primary_key=True)
    # patient_name = models.CharField(max_length=50)
    # is_right = models.BooleanField(default=True)
    width = models.IntegerField(default='0')
    height = models.IntegerField(default='0')
    link = models.CharField(max_length=500, default='')
    od_x = models.IntegerField(default='0')
    od_y = models.IntegerField(default='0')
    
    is_processed = models.BooleanField(default=False)
    under_process = models.BooleanField(default=False)

    def __str__(self):
        return self.patient_id
