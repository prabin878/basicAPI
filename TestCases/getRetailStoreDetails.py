import pytest
import requests
from Resources.fnpayload import *
from Resources.common import *
import os
from requests_toolbelt.utils import dump
import sys
from datetime import datetime


struct = os.path.abspath(os.getcwd())+"\\JsonFiles\\test.json"
xlpath = os.path.abspath(os.getcwd())+"\\DataFiles\\data.xlsx"


URL = get_property("Endpoint")+"/getRetailStoreDetails/v1/AMILGetRetailStoreDetails"
der = {"Authorization": "Bearer "+get_property("token")}

clearLogs()
clearReports()

@pytest.mark.parametrize("storeId,applicationID,applicationUser,status,Testcase",get_data(xlpath))
def getRetailStoreDetails(storeId,applicationID,applicationUser,status,Testcase):
        
        js = json.dumps(get_payload(storeId,applicationID,applicationUser,struct))
        
        res = requests.post(URL,js,headers=der)
        log = dump.dump_all(res)
        dt_str = datetime.now().strftime("%d-%m-%Y %H.%M.%S")
        sys.stdout = open(os.path.abspath(os.getcwd())+"\\Logs\\"+"GetRetailStoreDetails_"+Testcase+"_"+dt_str+".txt","w")
        print(log.decode('utf-8'))
        exceptionHandle(res.status_code)
        
       
        assert res.status_code == status
	
