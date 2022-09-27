
# ALARGE MFI KONTROL SISTEMI

# SICAKLIK_SET = 4000
# KESIM_ARALIGI = 4002
# SET_NUMUNE = 4004
# AGIRLIK_SET = 4006
# AGIRLIK_GRAM = 4010
# THERMOCOUPL = 4024
# 16256 set degeri 1

from glob import glob
from numbers import Real
from pickletools import read_floatnl
from pydoc import doc
from tracemalloc import start
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import asyncio
from pymodbus.payload import BinaryPayloadDecoder
from uuid import getnode as get_mac
import struct
import urllib.request

jsonfile = r"alarge-firebase.json"
#firebaseReal = pyrebase.initialize_app(config)
#database = firebaseReal.database()
testReal = {"test":{"a1":"12","a2":"13"}}
cred = credentials.Certificate(jsonfile)
firebase_admin.initialize_app(cred,{'databaseURL': 'https://alarge-79fc5-default-rtdb.europe-west1.firebasedatabase.app/'})
docName = ""
firestoreDb = firestore.client()
fireCollection = firestoreDb.collection("Devices")
readstream = firestoreDb.collection("Devices").stream()

clienthmi = ModbusClient(host="192.168.0.211", port=8000,)

datalar = []
tempData = []
filtreData = []

numberOfSample =0
numberOfCut = 0
timer = []


wifiConnectState = ""
name = "MFI"
status = False
type = "MFI"
macAdress = ""
finishFlag = False
startFlag = False

#REGISTER
START_REGISTER = 4046
SICAKLIK_SET = 4000
KESIM_ARALIGI = 4002
SET_NUMUNE = 4004
AGIRLIK_SET = 4006
AGIRLIK_GRAM = 4010
THERMOCOUPL = 4024
IOT_BAGLANTI_REGISTER = 4146

#read data


def writeFire(dataJson):
    doc_ref = firestoreDb.collection(u'Devices').document(docName)
    print(docName)
    doc_ref.set(dataJson)
  
       

def macAdressDetector():
    global macAdress
    global docName
    test = get_mac()
    macAdress = ":".join(("%012X" % test)[i:i+2]for i in range(0,12, 2))
    docName = macAdress


def wifiStateController():
    global wifiConnectState
    try:
        url = "https://www.google.com"
        urllib.request.urlopen(url)
        wifiConnectState =  "Connected"
        return wifiConnectState
    except:
        wifiConnectState = "Not connected"
        return wifiConnectState
        
        
       


def realTimeSensorAdd(sensorJson):
    try:
        ref = db.reference('/'+docName)
        ref.update(sensorJson)            
    except:
        print("REALTIME SENSOR WRITE ERROR")










def decryptoFunction(temp,tempFloat,interval,intervalFloat,samplesCut,samplesCutFloat,autoWeightSet,autoWeightFloatSet,orifisRes,orifisResFloat):
    try:
        
        orifisResForm = format(orifisRes, 'x')
        orifisResFloatForm = format(orifisResFloat,'x')

        tempForm = format(temp, 'x')
        tempFloatForm = format(tempFloat,'x')
        
        intervalForm = format(interval, 'x')
        intervalFloatForm = format(intervalFloat,'x')            

        samplesCutForm = format(samplesCut, 'x')
        samplesCutFloatForm = format(samplesCutFloat,'x')           

        autoWeightSetForm=format(autoWeightSet,'x')  
        autoWeightFloatSetformatForm=format(autoWeightFloatSet,'x')  


        orifisFin = orifisResForm+orifisResFloatForm
        tempFin = tempForm+tempFloatForm
        intervalFin = intervalFloatForm+intervalForm
        samplesCutFin = samplesCutFloatForm + samplesCutForm
        autoWeightSetFin =  autoWeightFloatSetformatForm +autoWeightSetForm 




        if len(orifisFin) == 8:
            orifisJson = struct.unpack('!f', bytes.fromhex(orifisFin))[0]
        
        if len(orifisFin) < 8:
            cikanOrifis = 8 - len(orifisFin)
            for x in range(cikanOrifis):
                orifisFin = orifisFin+"0"
            orifisJson= struct.unpack('!f', bytes.fromhex(orifisFin))[0]            


        if len(tempFin) == 8:
            tempJson= struct.unpack('!f', bytes.fromhex(tempFin))[0]

        if len(tempFin) < 8:
            cikanTemp = 8 - len(tempFin)
            for x in range(cikanTemp):
                tempFin = tempFin+"0"
            tempJson= struct.unpack('!f', bytes.fromhex(tempFin))[0]

        if len(intervalFin) == 8:
            intervalJson= struct.unpack('!f', bytes.fromhex(tempFin))[0]
        
        if len(intervalFin) < 8:
            cikanInterval = 8-len(intervalFin)
            for x in range(cikanInterval):
                intervalFin = intervalFin+"0"
            intervalJson = struct.unpack('!f', bytes.fromhex(intervalFin))[0]  


        if len(autoWeightSetFin) == 8:
            autoWeightSetJson = struct.unpack('!f', bytes.fromhex(autoWeightSetFin))[0]
        

        if len(autoWeightSetFin) < 8:
            cikanAutoWeightSet = 8-len(autoWeightSetFin)
            for x in range(cikanAutoWeightSet):
                autoWeightSetFin = autoWeightSetFin+"0"
            autoWeightSetJson = struct.unpack('!f', bytes.fromhex(autoWeightSetFin))[0]  
            
            
        if len(samplesCutFin) == 8:
            samplesCutJson = struct.unpack('!f', bytes.fromhex(samplesCutFin))[0]



        if len(samplesCutFin) < 8:
            cikansamplesCut = 8-len(samplesCutFin)
            for x in range(cikansamplesCut):
                samplesCutFin = samplesCutFin+"0"
            samplesCutJson = struct.unpack('!f', bytes.fromhex(samplesCutFin))[0]          
        
            
        return {"Set Temperature":tempJson,"Interval":intervalJson,"Weight":autoWeightSetJson,"Number Of Samples":samplesCutJson,"Current Temperature":orifisJson}
            
           
    except:
        print("HATALI REGISTER")
        
        

def hmiStart():
    global status
    try:
        status = clienthmi.open()
    except:
        status = False
        print("HMI START ERROR")



def hmiDataRead():
    global tempData
    global numberOfSample
    global numberOfCut

    
    try:
        fullArray = clienthmi.read_holding_registers(3999,27)
        temp = fullArray[0]
        tempFloat = fullArray[1]
        
        interval = fullArray[2]
        intervalFloat = fullArray[3]
      
        samplesCut = fullArray[4]
        samplesCutFloat = fullArray[5]
     
        autoWeightSet = fullArray[6]
        autoWeightFloatSet = fullArray[7]
        
        orifisRes = fullArray[25]
         
        orifisResFloat = fullArray[26]
     
        return decryptoFunction(tempFloat,temp,interval,intervalFloat,samplesCut,samplesCutFloat,autoWeightSet,autoWeightFloatSet,orifisRes,orifisResFloat)
       


    except:
        print("REGISTER OKUMA HATA")
        


    





            

      










   

        
