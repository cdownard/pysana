Feature: Projects
    
    Scenario: Get all projects
        Given there are currently projects
        When we request the list of projects
        Then we will see the current list of projects

    Scenario: Get all projects from workspace
        Given a workspace id to get its projects
        When we request the list of projects in that workspace id
        Then we will see the current list of projects for that workspace

    Scenario: Create new project
        Given a workspace id for a new project
        When we create a new project
        Then we will receive a confirmation of the project's creation

    Scenario: Get project details
        Given a specific project id to get its details
        When we request the details of the project
        Then we receive the details of the project

