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

     # create a list for obsolete devices and add devices, including their contact, name and End-of-Life(EOL), whos EOL is exceeded
      obsolete_devices = []
      for device in Device.objects.all():
         if device: 
            eol = device.cf["eol"]
            eol=datetime.strptime(eol, '%Y-%m-%d').date()
            if eol < date.today():
               obsolete_devices.append([device.cf["contact"],device.name, device.cf["eol"]]) 
             
     # sort obsolete devices by contact and show log message if we have no obsolete devices    
      if obsolete_devices:
         obsolete_devices=sorted(obsolete_devices,key=itemgetter(0))        
      else:
         self.log_failure(obj=None, message = "no obsolete Device found")

       
#new list without duplicate contact-information
      no_duplicate_contact = []

      i = -2
      for contact_mail in obsolete_devices:
         i += 1
         if contact_mail[0] == obsolete_devices[i][0]:
            no_duplicate_contact.append([[print(None)],contact_mail[1],contact_mail[2]]) 
         else:
            no_duplicate_contact.append(contact_mail)
          
# Create csv file for obsolete devices
      with open('obsolete_devices.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ['Contact', 'Device', 'EOL']
            writer.writerow(field)
            for contact in no_duplicate_contact:
               writer.writerow(contact)
             
      self.log_success(obj = None, message = "created obsolete devices csv file")
      return (no_duplicate_contact)     
