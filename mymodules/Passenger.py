import hashlib
import time
import tempfile
from mymodules import mqttConnect
import base64
import json
import sqlite3
import datetime
import uuid
from mymodules import gps
from mymodules import setMessage
from mymodules import doorlock
from mymodules import getSeatNumber
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from pyfingerprint.pyfingerprint import PyFingerprint

lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D21)
lcd_en = digitalio.DigitalInOut(board.D20)
lcd_d7 = digitalio.DigitalInOut(board.D25)
lcd_d6 = digitalio.DigitalInOut(board.D1)
lcd_d5 = digitalio.DigitalInOut(board.D12)
lcd_d4 = digitalio.DigitalInOut(board.D16)
lcd_backlight = digitalio.DigitalInOut(board.D13)

lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)

lcd.clear()


dbconnect = sqlite3.connect("taxanda.db",check_same_thread=False);
dbconnect.row_factory = sqlite3.Row;
#now we create a cursor to work with db
cursor = dbconnect.cursor()

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyAMA1', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)


def enrollPaasengerFingerPrint():
      ## Tries to enroll new finger
    try:
        print('Waiting for finger.')
        setMessage.setMess("Passenger, place your finger on the scanner")
        lcd.message = "Place finger on\nthe scanner"
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            setMessage.setMess("Passenger fingerprint is already enrolled, first delete the enroll fingerprint")
            lcd.clear()
            lcd.message = "Your finger is\nalraedy enrolled"
            return 301

        print('Remove finger...')
        lcd.clear()
        lcd.message = "remover finger"
        setMessage.setMess("Remove Finger")
        time.sleep(1)

        print('Waiting for same finger again...')
        lcd.clear()
        lcd.message = "place the same/nfinger again"
        setMessage.setMess("place the same finger again")

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass
        currentDT = datetime.datetime.now()
        
        loc = gps.getCoordinates()
        location_coord = json.dumps(loc)
        picId = uuid.uuid1()
        picIdString = str(picId)
        print('Downloading image (this take a while)...')
        setMessage.setMess("we are acquiring the information, wait....")
        lcd.clear()
        scroll_msg="processing..\nPlease wait..."
        lcd.message = scroll_msg

        imageDestination =  tempfile.gettempdir() + '/'+picIdString+'.bmp'
        f.downloadImage(imageDestination)

        print('The image was saved to "' + imageDestination + '".')
        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            setMessage.setMess("enrollment failed, fingerprint data not properly captured, make sure you are steady and your hands are clean")
            lcd.clear()
            lcd.message = "Failed, clean\nyour hands"
            raise Exception('Fingers do not match delete te save image')

        ## Creates a template
        f.createTemplate()
        cursor.execute('SELECT Id FROM Count WHERE Present==0')
        rows = cursor.fetchall()
        if(len(rows)==0):
            setMessage.setMess("the taxi is full")
            lcd.clear()
            lcd.message = "the taxi is full"
            return 301
        for row in rows:
            print(row['Id'])
        print(len(rows))   
        print(rows[0]['Id'])

        passId=rows[0]['Id']
        
        ## Saves template at new position number
        positionNumber = f.storeTemplate(passId)
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

        sql_update_query = """Update Count set Present = ? where Id = ?"""
        data = (1, passId)
        cursor.execute(sql_update_query, data)
        dbconnect.commit()
        f.loadTemplate(positionNumber, 0x01)
    ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode()
        print(len(characterics))
        dataBase64 =base64.b64encode(characterics)
        #print()
        template=dataBase64.decode()
        
        #cursor.execute('''INSERT INTO driver (driverId, deviceId, template,image,date) VALUES ('driver_id', '1010',template,imageDestination,currentDT )''')
        cursor.execute('INSERT INTO activity (Template, Image, RideTime,ArrivalTime,Ride,Arrived,RideLocation,ArrivalLocation,sent,sentArrival,fingerPrintPosition,fingerPrintPositionHistory) VALUES(?, ?, ?, ?, ?,?,?,?,?,?,?,?)', (template, imageDestination,currentDT ,"null",1,0,location_coord ,"null",0,0,positionNumber,positionNumber ))
        dbconnect.commit();
        last_row_id = cursor.lastrowid
        print("last row")
        print(last_row_id)

        dat={
            "device_id":1010,
            "time": currentDT.strftime("%m/%d/%Y, %H:%M:%S"),
            "data": template,
            "rowId":last_row_id
        }
        #door open
        doorlock.doorlock("open")
        setMessage.setMess("Done,get in")
        cursor.execute('SELECT Id FROM Count WHERE Present==1')
        rows = cursor.fetchall()
        setMessage.setMess("waiting for passenger to take a seat")   
        while(len(rows)!=getSeatNumber.getSeatNumber()):
                time.sleep(1)
        setMessage.setMess("Passenger In")
        doorlock.doorlock("close")
        print(len(rows))
        print(getSeatNumber.getSeatNumber())       
        #print(dat)
        print(template)
        my_json_object = json.dumps(dat)
        mqttConnect.driverMqtt("activity/1010/depart",my_json_object)
        return positionNumber
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        #exit(1)
        return 301
