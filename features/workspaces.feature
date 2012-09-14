Feature: Workspaces

    Scenario: List available workspaces
        Given I wish to list the workspaces
        When I request the list of workspaces
        Then I receive a list of workspaces

    Scenario: Update existing workspace
        Given I have a workspace id
        When I submit a request to update the workspace
        Then I receive confirmation the workspace was updated