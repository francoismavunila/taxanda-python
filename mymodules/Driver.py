import hashlib
import time
import tempfile
from mymodules import mqttConnect
import base64
import json
import sqlite3
import datetime
from pyfingerprint.pyfingerprint import PyFingerprint



dbconnect = sqlite3.connect("taxanda.db");
dbconnect.row_factory = sqlite3.Row;
#now we create a cursor to work with db
cursor = dbconnect.cursor()

## Tries to initialize the sensor
try:
    d = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( d.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(d.getTemplateCount()) +'/'+ str(d.getStorageCapacity()))

def getDriverFingerPrint(driver_id):
      ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( d.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        d.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = d.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( d.readImage() == False ):
            pass
        
        print('Downloading image (this take a while)...')

        imageDestination =  tempfile.gettempdir() + '/driver.bmp'
        d.downloadImage(imageDestination)

        print('The image was saved to "' + imageDestination + '".')
        ## Converts read image to characteristics and stores it in charbuffer 2
        d.convertImage(0x02)

        ## Compares the charbuffers
        if ( d.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        d.createTemplate()
  
        ## Saves template at new position number
        positionNumber = d.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        d.loadTemplate(positionNumber, 0x01)
    ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(d.downloadCharacteristics(0x01)).encode()
        print(len(characterics))
        dataBase64 =base64.b64encode(characterics)
        #print()
        template=dataBase64.decode()
        currentDT = datetime.datetime.now()
        #cursor.execute('''INSERT INTO driver (driverId, deviceId, template,image,date) VALUES ('driver_id', '1010',template,imageDestination,currentDT )''')
        cursor.execute('INSERT INTO driver (driverId, deviceId, template,image,date) VALUES(?, ?, ?, ?, ?)', (driver_id, 1010,template,imageDestination,currentDT ))
        dbconnect.commit();
        dat={
            "device_id":1010,
            "driver_id":driver_id,
            "data":dataBase64.decode()
        }
        print(dat)
        print(dataBase64)
        my_json_object = json.dumps(dat)
        mqttConnect.driverMqtt("driv/register/sendFP",my_json_object)
        return positionNumber
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        #exit(1)
        return 301

def get_DriverfingerprintImage(id):
    ## Tries to read image and download it
    try:
       ## print('Waiting for finger...')

        ## Wait that finger is read
        #while ( d.readImage() == False ):
         #   pass
        print('Downloading image (this take a while)...')

        imageDestination =  tempfile.gettempdir() + '/driver.bmp'
        d.downloadImage(imageDestination)

        print('The image was saved to "' + imageDestination + '".')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
def delete_fingerprint():
    print('trying to delete finger print')
    ## Tries to delete the template of the finger
    try:
        positionNumber = input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)

        if ( d.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)