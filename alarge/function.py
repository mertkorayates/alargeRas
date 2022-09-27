
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
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin.firestore import SERVER_TIMESTAMP
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
doc_ref = firestoreDb.collection('Devices')

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

startStateList = [False,False]
kontrolFireStart = True

samplesCutJson = 0
kesilenDenemeSayiJson =1

deviceState = False
tempArray = []
weightArray = []
intervalGlobal = 0
numberOfSamplesGlobal = 0
setTempGlobal = 0
weightGlobal = 0
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







fireStoreActive = True

def decryptoFunction(temp,tempFloat,interval,intervalFloat,samplesCut,samplesCutFloat,autoWeightSet,autoWeightFloatSet,orifisRes,orifisResFloat,startStateReg,agirlikOne,agirkikOneFloat,agirlikTwo, agirkikTwoFloat,agirlikOThree,agirlikOThreeFloat,agirlikFor,agirkikForFloat,agirlikFive,agirkikFiveFloat,agirlikSix,agirkikSixFloat,agirlikSeven,agirkikSevenFloat,agirlikEight,agirkikEightFloat,agirlikNine,agirkikNineFloat,agirlikTen,agirkikTenFloat,kesilenDenemeSayi):
    try:
        global startStateList
        global fireStoreActive
        global kontrolFireStart
        global samplesCutJson
        global kesilenDenemeSayiJson
        global deviceState
        global tempArray
        global weightArray
        global intervalGlobal
        global numberOfSamplesGlobal
        global setTempGlobal
        global weightGlobal

        kesilenDenemeSayiForm = format(kesilenDenemeSayi, 'x');
       
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

        agirlikOneForm =  format(agirlikOne,'x')  
        agirlikOneFloatForm =  format(agirkikOneFloat,'x')  

        agirlikTwoForm = format(agirlikTwo,'x')  
        agirlikTwoFloatForm = format(agirkikTwoFloat,'x')  
       
        agirlikOThreeForm = format(agirlikOThree,'x')  
        agirlikOThreeFloatForm = format(agirlikOThreeFloat,'x')  


    
        agirlikForForm = format(agirlikFor,'x')  
        agirlikForFloatForm = format(agirkikForFloat,'x')  

        agirlikFiveForm = format(agirlikFive,'x')  
        agirlikFiveFloatForm = format(agirkikFiveFloat,'x')  

        agirlikSixForm = format(agirlikSix,'x')  
        agirlikSixFloatForm = format(agirkikSixFloat,'x')  

        agirlikSevenForm = format(agirlikSeven,'x')  
        agirlikSevenFloatForm = format(agirkikSevenFloat,'x')

        agirlikEightForm = format(agirlikEight,'x')  
        agirlikEightFloatForm = format(agirkikEightFloat,'x')


        
        agirlikNineForm = format(agirlikNine,'x')  
        agirlikNineFloatForm = format(agirkikNineFloat,'x')
        
        agirlikTenForm = format(agirlikTen,'x')  
        agirlikTenFloatForm = format(agirkikTenFloat,'x')



        orifisFin = orifisResForm+orifisResFloatForm
        tempFin = tempForm+tempFloatForm
        intervalFin = intervalFloatForm+intervalForm
        samplesCutFin = samplesCutFloatForm + samplesCutForm
        autoWeightSetFin =  autoWeightFloatSetformatForm +autoWeightSetForm 
        startStateFin = startStateReg
        agirlikOneFin = agirlikOneFloatForm+ agirlikOneForm 

        agirlikTwoFin = agirlikTwoFloatForm + agirlikTwoForm  
        agirlikThreeFin =  agirlikOThreeFloatForm +agirlikOThreeForm
        agirlikForFin = agirlikForFloatForm + agirlikForForm
        agirlikFiveFin = agirlikFiveFloatForm +agirlikFiveForm 
        agirlikSixFin = agirlikSixFloatForm+ agirlikSixForm  
        agirlikSevenFin = agirlikSevenFloatForm + agirlikSevenForm  
        agirlikEightFin = agirlikEightFloatForm + agirlikEightForm
        agirlikNineFin = agirlikNineFloatForm + agirlikNineForm  
        agirlikTenFin = agirlikTenFloatForm + agirlikTenForm  

      

        deviceState = True


        if len(kesilenDenemeSayiForm) == 8:
            kesilenDenemeSayiJson = struct.unpack('!f', bytes.fromhex(kesilenDenemeSayiForm))[0]


        if len(kesilenDenemeSayiForm) < 8:
            kesilenDenemeSayiFormCut = 8 - len(kesilenDenemeSayiForm)
            for x in range(kesilenDenemeSayiFormCut):
                kesilenDenemeSayiForm = kesilenDenemeSayiForm+"0"
            kesilenDenemeSayiJson= struct.unpack('!f', bytes.fromhex(kesilenDenemeSayiForm))[0]

                     


        

   




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

       






        if samplesCutJson == kesilenDenemeSayiJson and kontrolFireStart:
            fireTestAdd(intervalGlobal,numberOfSamplesGlobal,setTempGlobal,"13:40",tempArray,weightArray,weightGlobal)


            print("s")
                
               


        if startStateFin == 16256:
                
            kontrolFireStart = True

            if len(agirlikOneFin) == 8:
                agirlikOneJson = struct.unpack('!f', bytes.fromhex(agirlikOneFin))[0]

            if len(agirlikOneFin) < 8:
                agirlikOneCut = 8-len(agirlikOneFin)
                for x in range(agirlikOneCut):
                    
                    agirlikOneFin = agirlikOneFin+"0"
                agirlikOneJson = struct.unpack('!f', bytes.fromhex(agirlikOneFin))[0]      

            #if startStateFin == 16256:
                
            if len(agirlikTwoFin) == 8:

                agirlikTwoJson = struct.unpack('!f', bytes.fromhex(agirlikTwoFin))[0]



            if len(agirlikTwoFin) < 8:
                    
                agirlikTwoCut = 8-len(agirlikTwoFin)
                for x in range(agirlikTwoCut):
                    agirlikTwoFin = agirlikTwoFin+"0"
                agirlikTwoJson = struct.unpack('!f', bytes.fromhex(agirlikTwoFin))[0]      
            



                
            if len(agirlikThreeFin) == 8:
                agirlikThreeJson = struct.unpack('!f', bytes.fromhex(agirlikThreeFin))[0]



            if len(agirlikThreeFin) < 8:
                agirlikThreeCut = 8-len(agirlikThreeFin)
                for x in range(agirlikThreeCut):
                    agirlikThreeFin = agirlikThreeFin+"0"
                agirlikThreeJson = struct.unpack('!f', bytes.fromhex(agirlikThreeFin))[0]      
            



                
            if len(agirlikForFin) == 8:
                agirlikForJson = struct.unpack('!f', bytes.fromhex(agirlikForFin))[0]



            if len(agirlikForFin) < 8:
                agirlikForCut = 8-len(agirlikForFin)
                for x in range(agirlikForCut):
                    agirlikForFin = agirlikForFin+"0"
                agirlikForJson = struct.unpack('!f', bytes.fromhex(agirlikForFin))[0]      
            


                
            if len(agirlikFiveFin) == 8:
                agirlikFiveJson = struct.unpack('!f', bytes.fromhex(agirlikFiveFin))[0]



            if len(agirlikFiveFin) < 8:
                agirlikFiveCut = 8-len(agirlikFiveFin)
                for x in range(agirlikFiveCut):
                    agirlikFiveFin = agirlikFiveFin+"0"
                agirlikFiveJson = struct.unpack('!f', bytes.fromhex(agirlikFiveFin))[0]      
            

                
            if len(agirlikSixFin) == 8:
                agirlikSixJson = struct.unpack('!f', bytes.fromhex(agirlikSixFin))[0]



            if len(agirlikSixFin) < 8:
                agirlikSixCut = 8-len(agirlikSixFin)
                for x in range(agirlikSixCut):
                    agirlikSixFin = agirlikSixFin+"0"
                agirlikSixJson = struct.unpack('!f', bytes.fromhex(agirlikSixFin))[0]      
            

            if len(agirlikSevenFin) == 8:
                agirlikSevenJson = struct.unpack('!f', bytes.fromhex(agirlikSevenFin))[0]



            if len(agirlikSevenFin) < 8:
                agirlikSevenCut = 8-len(agirlikSevenFin)
                for x in range(agirlikSevenCut):
                    agirlikSevenFin = agirlikSevenFin+"0"
                agirlikSevenJson = struct.unpack('!f', bytes.fromhex(agirlikSevenFin))[0]   

            if len(agirlikEightFin) == 8:
                agirlikEightJson = struct.unpack('!f', bytes.fromhex(agirlikEightFin))[0]



            if len(agirlikEightFin) < 8:
                agirlikEightCut = 8-len(agirlikEightFin)
                for x in range(agirlikEightCut):
                    agirlikEightFin = agirlikEightFin+"0"
                agirlikEightJson = struct.unpack('!f', bytes.fromhex(agirlikEightFin))[0]   

            if len(agirlikNineFin) == 8:
                agirlikNineJson = struct.unpack('!f', bytes.fromhex(agirlikNineFin))[0]



            if len(agirlikNineFin) < 8:
                agirlikNineCut = 8-len(agirlikNineFin)
                for x in range(agirlikNineCut):
                    agirlikNineFin = agirlikNineFin+"0"
                agirlikNineJson = struct.unpack('!f', bytes.fromhex(agirlikNineFin))[0]   

            if len(agirlikTenFin) == 8:
                agirlikTenJson = struct.unpack('!f', bytes.fromhex(agirlikTenFin))[0]



            if len(agirlikTenFin) < 8:
                agirlikTenCut = 8-len(agirlikTenFin)
                for x in range(agirlikTenCut):
                    agirlikTenFin = agirlikTenFin+"0"
                agirlikTenJson = struct.unpack('!f', bytes.fromhex(agirlikTenFin))[0]   


            tempArray.append(orifisJson)
            weightArray = [agirlikOneJson,agirlikTwoJson,agirlikThreeJson,agirlikForJson,agirlikFiveJson,agirlikSixJson,agirlikSevenJson,agirlikEightJson,agirlikNineJson,agirlikTenJson]
            intervalGlobal = intervalJson
            numberOfSamplesGlobal = samplesCutJson
            setTempGlobal = tempJson
            weightGlobal = autoWeightSetJson
            fireStateWrite(True)
           


                

            
               
            return {"Set Temperature":tempJson,"Interval":intervalJson,"Weight":autoWeightSetJson,"Number Of Samples":samplesCutJson,"Current Temperature":orifisJson,"Weighing":[agirlikOneJson,agirlikTwoJson,agirlikThreeJson,agirlikForJson,agirlikFiveJson,agirlikSixJson,agirlikSevenJson,agirlikEightJson,agirlikNineJson,agirlikTenJson],"isActive":True}    

        else:
            kontrolFireStart = False
            fireStateWrite(False)
           
            return {"Set Temperature":tempJson,"Interval":intervalJson,"Weight":autoWeightSetJson,"Number Of Samples":samplesCutJson,"Current Temperature":orifisJson,"Weighing":[0.0],"isActive":True}
            
            
           
    except:
        deviceState = False
        fireStateWrite(False)
        print("HATALI REGISTER")
        
        

