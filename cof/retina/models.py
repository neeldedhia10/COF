from django.db import models
from django.core.validators import int_list_validator

class Patient(models.Model):
    patient_id = models.CharField(max_length=15, primary_key=True)
    # patient_name = models.CharField(max_length=50)
    # is_right = models.BooleanField(default=True)
    width = models.IntegerField(default='0')
    height = models.IntegerField(default='0')

    od_x = models.IntegerField(default='0')
    od_y = models.IntegerField(default='0')

    cf_x = models.IntegerField(null=True)
    cf_y = models.IntegerField(null=True)

    ma_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    ma_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    ma_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    rh_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    rh_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    rh_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    he_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    he_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    he_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    cws_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    cws_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    cws_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    nve_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    nve_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    nve_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    nvd_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    nvd_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    nvd_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    sh_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    sh_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    sh_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    vh_x = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    vh_y = models.CharField(validators=[int_list_validator], max_length=100, default='0')
    vh_r = models.CharField(validators=[int_list_validator], max_length=100, default='0')

    comment = models.CharField(max_length=500, null=True)
    is_processed = models.BooleanField(default=False)
    under_process = models.BooleanField(default=False)
    def __str__(self):
        return self.patient_id
