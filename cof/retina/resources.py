from import_export import resources
from .models import Patient

class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient

