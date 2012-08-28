#! /usr/bin/python
import requests
import json
# My API Key: oHKGELa.71Xsjl1PalAaX2cydWcke1DP

#use example -> import padmasana


class API(object):
    def __init__(self, key):
        self.key = key
        self.url = 'https://app.asana.com/api'
        self.api_version = '1.0'
        self.api_url = self.url + "/" + self.api_version

    def create_basic_auth(self):
        '''Creates the basic auth credential to be passed.
        Asana specifies that the username should be the api
        key and the password should be blank separated by a
        colon. Thus, 'apikey:' is used and then encoded in
        base64.'''

        encode_me = self.key + ':'
        return encode_me.encode('base64').rstrip()

    # Listing Methods
    # The following methods perform all listing related functions. They all
    # return json so it can be used and abused accordingly.
    def projects(self):
        url = self.api_url + '/projects'
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def project_tasks(self, project_id):
        url = self.api_url + '/project/' + project_id + '/tasks'
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def project_details(self, project_id):
        url = self.api_url + '/project/' + project_id
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def workspaces(self):
        url = self.api_url + '/workspaces'
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def workspace_details(self, workspace_id):
        url = self.api_url + '/workspace/' + workspace_id
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data
