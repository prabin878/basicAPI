import pandas as pd
from configparser import ConfigParser
import os
import json
import pytest




def get_data(xlpath):
        dat = pd.read_excel(xlpath)
        dat.fillna('',inplace=True)
        li = dat.values.tolist()
        return li

def get_property(key):
	config=ConfigParser()
	config.read(os.path.abspath(os.getcwd())+"/Resources/Config.cfg")
	prop=config.get("Environment",key)
	return prop

def clearLogs():
        logpath=os.path.abspath(os.getcwd())+"/Logs"
        for l in os.listdir(logpath):
                os.remove(os.path.join(logpath,l))

def get_json(struct):
        with open(struct) as json_file:
                json_struct = json.load(json_file)
        return json_struct

def clearReports():
        reportpath=os.path.abspath(os.getcwd())+"/Reports"
        for r in os.listdir(reportpath):
                os.remove(os.path.join(reportpath,r))

def exceptionHandle(status):
        stat = [504,404,501,503]
        for i in stat:
                if status == i:
                        pytest.exit("There could be a Environment or URI issue. Please check")
        
       


