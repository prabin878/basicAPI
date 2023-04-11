import json
from Resources.common import *



def get_payload(storeId,applicationID,applicationUser,struct):
	json_data=get_json(struct)
		
	if storeId == "none":
		json_data["getRetailStoreDetailsRequest"]["storeId"] = None
	elif storeId == "omitted":
		json_data["getRetailStoreDetailsRequest"].pop("storeId")
	else:
		json_data["getRetailStoreDetailsRequest"]["storeId"] = str(storeId)

	if applicationID== "none":
		json_data["getRetailStoreDetailsRequest"]["applicationDataInfo"]["applicationID"] = None
	elif applicationID == "omitted":
		json_data["getRetailStoreDetailsRequest"]["applicationDataInfo"].pop("applicationID")
	else:
		json_data["getRetailStoreDetailsRequest"]["applicationDataInfo"]["applicationID"] = applicationID

	
	if applicationUser== "none":
		json_data["getRetailStoreDetailsRequest"]["applicationDataInfo"]["applicationUser"] = None
	elif applicationUser == "omitted":
		json_data["getRetailStoreDetailsRequest"]["applicationDataInfo"].pop("applicationUser")
	else:
		json_data["getRetailStoreDetailsRequest"]["applicationDataInfo"]["applicationUser"] = applicationUser
	
	return json_data
