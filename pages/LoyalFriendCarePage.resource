# LoyalFriendCarePage.resource
# C:\Users\user\PycharmProjects\Robot-Selenium-Sample\pages\LoyalFriendCarePage.resource

*** Settings ***
Library    ../utils/click_utils.py
Library    ../utils/sendkey_utils.py

*** Variables ***
${email_BOX_xPATH}      //input[@id='email']
${password_BOX_xPATH}   //input[@id='password']
${login_BUTTON_xPATH}   //button[@type='submit']

*** Keywords ***
Perform Login
    [Arguments]    ${user_email}    ${user_password}
    [Documentation]    Enters email and password, then clicks the login button.
    Send Keys Smartly    xpath=${email_BOX_xPATH}       ${user_email}
    Send Keys Smartly    xpath=${password_BOX_xPATH}    ${user_password}
    Smart Click Element  xpath=${login_BUTTON_xPATH}