def hmiStart():
    global status
    try:
        status = clienthmi.open()
    except:
        status = False
        print("HMI START ERROR")


def fireWriteFunc(connectionState,macAdressID,deviceName,statusDevice,typeDevice):


    doc_ref.document(macAdress).set({
        "Connection State":connectionState,
        "ID":macAdressID,
        "Name": deviceName,
        "Status" : statusDevice,
        "Type" : typeDevice
        })
    


def fireReadFunc():
    print(macAdress)
    docs = doc_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')


def fireStateWrite(deviceState):
    doc_ref.document(macAdress).update({
        "Status": deviceState
    })


def fireTestAdd(interval,numberOfSample,setTemperature,timeStampDate,tempArray,weightArray,weight):

    doc_ref.document(macAdress).collection("tests").document().set({
        "Interval":interval,
        "Material":"",
        "Name":"",
        "Number Of Samples" : numberOfSample,
        "Operator":"",
        "Set Temperature": setTemperature,
        "Start Date" : SERVER_TIMESTAMP,
        "Temperature": tempArray,
        "Weighing" : weightArray,
        "Weight" : weight

    })


def hmiDataRead():
    global tempData
    global numberOfSample
    global numberOfCut

    
    try:
       
        fullArray = clienthmi.read_holding_registers(3999,115)
        temp = fullArray[0]
        tempFloat = fullArray[1]
        
        interval = fullArray[2]
        intervalFloat = fullArray[3]
        

        
        samplesCut = fullArray[4]
        samplesCutFloat = fullArray[5]
     
        autoWeightSet = fullArray[6]
        autoWeightFloatSet = fullArray[7]

        kesilenDenemeSayi = fullArray[15]
        
        orifisRes = fullArray[25]
         
        orifisResFloat = fullArray[26]
        startStateReg = fullArray[47]
        
        agirlikOne = fullArray[90]
        agirkikOneFloat = fullArray[91]

        agirlikTwo = fullArray[92]
        agirkikTwoFloat = fullArray[93]

        agirlikOThree = fullArray[94]
        agirlikOThreeFloat = fullArray[95]

        agirlikFor = fullArray[96]
        agirkikForFloat = fullArray[97]

        agirlikFive = fullArray[98]
        agirkikFiveFloat = fullArray[99]

        agirlikSix = fullArray[100]
        agirkikSixFloat = fullArray[101]

        agirlikSeven = fullArray[102]
        agirkikSevenFloat = fullArray[103]

        agirlikEight = fullArray[104]
        agirkikEightFloat = fullArray[105]

        agirlikNine = fullArray[106]
        agirkikNineFloat = fullArray[107]

        agirlikTen = fullArray[108]
        agirkikTenFloat = fullArray[109]


        return decryptoFunction(tempFloat,temp,interval,intervalFloat,samplesCut,samplesCutFloat,autoWeightSet,autoWeightFloatSet,orifisRes,orifisResFloat,startStateReg,agirlikOne,agirkikOneFloat,agirlikTwo, agirkikTwoFloat,agirlikOThree,agirlikOThreeFloat,agirlikFor,agirkikForFloat,agirlikFive,agirkikFiveFloat,agirlikSix,agirkikSixFloat,agirlikSeven,agirkikSevenFloat,agirlikEight,agirkikEightFloat,agirlikNine,agirkikNineFloat,agirlikTen,agirkikTenFloat,kesilenDenemeSayi)
       


    except:
        print("REGISTER OKUMA HATA")
        fireStateWrite(False)
        


    





            

      










   

        
