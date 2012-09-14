from behave import *
from pysana import API

key = 'oHKGELa.71Xsjl1PalAaX2cydWcke1DP'


# List the workspaces
@given(u'I wish to list the workspaces')
def step(context):
    context.api = API(key)
    assert context.api

@when(u'I request the list of workspaces')
def step(context):
    context.workspaces = context.api.workspaces_list()
    assert context.workspaces

@then(u'I receive a list of workspaces')
def step(context):
    if context.workspaces[0]['id']:
        assert True
    else:
        assert False


# Update existing workspaces
@given(u'I have a workspace id')
def step(context):
    context.api = API(key)
    context.api.update_workspaces()
    context.workspace_id = context.api.workspaces[0]['id']
    assert context.workspace_id

@when(u'I submit a request to update the workspace')
def step(context):
    context.update_response = \
            context.api.workspace_name(context.workspace_id,
                                "Pysana updating workspace name")
    if context.update_response["errors"]:
        assert False
    else:
        assert True

@then(u'I receive confirmation the workspace was updated')
def step(context):
    assert context.update_response
