*** Settings ***
Library    SeleniumLibrary
Library    String
Library    Collections
Resource   ../pages/LoyalFriendCarePage.resource
Library    ../utils/click_utils.py
Library    ../utils/sendkey_utils.py

*** Variables ***
${name}                lazKOrsan
${email}               lazKorsan190220260356@lazKorsan.com
${password}            Query.2026
${loginUrl}            https://qa.loyalfriendcare.com/en/login
${BROWSER}              chrome


*** Test Cases ***
Login to LoyalFriendCare
    [Documentation]    Test the login functionality of LoyalFriendCare
    [Tags]    login    smoke

    # Start test
    Open Browser        ${loginUrl}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    10s

    # Perform login using the reusable keyword from LoyalFriendCarePage.resource
    Perform Login    ${email}    ${password}

    # Add a verification step to ensure login was successful
    # Wait Until Page Contains    Dashboard    timeout=10s
    # Log    Login successful, "Dashboard" text is visible.

    [Teardown]    Close Browser
