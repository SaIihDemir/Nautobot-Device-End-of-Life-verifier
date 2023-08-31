from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from datetime import datetime, date
import json

class Verifyer(Job) :
 class Meta:
         description = """
             1.Lists every device with a expired EOL(End-of-Life).
             2.Shows the contact person, whos EOL has expired.
             """
         name = "Function : compare eol date with today and filter obsolete devices."
 
 def run (self, data, commit):
     device = Device.objects.all()  
     eol_date_str = Device.customfields.CustomFieldModels.objects.all()
  
     obsolete_devices = []                                           #create a list for expired devices
         
     for device in Device.objects.all():
             eol_date_str = Device.eol.get('eol', None)  
             if eol_date_str:
                 eol_date = datetime.strptime(eol_date_str, '%Y-%m-%d').date()
                 if eol_date < date.today():
                     obsolete_devices.append(display)
         
 
     if obsolete_devices:
                 self.log_failure("Check the following obsolete devices:")
                 for device in obsolete_devices:
                     self.log_failure(device)
 
