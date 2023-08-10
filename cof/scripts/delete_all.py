import os
from retina.models import Patient
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cof.settings')

Patient.objects.all().delete()
# p=Patient("TEST1")
# p.save()
