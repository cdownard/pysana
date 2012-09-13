#! /usr/bin/python
import requests
import json


class API(object):
    def __init__(self, key):
        """
        workspaces and projects are arrays of dicts.
        The workspaces array stores in the following way:
        {
            'id': 12345869,
            'name': 'workspace_name'
        }
        Please note that the ID is not a string. Asana's docs do not reflect
        that the ID may contain characters, however it is possible in the tests
        that have been run. If a string representation of the ID field is
        passed back to the Asana API, an error will occur and the resposne will
        say that the workspace does not exist.
        """
        self.key = key
        self.url = 'https://app.asana.com/api'
        self.api_version = '1.0'
        self.api_url = self.url + "/" + self.api_version
        self.workspaces = []
        self.projects = []

    def create_basic_auth(self):
        '''Creates the basic auth credential to be passed.
        Asana specifies that the username should be the api
        key and the password should be blank separated by a
        colon. Thus, 'apikey:' is used and then encoded in
        base64.'''

        encode_me = self.key + ':'
        return encode_me.encode('base64').rstrip()

    # Self Maintenance
    def update_workspaces(self):
        current = self.workspaces()
        for w in current:
            if w not in self.workspaces:
                self.workspaces.append(w)

    def update_projects(self):
        current = self.projects()
        for p in current:
            if p not in self.projects:
                self.projects.append(p)

    ############
    # Projects #
    ############
    def projects(self):
        url = self.api_url + '/projects'
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def project_tasks(self, project_id):
        url = self.api_url + '/project/' + str(project_id) + '/tasks'
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def project_details(self, project_id):
        url = self.api_url + '/project/' + str(project_id)
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def new_project(self, workspace_id, project_name, project_notes=None):
        url = self.api_url + '/workspaces/' + str(workspace_id) + '/projects'
        put_data = {'name': project_name, 'id': workspace_id}
        if project_notes:
            put_data['notes'] = project_notes
        else:
            put_data['notes'] = ''
        post_request = requests.post(url, auth=(self.key, ''), data=(put_data))
        json_data = json.loads(post_request.text)['data']
        return json_data

    ##############
    # Workspaces #
    ##############
    def workspaces(self):
        url = self.api_url + '/workspaces'
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def workspace_details(self, workspace_id):
        url = self.api_url + '/workspace/' + str(workspace_id)
        get_request = requests.get(url, auth=(self.key, ''))
        json_data = json.loads(get_request.text)['data']
        return json_data

    def workspace_name(self, workspace_id, workspace_name):
        url = self.api_url + '/workspace/' + str(workspace_id)
        put_data = {'name': workspace_name}
        post_request = requests.post(url, auth=(self.key, ''), data=(put_data))
        json_data = json.loads(post_request.text)['data']
        return json_data
