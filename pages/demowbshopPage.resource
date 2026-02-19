# demowbshopPage.resource
# C:\Users\user\PycharmProjects\robot_beta_UI\pages\demowbshopPage.resource


*** Settings ***
Library         SeleniumLibrary
Library         String
Library         Collections
Library         ../utils/click_utils.py
Library         ../utils/sendkey_utils.py
Variables       ../properties/test_data.py


*** Variables ***
${BROWSER}      chrome
${loginButton_Xpath}    //*[@class="ico-login"]
${mailBox_Xpath}    //input[@id="Email"]
${passwordBox_Xpath}    //input[@id="Password"]
${rememberMe_Xpath}    //input[@id="RememberMe"]
${submitButton_Xpath}    //input[@class="button-1 login-button"]
${logoutButton_Xpath}    //*[@class="ico-logout"]
${customerInfoButton_Xpath}    //*[@href="/customer/info"]

*** Keywords ***
Open Demo WebShop
    Open Browser    ${demowebShop_Login_URL}    ${BROWSER}
    Maximize Browser Window

Go To Login Page
# Kullanıcı login linkine basar
    ${status}=    Smart Click Element    xpath=${loginButton_Xpath}
    Should Be True    ${status}    Login Buttona tıklanamadı.

Login With Credentials
    [Arguments]    ${email}    ${password}
    Smart Send Keys    xpath=${mailBox_Xpath}    text=${email}
    Smart Send Keys    xpath=${passwordBox_Xpath}    text=${password}
    Smart Click Element    xpath=${submitButton_Xpath}

Verify Successful Login
    Wait Until Page Contains Element    xpath=${logoutButton_Xpath}    timeout=10s

Verify Customer Info
    [Arguments]    ${expected_name}
    Verify Element Text And Highlight    locator=${customerInfoButton_Xpath}    expected_text=${expected_name}
