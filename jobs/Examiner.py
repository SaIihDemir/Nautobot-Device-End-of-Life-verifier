from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from nautobot.extras.models import CustomField
from datetime import datetime, date


class Verifyer(Job) :
 class Meta:
         description = """
             1.Lists every device with a expired EOL(End-of-Life).
             2.Shows the contact person, whos EOL has expired.
             """
         name = "Function : compare eol date with today and filter obsolete devices."
  
def run(self, data, commit):  
        obsolete_devices = []
 
        for device in Device.objects.all():
            eol = device.cf["eol"]         
            eol = datetime.strptime(eol_field, '%Y-%m-%d').date()
            if eol < date.today():
               obsolete_devices.append(device)

            for devices in obsolete_devices:
                self.log_failure(obj = devices, message = "test")
                 
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                                   
                           
 
