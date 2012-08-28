from behave import *
import pysana


@given(u'there are currently projects')
def step(context):
    context.key = 'oHKGELa.71Xsjl1PalAaX2cydWcke1DP'
    context.api = pysana.API(context.key)
    assert True


@when(u'we request the list of projects')
def step(context):
    context.projects = context.api.list_projects()
    assert context.projects

@then(u'we will see the current list of projects')
def step(context):
    assert context.projects
