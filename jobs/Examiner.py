from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from datetime import datetime, date
import csv
from operator import attrgetter, itemgetter
import re


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
      unwanted_devices = ["Frame","Rackdevice","Patchpanel"]
      for device in Device.objects.all():
         if device.device_role.name in unwanted_devices:
            continue 
         eol = device.cf["eol"]
         try:
            eol=datetime.strptime(eol, '%Y-%m-%d').date()
            if eol < date.today():
               obsolete_devices.append(device) 
         except Exception as e:
                self.log_failure(message = "Error parsing EOL date: {}".format(str(e)))
                continue
             
# sort obsolete devices by contact and show log message if we have no obsolete devices    
      if obsolete_devices:
         sorted_devices = sorted(obsolete_devices, key=lambda x: x.cf["contact"])
      else:
         self.log_failure(obj=None, message = "no obsolete Device found")

       
#contact_Devices = list for contacts with all their devices 
#only_one_contact = splits up devices with multiple contacts into seperate contacts with their devices
 
     
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

#split multiple mail adresses string seperate strings with devices
      split_contacts = []                  
      for contact_with_device in contact_devices:
          seperated_mail = re.split(r"[\s]\s*", contact_with_device[0])
          split_contacts.append([seperated_mail,contact_with_device[-1]])
            
      one_mail_with_devices = []      
      for devices in split_contacts:
          if len(devices[0]) > 0:
              for mail in (devices[0]):
                  one_mail_with_devices.append([mail,devices[-1]])
      one_mail_with_devices = sorted(one_mail_with_devices, key = itemgetter(0))
  
      contact_devices = []
      i = -2
      for contact in one_mail_with_devices:
          i += 1
          mail = contact[0]
          devices = contact[1]
          email = mail.replace(" ", "")
          previous_mail = one_mail_with_devices[i][0].replace(" ", "")
          if email == previous_mail:
              for device in devices:
                  if device in contact_devices[-1][1]:
                      continue
                  else:
                      contact_devices[-1][1].append(device)
          elif email != previous_mail:  
              contact_devices.append([email,devices])

# Create csv file for obsolete devices
      with open('obsolete_devices.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ['Contact', 'Device', 'EOL']
            writer.writerow(field)
            for contact_with_devices in contact_devices:
               contact = contact_with_devices[0]
               devices = contact_with_devices[1]
               device_string = ""
               device_eol = ""
               for device in devices:
                   device_string += device.name + ", " 
                   device_eol += device.cf["eol"] + ", "
               writer.writerow([contact,device_string,device_eol])
            self.log_success(obj = None, message = "created csv file for obsolete devices")   
       
      emails = []
  
      for contact in contact_devices:
          device_string = ""
          for device in contact[-1]:
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
           
