import requests

from thehive4py.api import TheHiveApi

from thehive4py.models import *

from thehive4py.query import *

import configparser

import json


global config

global thehive_api

config = configparser.ConfigParser()

config.read('config.ini')

thehive_api = TheHiveApi(config['thehive']['url'], config['thehive']['api_key'])


class HarfangLabApi:

    def __init__(self, url, token):

        self.url = url

        self.api_url = self.url + "/api"

        self.headers = {"Accept" : "application/json", "Authorization" : "Token " + token}


    def get_aggregation_alerts(self, limit = 10):

        return requests.get(self.api_url + "/data/alert/alert/AggregationAlert/", headers = self.headers, params = {"limit": limit})

    

    def set_false_positive(self,id_alert):

        try:

            if self.get_alert_status(id_alert)=="new":

                return requests.post(self.api_url+"/data/alert/alert/AggregationAlert/tag/", headers=self.headers, data={"ids":[id_alert],"new_status":"false_positive","tag_alerts":True,"new
_comment":""})

        except:

            pass

        return 0


    def set_closed(self,id_alert):

        try:

            if self.get_alert_status(id_alert)=="new":

                return requests.post(self.api_url+"/data/alert/alert/AggregationAlert/tag/", headers=self.headers, data={"ids":[id_alert],"new_status":"closed","tag_alerts":True,"new_comment
":""})

        except:

            pass

        return 0


def set_alert_status_thehive_false_positive(id_alert_thehive):

    tags = thehive_api.get_alert(id_alert_thehive).json()["tags"]

    tags.append("status:false_positive")

    tags = [i for i in tags if i !="status:new"]

    params = json.dumps({"tags":tags})

    print(params)

    return requests.patch(config['thehive']['url']+f"/api/alert/{id_alert_thehive}",headers={'content-type':'application/json',"Authorization":f"Bearer {config['thehive']['api_key']}"},data=
params)


def set_alert_status_thehive_closed(id_alert_thehive):

    tags = thehive_api.get_alert(id_alert_thehive).json()["tags"]

    if not "status:closed" in tags:

        tags.append("status:closed")

    tags = [i for i in tags if i !="status:new"]

    params = json.dumps({"tags":tags})

    print(params)

    return requests.patch(config['thehive']['url']+f"/api/alert/{id_alert_thehive}",headers={'content-type':'application/json',"Authorization":f"Bearer {config['thehive']['api_key']}"},data=
params)


def get_reference_by_alert_id(alert_id):

    thehive_alerts_array = thehive_api.get_alert(alert_id).json()

    return thehive_alerts_array["sourceRef"]


def get_alert_tenant_by_id(id_alert):

    alert = thehive_api.get_alert(id_alert).json()

    return alert["source"]


def set_status_from_responder_false_positive(group_name):

    id_alert = group_name.split(" # ")[1]

    set_alert_status_thehive_false_positive(id_alert)

    id_harfang = get_reference_by_alert_id(id_alert)

    tenant = "harfanglab_"+get_alert_tenant_by_id(id_alert)

    url_harfang = config[tenant]["url"]

    api_key = config[tenant]["api_key"]

    api_harfang = HarfangLabApi(url_harfang,api_key)

    api_harfang.set_false_positive(id_harfang)


def set_status_from_responder_closed(group_name):

    id_alert = group_name.split(" # ")[1]

    set_alert_status_thehive_closed(id_alert)

    id_harfang = get_reference_by_alert_id(id_alert)

    tenant = "harfanglab_"+get_alert_tenant_by_id(id_alert)

    url_harfang = config[tenant]["url"]

    api_key = config[tenant]["api_key"]

    api_harfang = HarfangLabApi(url_harfang,api_key)

    api_harfang.set_closed(id_harfang)



# Pour passer une alerte thehive et son alerte associée harfang en false positive : set_status_from_responder_false_positive(<nom du groupe de la task>)

# Pour passer une alerte thehive et son alerte associée harfang en closed         : set_status_from_responder_closed(<nom du groupe de la task>)
