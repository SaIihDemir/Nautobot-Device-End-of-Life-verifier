from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from datetime import datetime, date
import csv
from operator import attrgetter

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
      unwanted_devices = [""]
      for device in Device.objects.all():
         if device in unwanted_devices:
            continue 
         eol = device.cf["eol"]
         try:
            eol=datetime.strptime(eol, '%Y-%m-%d').date()
            if eol < date.today():   
               obsolete_devices.append(device) 
         except Exception as e:
                self.log_failure(message = "Error parsing EOL date: {}".format(str(e)))
                continue
             
# see if customfield "contact" has more than one e-mail in it.
# sort obsolete devices by contact and show log message if we have no obsolete devices 
         
      one_contact_devices = []

      for one_contact in obsolete_devices:
         if len(one_contact) >2:
            for one_mail in (one_contact[0:len(one_contact)-1]):
               one_contact_devices.append([one_mail,one_contact[-1]])
         else:
            one_contact_devices.append(one_contact)
         
         if obsolete_devices:
            sorted_devices = sorted(one_contact_devices, key=lambda x: x.cf["contact"])
         else:
            self.log_failure(obj=None, message = "no obsolete Device found")

       
#list for contacts with all their devices
      contact_devices = []
      i = -2
      j = -1
      for device in sorted_devices:
         i += 1
         if device.cf["contact"] != sorted_devices[i].cf["contact"]:
            contact_devices.append([device.cf["contact"],[device]])
            j += 1
         else:
            contact_devices[j][1].append(device)
          
# Create csv file for obsolete devices
      with open('obsolete_devices.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ['Contact', 'Device', 'EOL']
            writer.writerow(field)
            for device in sorted_devices:
               writer.writerow([device.cf["contact"],device,device.cf["eol"]])
            self.log_success(obj = None, message = "created csv file for obsolete devices")   
       
      emails = []
  
      for contact in contact_devices:
          device_string = ""
          for device in contact[1]:
              device_string += device.name + "\n"
          email = """
Sehr geehrte/r {},
folgende Geräte mit der/den Bezeichnung/Bezeichnungen:
{}
haben ihr EOL erreicht.

Bitte prüfen Sie folgende Informationen:
1. Ist das Gerät noch produktiv im Einsatz?
2. Ist die Herstellergarantie noch aktuell?
3. Sind alle Softwarekomponenten auf dem aktuellen Stand?
      """.format(contact[0], device_string)
          emails.append(email)
       
      return'\n'.join(emails)
           
