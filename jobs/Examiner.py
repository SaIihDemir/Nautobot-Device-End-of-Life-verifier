from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from datetime import datetime, date
import csv
from operator import itemgetter

class VerifyEOL(Job) :
 class Meta:
         description = """
             1.Lists every device with an expired EOL(End-of-Life).
             2.Shows who the device belongs to, including the contact information .
             """
         name = "Compare EOL date with today and filter obsolete devices."
         
        
 def run (self, data, commit):
  
      for device in Device.objects.all():
         if device: 
            eol = device.cf["eol"]
            obsolete_devices = []
            eol=datetime.strptime(eol, '%Y-%m-%d').date()
            if eol < date.today():
               obsolete_devices.append([device.cf["contact"],device.name, device.cf["eol"]]) 
         
      if obsolete_devices:
         sorted_obsolete_devices=sorted(obsolete_devices,key=itemgetter(0))   
         with open('obsolete_devices.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ['Contact', 'Device', 'EOL']
            writer.writerow(field) 
            for devices in obsolete_devices:
                with open('obsolete_devices', 'a', newline='') as p:
                     writer.writerow(devices)
         self.log_success(obj=None , message = "created list with obsolete Devices")     
      else:
            self.log_failure(obj=None, message = "no obsolete Device found")
           
                     
                     
                     
                     
                  
                                   
                  
                     
                                   
                                   
                                   
                                   
                                   
                                   
                           
 
