from django.conf import settings

# Importing Nautobot DCIM device model in order to be able to choose what device I want to connect to
from nautobot.dcim.models import Device

# The import of Job is needed to inherit the Job class. This is the magic sauce for Nautobot Jobs.
# ObjectVar import will be used to select a device
from nautobot.extras.jobs import Job, ObjectVar

# Import Netmiko to connect to the device and execute commands
from netmiko import ConnectHandler

# Setting the name here gives a category for these jobs to be categorized into
name = "josh-v.com Demo jobs"

class GetShowVersion(Job):
    device = ObjectVar(
        model=Device, # Using the Device model imported to say I want to select devices
        query_params={
            # Using this as a method to make sure that the device has a primary IP address
            "has_primary_ip": True, 
            "status": "active", # Used to make sure that the device is active
            }
        )

    # I like to describe the class Meta as what information about the Job to pass into Nautobot to help describe the Job
    class Meta:
        name = "Get show version"
        description = "Get the version information from a device"
        # Define task queues that this can run in.
        task_queues = [
            settings.CELERY_TASK_DEFAULT_QUEUE,
            "priority",
            "bulk",
            ]

    # The code execution, all things for the job are here.
    def run(self, data, commit):
        device = data["device"]

        self.log_debug(device)


jobs = (GetShowVersion)
