# US002demeoweb.robot
# C:\Users\user\PycharmProjects\robot_beta_UI\Tests\US002demeoweb.robot

*** Settings ***
Library         SeleniumLibrary
Library         String
Library         Collections
Resource        ../pages/demowbshopPage.resource
Library         ../utils/click_utils.py
Library         ../utils/sendkey_utils.py
Variables       ../properties/test_data.py

*** Variables ***
${BROWSER}      chrome

*** Test Cases ***
Login to demowebShop
    [Documentation]    Test the login functionality of demowebshop
    [Tags]    login

    # Kullanıcı demeowebshop sitesini acar
    Open Browser        ${demowebShop_Login_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    10s

    # Kullanıcı login linkine basar
    ${status}=    Smart Click Element    xpath=${loginButton_Xpath}
    Should Be True    ${status}    Login linkine tıklanamadı.

    # Kullanıcı email ve şifre girer

    Smart Send Keys    xpath=${mailBox_Xpath}    text=${login_webshop}
    Smart Send Keys    xpath=${passwordBox_Xpath}    text=${password_webshop}
    Smart Click Element    xpath=${submitButton_Xpath}

    # Başarılı girişi doğrula
    Wait Until Element Is Visible    xpath=//*[@class="ico-logout"]    timeout=10s
    Log    Login successful!

    [Teardown]    Close Browser
