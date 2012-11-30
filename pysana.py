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
        current = self.projects_list()
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
        post_data = {'name': project_name, 'id': workspace_id}
        if project_notes:
            post_data['notes'] = project_notes
        else:
            post_data['notes'] = ''
        return self.post_data(url, post_data)

    def project_change_details(self, project_id, project_name=None, project_notes=None):
        url = self.api_url + '/projects/' + str(project_id)
        put_data = {}
        if project_name:
            put_data['name'] = project_name
        if project_notes:
            put_data['notes'] = project_notes
        return self.post_data(url, put_data)

    #Stories
    def story_details(self, story_id):
        url = self.api_url + '/stories/' + str(story_id)
        return self.get_data(url)
    
    def stories_for_task(self, task_id):
        url = self.api_url + '/tasks/' + str(task_id) + '/stories'
        return self.get_data(url)

    def stories_for_project(self, project_id):
        url = self.api_url + '/projects/' + str(project_id) + '/stories'
        return self.get_data(url)

    #Tags
    def tag_details(self, tag_id):
        url = self.api_url + '/tags/' + str(tag_id)
        return self.get_data(url)

    def tag_create(self, tag_data, workspace_id=None):
        """
        tag_data: a dictionary of the information for the new tag.
        """
        if workspace_id:
            url = self.api_url + '/workspaces/' + str(workspace_id) + '/tags'
        else:
            url = self.api_url + '/tags'
        return self.post_data(url, tag_data)

    def tags_in_workspace(self, workspace_id):
        url = self.api_url + '/workspaces/' + str(workspace_id) + '/tags'
        return self.get_data(url)
    
    def tag_tasks(self, tag_id):
        url = self.api_url + '/tags/' + str(tag_id) + '/tasks'
        return self.get_data(url)

    def tag_update(self, tag_id, update_dict):
        url = self.api_url + '/tags/' + str(tag_id)
        return self.post_data(url, update_dict)

    def tags(self):
        url = self.api_url + '/tags'
        return self.get_data(url)

    #Tasks
    def task_create(self, workspace_id):
        """
        Create new task
        workspace_id: the id of the workspace the task will be attached to.
        """
        url = self.api_url + '/workspaces/' + str(workspace_id) + '/tasks'
                
        return self.get_data(url)

    def task_details(self, task_id):
        url = self.api_url + '/tasks/' + str(task_id)
        return self.get_data(url)

    def tasks_in_project(self, project_id):
        url = self.api_url + '/projects/' + str(project_id) + '/tasks'
        return self.get_data(url)
    
    def tasks_in_worskapce(self, workspace_id):
        url = self.api_url + '/workspaces/' + str(workspace_id) + '/tasks'
        return self.get_data(url)

    def tasks(self):
        url = self.api_url + '/tasks'
        return self.get_data(url)

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
        url = self.api_url + '/workspaces/' + str(workspace_id)
        return self.get_data(url)

    def workspace_name(self, workspace_id, workspace_name):
        url = self.api_url + '/workspaces/' + str(workspace_id)
        put_data = {'name': workspace_name}
        return self.put_data(url, put_data)

    # Utility methods
    def get_data(self, url):
        """
        Users are responsible for handling what happens when
        an error is received. The JSON returned will have the
        following format:

        {"errors":[{"message":"Request data must be a JSON object, not null"}]}
        or 
        {"errors":[{"message":"No matching route for request"}]}

        Pysana will return the errors dict or the data dict.
        """
        get_request = requests.get(url, auth=(self.key, ''))
        j = json.loads(get_request.text)
        if 'errors' in j:
            return j
        else:
            return j['data']

    def post_data(self, url, post_data):
        post_request = requests.post(url, auth=(self.key, ''), data=(post_data))
        j = json.loads(post_request.text)
        if 'errors' in j:
            return j
        else:
            return j['data']

    def put_data(self, url, put_data):
        put_request = requests.put(url, auth=(self.key, ''), data=(put_data))
        j = json.loads(put_request.text)
        if 'errors' in j:
            return j
        else:
            return j['data']
