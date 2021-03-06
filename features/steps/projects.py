from behave import *
import pysana

key = 'oHKGELa.71Xsjl1PalAaX2cydWcke1DP'
test_project_id = "1483293500928"


# Get All Projects
@given(u'there are currently projects')
def step(context):
    context.api = pysana.API(key)

@when(u'we request the list of projects')
def step(context):
    context.projects_list = context.api.projects_list()

@then(u'we will see the current list of projects')
def step(context):
    assert context.projects_list

###############################################################################

# Get All Projects From Workspace
@given(u'a workspace id to get its projects')
def step(context):
    context.api = pysana.API(key)
    context.workspaces = context.api.update_workspaces()

@when(u'we request the list of projects in that workspace id')
def step(context):
    context.projects = context.api.projects_list(context.api.workspaces[0]['id'])

@then(u"we will see the current list of projects for that workspace")
def step(context):
    assert context.projects

###############################################################################

# Create New Project
@given(u'a workspace id for a new project')
def step(context):
    context.api = pysana.API(key)
    context.workspaces = context.api.workspaces_list()
    context.workspace = context.workspaces[0]['id']

@when(u'we create a new project')
def step(context):
    context.response_from_asana = \
			context.api.new_project(context.workspace, "My new project", "Some notes for the project")

@then(u"we will receive a confirmation of the project's creation")
def step(context):
    assert context.response_from_asana

###############################################################################

# Get Project Details
@given(u'a specific project id to get its details')
def step(context):
    context.api = pysana.API(key)
    context.test_project_id = test_project_id


@when(u'we request the details of the project')
def step(context):
    context.test_project_details = \
                        context.api.project_details(context.test_project_id)


@then(u'we receive the details of the project')
def step(context):
    assert context.test_project_details

###############################################################################
