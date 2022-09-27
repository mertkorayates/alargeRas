import function as func
import asyncio

async def main():
    
    if func.wifiStateController() == "Connected":
        print("WIFI BAGLI")
        func.macAdressDetector()
        func.writeFire({"Connection State " : "Baaglandı"})
        func.hmiStart()
    else:
        print("WIFI BAGLI DEGIL")
        
    
    if func.status and len(func.wifiConnectState) > 2:

        await loop()

    else:
        if func.wifiConnectState:
            print("ELSSEE")
                







async def loop():
    while True:
        try:
        
            
            sensorVal = func.hmiDataRead()
          
            func.realTimeSensorAdd(sensorVal)
            
        except:
            break


asyncio.run(main())
