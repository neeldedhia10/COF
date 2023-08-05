

from retina.models import Patient
Patient.objects.all().delete()
p=Patient("dummy")
p.save()
