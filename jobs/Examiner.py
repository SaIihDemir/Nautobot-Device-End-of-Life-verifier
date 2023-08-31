from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from nautobot.extras.models import CustomField
from datetime import datetime, date
import json

class Verifyer(Job) :
 class Meta:
         description = """
             1.Lists every device with a expired EOL(End-of-Life).
             2.Shows the contact person, whos EOL has expired.
             """
         name = "Function : compare eol date with today and filter obsolete devices."
 
def run(self, data, commit):
        eol_field_name = "EOL Date"  # Replace with the actual name of the EOL custom field
        obsolete_devices = []

        for device in Device.objects.all():
            eol_field = device.custom_field_data.get(eol_field_name)
            if eol_field:
                eol = datetime.strptime(eol_field, '%Y-%m-%d').date()
                if eol < date.today():
                    obsolete_devices.append(device)
         
 
     if obsolete_devices:
                 self.log_failure("Check the following obsolete devices:")
                 for device in obsolete_devices:
                     self.log_failure(device)
 