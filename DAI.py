import time, random, requests
import datetime as date
import DAN

ServerURL = 'http://iot.iottalk.tw:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'WaterWall_timer_01'  #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Orchidhouse_control'
DAN.profile['df_list']=['SState_I4']
DAN.profile['d_name']= 'WaterWall_timer_01' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

#Var
StartTime = date.time(hour=8, minute=0, second=0)
EndTime = date.time(hour=17, minute=0, second=0)
Intraval = date.timedelta(minutes=30)

def Push_Activate():
    try:
        IDF_data = 1
        DAN.push ('SState_I4', IDF_data)
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    #start few second
    time.sleep(120)
    IDF_data = 0
    DAN.push ('SState_I4', IDF_data)

Past_time = date.datetime.now()

while True:
    #add a datetime control code
    Now_time = date.datetime.now()
    if StartTime <= Now_time.time() <= EndTime:
        Past_time_ = Past_time + Intraval
        if Past_time_ < Now_time:
            print('Active Water Wall',end=' ')
            print(Now_time)
            Push_Activate()
            Past_time = Now_time
        
    time.sleep(60)

