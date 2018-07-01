from pyicloud import PyiCloudService

# TODO: Please insert icloud username and password below
api = PyiCloudService('<iCloud Email>', '<iCloud Password>') #


# This is the file that takes care of connecting to iCloud on my pi.
# It is used primarily to check events on a calender and create reminders
# in the reminders app.
# This first part is just a prompt that will appear on the first startup
# to request a security pin from your icloud account.

if api.requires_2fa:
    import click
    print ("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print ("  %s: %s" % (i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print ("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print ("Failed to verify verification code")
        sys.exit(1)

def date():
    pass


# This is where the actual actions take place

def makeReminder(title,description,year,month,day,hour,minute):
    date.year = " ".join(year)
    date.month = " ".join(month)
    date.day = " ".join(day)
    date.hour = " ".join(hour)
    date.minute = " ".join(minute)
    api.reminders.post(" ".join(title)," ".join(description),date)

def showEvents():
    events = api.calendar.events()
    response = []
    for event in events:
        response.append(event['title'] + " starting at " + str(event["localStartDate"][4])+":"+str(event["localStartDate"][5]) + " on " + str(event["localStartDate"][2])+"/"+str(event["localStartDate"][3]))
    return response

def interpret(r):
    if "make reminder" in r:
        r = r.split(" ")
        try:
            makeReminder(r[r.index("title")+1:r.index("description")],r[r.index("description")+1:r.index("year")],r[r.index("year")+1:r.index("month")],r[r.index("month")+1:r.index("day")],r[r.index("day")+1:r.index("hour")],r[r.index("hour")+1],"0")
        except:
            try:
                makeReminder(r[r.index("reminder")+1:r.index("description")],r[r.index("description")+1:],"","","","","")
            except:
                makeReminder(r[r.index("reminder")+1:], "" , "" , "" , "" , "" , "" )
        return "Reminder set"
    elif "show events" in r:
        return " and ".join(showEvents())
    else:
        return "Sorry, I could not understand your request."
