Feature: List the projects
    
    Scenario: Get all projects
        Given there are currently projects
        When we request the list of projects
        Then we will see the current list of projects

    Scenario: Get specific project
        Given 