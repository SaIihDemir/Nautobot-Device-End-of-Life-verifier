from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from datetime import datetime, date

class VerifyEOL(Job) :
 class Meta:
         description = """
             1.Lists every device with an expired EOL(End-of-Life).
             2.Shows who the device belongs to, including the contact information .
             """
         name = "Compare EOL date with today and filter obsolete devices."
         
        
 def run (self, data, commit):
  for device in Device.objects.all():
            eol = device.cf["eol"]
            obsolete_devices = []
            if eol:
                eol=datetime.strptime(eol, '%Y-%m-%d').date()
                if eol < date.today():
                    obsolete_devices.append(device)
                    sorted_obsolete_devices = sorted(obsolete_devices(key=, reverse = False)
                    for devices in sorted_obsolete_devices:
                        contact = device.cf["contact"], devices, devices.cf["eol"]
                        self.log_failure(obj= sorted_obsolete_devices, message = "Inform GWDG and the contact about this Device")
  return contact
                     
                  
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                           
 
