from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from datetime import datetime, date
import csv
import operator import itemgetter

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
                  obsolete_devices.append([device.cf["contact"],device, device.cf["eol"]])
                  sorted(obsolete_devices,key=itemgetter(0))
                  self.log_failure(obj=obsolete_devices, message = "HI")                
  return obsolete_devices
                     
                  
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                           
 
