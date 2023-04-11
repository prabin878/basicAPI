import pytest
import requests
import os
from Resources.common import *
from requests_toolbelt.utils import dump
import sys
import time
from datetime import datetime
from pytz import timezone
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import  ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider





struct = os.path.abspath(os.getcwd())+"/JsonFiles/checkeligibility.json"
xlpath = os.path.abspath(os.getcwd())+"/DataFiles/scfdata.xlsx"

URL = "https://check-eligibility-qat1.px-npe1101.pks.t-mobile.com/scee/v1/eligible-criteria/eligible-ban"
der = {"Content-Type": "application/json"}

clearLogs()
clearReports()


@pytest.fixture(scope="module")
def dbsetup():
        print("setting up DB Connection")
        auth_provider = PlainTextAuthProvider(username='qat_scee_rw', password='wMeHHVSASm77z33R')
        profile = ExecutionProfile(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
        cluster = Cluster(contact_points=['10.130.169.197','10.130.169.195','10.130.169.193'],control_connection_timeout=10,port=9042,auth_provider=auth_provider, protocol_version=4,execution_profiles={EXEC_PROFILE_DEFAULT: profile})

        # trying to connect to DB maximum 4 attempts
        for i in range(4):
                try:
                        session = cluster.connect('ebcis_scee_ks_qat')
                except Exception as e:
                        if i == 3:
                                print(e)
                                pytest.exit("Something wrong with DB connection. Please check")
                else:
                        break
                        
                                
        yield session,cluster
        session.shutdown()
        cluster.shutdown()
        
        
@pytest.mark.parametrize("banId,Eligible,status,Testcase",get_data(xlpath))
def test_checkEligibility(banId,Eligible,status,Testcase,dbsetup):

        # providing banId to the Request body
        json_data=get_json(struct)
        json_data["sourceBAN"] = banId
        js = json.dumps(json_data)
        

        # capturing time in PST to use in CQL query
        date = datetime.now().astimezone(timezone("US/Pacific"))
        now = date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Running the check eligibility service
        res = requests.post(URL,js,headers=der,verify=False)
        
        # capturing date for naming the log files
        dt_str = datetime.now().strftime("%d-%m-%Y")

        # handling exception of any downtime of service
        exceptionHandle(res.status_code)

        assert res.status_code == status
        
        
        log = dump.dump_all(res)
        
        sys.stdout = open(os.path.abspath(os.getcwd())+"/Logs/CheckEligibility_"+Testcase+"_"+dt_str+".txt","w")
        print(log.decode('utf-8'))
        
        
        # preparing CQL query
        query1 = "select * from eligibility_check_trx_log where ban_id="+str(banId)+" and create_dttm >= '"+now+"' allow filtering;"
        query2 = "select * from account_eligibility where ban_id="+str(banId)+" allow filtering;"
        print("**********Queries used to validate Cassandra DB records are below********")
        print(query1)
        print(query2)
        
        # refreshing the tables to reflect the new record immediately 
        dbsetup[1].refresh_table_metadata('ebcis_scee_ks_qat','eligibility_check_trx_log')
        time.sleep(3)
        
        # Executing CQL queries
        rows = dbsetup[0].execute(query1)
        rows1 = dbsetup[0].execute(query2)

        # Cassandra DB record validations
        print("****************Eligibility Trx Record***************")
        if len(rows.current_rows) == 0:
            pytest.fail("Record not found in trx table. Please check the ban data or there could be an issue with other Microservices")
        for user_row in rows:
                print(user_row.ban_id,"|",user_row.eligible,"|",user_row.create_by,"|",user_row.rule_set,"|",user_row.failure_rule,"|",user_row.create_dttm)
                assert user_row.eligible == Eligible      
        print("****************Account Eligibility  Record***************") 
        if len(rows1.current_rows) == 0:
            pytest.fail("Record not found in account eligibility table. Please check the ban data or there could be an issue with other Microservices")
        for user_row1 in rows1:
                print (user_row1.conversion_id,"|",user_row1.ban_id,"|",user_row1.elig_eval_info,"|",user_row1.eligible,"|",user_row1.last_elig_check_by,"|",user_row1.last_elig_check_dttm)
                assert user_row1.eligible == Eligible
           
        
                
            
        
        
        
        
       
        

        