def passengerArrival():
    try:
        #setMessage.setMess(" place your finger on the sensor")
        lcd.clear()
        lcd.message = "place finger\non the scanner"
        print('Waiting for finger...')
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        print('one')
        ## Searchs template
        result = f.searchTemplate()
        print('two')
        positionNumber = result[0]
        accuracyScore = result[1]
        print('three')
        if ( positionNumber == -1 ):
            print('No match found!')
            lcd.clear()
            lcd.message = "No Match"
            setMessage.setMess("Your finger doesn't match try again")
            return 301
        
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))
        currentDT = datetime.datetime.now()
     
        loc = gps.getCoordinates()
        location_coord = json.dumps(loc)
        
        query_statement="""SELECT Template,Id FROM Activity WHERE fingerPrintPosition=?"""
        dat=str(positionNumber)
        cursor.execute(query_statement,dat)
        rows = cursor.fetchall()
        print(len (rows))
        template=rows[0]['Template']
        rowId=rows[0]['Id']
        print(rowId)
        print(template)
        sql_update_query = """Update activity set ArrivalTime = ?,Arrived= ?,ArrivalLocation = ?,fingerPrintPosition=? where fingerPrintPosition = ?"""
        data = (currentDT,1,location_coord,301, positionNumber)
        sql_count = """Update Count set Present = ? where Id = ?"""
        countData = (0, positionNumber)
        cursor.execute(sql_update_query, data)
        cursor.execute(sql_count, countData)
        dbconnect.commit()
        lcd.clear()
        lcd.message = "done,you \ncan move out"
        dat={
            "device_id":1010,
            "time": currentDT.strftime("%m/%d/%Y, %H:%M:%S"),
            "data": template,
            "rowId":rowId
        }
#         setMessage.setMess("Done")
#         print(dat)
        #print(template)
        doorlock.doorlock("open")
        setMessage.setMess("Done,get in")
        cursor.execute('SELECT Id FROM Count WHERE Present==1')
        rows = cursor.fetchall()
        setMessage.setMess("waiting for passenger move out")   
        while(len(rows)!=getSeatNumber.getSeatNumber()):
                time.sleep(1)
        setMessage.setMess("Passenger out")
        doorlock.doorlock("close")
        print(len(rows))
        print(getSeatNumber.getSeatNumber()) 
        my_json_object = json.dumps(dat)
        mqttConnect.driverMqtt("activity/1010/arrival",my_json_object)
        return positionNumber

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        setMessage.setMess("error, contact technician +263783857780")
        return 301
def clearDriverInfo():
    f.clearDatabase()
def getTemplate():
        f.loadTemplate(2, 0x01)
    ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode()
        print(len(characterics))
        dataBase64 =base64.b64encode(characterics)
        #print()
        template=dataBase64.decode()
        print(template)
