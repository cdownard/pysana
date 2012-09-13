#! /usr/bin/python
import requests
import json


class API(object):
    def __init__(self, key):
        """
        workspaces, projects, and users are arrays of dicts.
        The workspaces array stores in the following way:
        {
            'id': 12345869,
            'name': 'workspace_name'
        }
        Please note that the ID is not a string. Asana's docs do not reflect
        that the ID may contain characters, however it is possible in the tests
        that have been run. If a string representation of the ID field is
        passed back to the Asana API, an error will occur and the response will
        say that the workspace does not exist. Instead, pysana handles the
        string conversion. Python will read the ID as a Long.
        """
        self.key = key
        self.url = 'https://app.asana.com/api'
        self.api_version = '1.0'
        self.api_url = self.url + "/" + self.api_version
        self.workspaces = []
        self.projects = []
        self.users = []

    # Self Maintenance
    def update_workspaces(self):
        current = self.workspaces_list()
        for workspace in current:
            if workspace not in self.workspaces:
                self.workspaces.append(workspace)

    def update_projects(self):
        current = self.project_list()
        for project in current:
            if project not in self.projects:
                self.projects.append(project)

    def update_users(self):
        current = self.users_list()
        for user in current:
            if user not in self.users:
                self.users.append(user)

    # Projects
    def projects_list(self, workspace_id=None):
        url = self.api_url
        if workspace_id:
            url += '/workspaces/' + str(workspace_id) + '/projects'
        else:
            url += '/projects'
        return self.get_data(url)

    def project_tasks(self, project_id):
        url = self.api_url + '/projects/' + str(project_id) + '/tasks'
        return self.get_data(url)

    def project_details(self, project_id):
        url = self.api_url + '/projects/' + str(project_id)
        return self.get_data(url)

    def new_project(self, workspace_id, project_name, project_notes=None):
        url = self.api_url + '/workspaces/' + str(workspace_id) + '/projects'
        put_data = {'name': project_name, 'id': workspace_id}
        if project_notes:
            put_data['notes'] = project_notes
        else:
            put_data['notes'] = ''
        return self.post_data(url, put_data)

    def project_change_details(self, project_id, project_name=None, project_notes=None):
        url = self.api_url + '/projects/' + str(project_id)
        put_data = {}
        if project_name:
            put_data['name'] = project_name
        if project_notes:
            put_data['notes'] = project_notes
        return self.post_data(url, put_data)

    # Users
    def users_list(self):
        """
        This method return all users in all workspaces. It does not return what
        work space the user belongs to.
        """
        url = self.api_url + '/users'
        return self.get_data(url)

    def users_in_workspace(self, workspace_id):
        """
        Returns list of users in a specific workspace. Use the workspace id
        from the workspace field (the key is 'id'). Alternatively, the id
        may be provided manually.
        """
        url = self.api_url + '/workspaces/' + str(workspace_id) + '/users'
        return self.get_data(url)

    def user_details(self, user_id):
        """
        Returns the details on a given user including member workspaces.
        """
        url = self.api_url + '/users/' + str(user_id)
        return self.get_data(url)

    # Workspaces
    def workspaces_list(self):
        url = self.api_url + '/workspaces'
        return self.get_data(url)

    def workspace_details(self, workspace_id):
        url = self.api_url + '/workspace/' + str(workspace_id)
        return self.get_data(url)

    def workspace_name(self, workspace_id, workspace_name):
        url = self.api_url + '/workspace/' + str(workspace_id)
        put_data = {'name': workspace_name}
        return self.post_data(url, put_data)

    # Utility methods
    def get_data(self, url):
        get_request = requests.get(url, auth=(self.key, ''))
        return json.loads(get_request.text)['data']

    def post_data(self, url, put_data):
        post_request = requests.post(url, auth=(self.key, ''), data=(put_data))
        return json.loads(post_request.text)['data']
