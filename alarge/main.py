import function as func
import asyncio

async def main():
    while True:
        if func.wifiStateController() == "Connected":
            print("WIFI BAGLI")
            func.macAdressDetector()
            func.hmiStart()
            func.fireWriteFunc(True,func.macAdress,"MFI",True,"MFI")
        else:
            print("WIFI BAGLI DEGIL")
        
    
        if func.status and len(func.wifiConnectState) > 2:

            await loop()

        else:
            if func.wifiConnectState:
                 func. fireStateWrite(False)
                

async def loop():
    while True:
        try:
        
            
            sensorVal = func.hmiDataRead()
          
            func.realTimeSensorAdd(sensorVal)
            
        except:
            break


asyncio.run(main())



