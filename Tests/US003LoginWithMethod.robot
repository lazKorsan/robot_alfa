# US003LoginWithMethod.robot
# C:\Users\user\PycharmProjects\robot_beta_UI\Tests\US003LoginWithMethod.robot

*** Settings ***
Documentation    US003 - Test case for successful login functionality.
Library          SeleniumLibrary
Library          Collections
Test Setup       Open Demo WebShop
Test Teardown    Close Browser
Variables       ../properties/test_data.py
Resource        ../pages/demowbshopPage.resource

*** Variables ***

*** Test Cases ***
US003_TC01 Login test
    [Tags]    login2

    Go To Login Page
    Login With Credentials    ${login_webshop}    ${password_webshop}
    Verify Successful Login
