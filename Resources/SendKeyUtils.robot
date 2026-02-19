*** Settings ***
Library           SeleniumLibrary
Library           Collections

*** Keywords ***
Highlight Element
    [Documentation]    Highlights a web element with a specified color and duration.
    [Arguments]    ${locator}    ${color}=yellow    ${duration}=0.5
    ${element} =    Get WebElement    ${locator}
    ${original_style} =    Execute JavaScript    return arguments[0].getAttribute('style');    ${element}
    Execute JavaScript    arguments[0].setAttribute('style', arguments[1]);    ${element}    border: 3px solid ${color}; background: #ffff99;
    Sleep    ${duration}
    Execute JavaScript    arguments[0].setAttribute('style', arguments[1]);    ${element}    ${original_style}

Send Keys Robustly
    [Documentation]    Provides a robust way to input text into web elements.
    ...    Supports human-like typing, clearing existing text, pressing Enter, and highlighting.
    [Arguments]    ${locator}    ${text}
    ...    ${clear_first}=${TRUE}    ${press_enter}=${FALSE}
    ...    ${human_like}=${FALSE}    ${delay}=0.1s
    ...    ${highlight_color}=yellow    ${timeout}=10s
    
    Log To Console    ======================================================================
    Log To Console    [Send Keys Robustly] 🚀 Yazma işlemi başlıyor...
    Log To Console    [Send Keys Robustly]    ├─ Metin: '${text}'
    Log To Console    [Send Keys Robustly]    ├─ Locator: ${locator}
    Log To Console    [Send Keys Robustly]    ├─ İnsan gibi: ${human_like}
    Log To Console    [Send Keys Robustly]    └─ Enter: ${press_enter}
    Log To Console    ${'='*70}

    Wait Until Element Is Visible    ${locator}    timeout=${timeout}
    Wait Until Element Is Enabled    ${locator}    timeout=${timeout}
    
    Highlight Element    ${locator}    ${highlight_color}

    IF    ${clear_first}
        Clear Element Text    ${locator}
        Sleep    0.2s
    END

    IF    ${human_like}
        FOR    ${char}    IN    @{text.split('')}
            Input Text    ${locator}    ${char}
            ${random_delay} =    Evaluate    random.uniform(0.05, 0.15)    random
            Sleep    ${random_delay}s
        END
    ELSE
        Input Text    ${locator}    ${text}
    END

    IF    ${press_enter}
        Press Keys    ${locator}    RETURN
        Log To Console    [Send Keys Robustly] ✅ Enter tuşuna basıldı
    END
    
    Log To Console    [Send Keys Robustly] ✅ Yazma işlemi BAŞARILI

Send Keys By Id
    [Documentation]    Inputs text into an element located by its ID.
    [Arguments]    ${element_id}    ${text}    &{kwargs}
    ${locator} =    Set Variable    id=${element_id}
    Send Keys Robustly    ${locator}    ${text}    &{kwargs}

Send Keys By Name
    [Documentation]    Inputs text into an element located by its name attribute.
    [Arguments]    ${name}    ${text}    &{kwargs}
    ${locator} =    Set Variable    name=${name}
    Send Keys Robustly    ${locator}    ${text}    &{kwargs}

Send Keys By Class
    [Documentation]    Inputs text into an element located by its class name. Note: may not be unique.
    [Arguments]    ${class_name}    ${text}    &{kwargs}
    ${locator} =    Set Variable    class=${class_name}
    Send Keys Robustly    ${locator}    ${text}    &{kwargs}

Send Keys By Css Selector
    [Documentation]    Inputs text into an element located by CSS Selector.
    [Arguments]    ${css_selector}    ${text}    &{kwargs}
    ${locator} =    Set Variable    css=${css_selector}
    Send Keys Robustly    ${locator}    ${text}    &{kwargs}

Send Keys By Placeholder
    [Documentation]    Inputs text into an element located by its placeholder attribute.
    [Arguments]    ${placeholder_text}    ${text}    &{kwargs}
    ${locator} =    Set Variable    xpath=//input[@placeholder='${placeholder_text}']
    Send Keys Robustly    ${locator}    ${text}    &{kwargs}

Send Keys By Label
    [Documentation]    Inputs text into an element associated with a label using XPath.
    [Arguments]    ${label_text}    ${text}    &{kwargs}
    ${locator} =    Set Variable    xpath=//label[contains(text(), '${label_text}')]/following::input[1]
    Send Keys Robustly    ${locator}    ${text}    &{kwargs}

Send Random Text
    [Documentation]    Generates a random alphanumeric string and inputs it into a field.
    [Arguments]    ${locator}    ${length}=10    &{kwargs}
    ${chars} =    Set Variable    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
    ${random_text} =    Evaluate    ''.join(random.choices(${chars}, k=${length}))    random
    Log To Console    [Send Keys Robustly] 🎲 Rastgele metin: '${random_text}'
    Send Keys Robustly    ${locator}    ${random_text}    &{kwargs}

Send Random Password
    [Documentation]    Generates a strong random password (uppercase, lowercase, digit, symbol + 8 random) and inputs it.
    [Arguments]    ${locator}    &{kwargs}
    ${upper} =    Set Variable    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ${lower} =    Set Variable    abcdefghijklmnopqrstuvwxyz
    ${digits} =    Set Variable    0123456789
    ${symbols} =    Set Variable    !@#$%
    ${all_chars} =    Set Variable    ${upper}${lower}${digits}${symbols}
    ${password} =    Evaluate    random.choice(${upper}) + random.choice(${lower}) + random.choice(${digits}) + random.choice(${symbols}) + ''.join(random.choices(${all_chars}, k=8))    random
    Log To Console    [Send Keys Robustly] 🔐 Şifre oluşturuldu: ${'*' * len(${password})}
    Send Keys Robustly    ${locator}    ${password}    &{kwargs}

Send Random Email
    [Documentation]    Generates a random email address (e.g., test.random@domain.com) and inputs it.
    [Arguments]    ${locator}    ${prefix}=test    &{kwargs}
    @{domains} =    Create List    example.com    test.com    demo.com    instulearn.com
    ${random_string} =    Evaluate    ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))    random
    ${email} =    Set Variable    ${prefix}.${random_string}@${random.choice(${domains})}
    Log To Console    [Send Keys Robustly] 📧 Email oluşturuldu: ${email}
    Send Keys Robustly    ${locator}    ${email}    &{kwargs}

Send Random Phone Number
    [Documentation]    Generates a random Turkish-like phone number (e.g., 5XX XXX XXXX) and inputs it.
    [Arguments]    ${locator}    &{kwargs}
    ${digit1} =    Evaluate    random.randint(10, 99)    random
    ${digit2} =    Evaluate    random.randint(100, 999)    random
    ${digit3} =    Evaluate    random.randint(1000, 9999)    random
    ${phone} =    Set Variable    5${digit1}${digit2}${digit3}
    Log To Console    [Send Keys Robustly] 📱 Telefon: ${phone}
    Send Keys Robustly    ${locator}    ${phone}    &{kwargs}

Send Current Date
    [Documentation]    Inputs today's date or a date offset by a number of days in "DD.MM.YYYY" format.
    [Arguments]    ${locator}    ${days_offset}=0    &{kwargs}
    ${date} =    Evaluate    (datetime.now() + timedelta(days=${days_offset})).strftime("%d.%m.%Y")    datetime, timedelta
    Log To Console    [Send Keys Robustly] 📅 Tarih: ${date}
    Send Keys Robustly    ${locator}    ${date}    &{kwargs}

Clear Text Field
    [Documentation]    Clears the text from a specified input field using the robust send keys mechanism.
    [Arguments]    ${locator}    &{kwargs}
    # Ensure clear_first is TRUE, and remove it from kwargs if present to avoid duplication
    ${kwargs_copy} =    Create Dictionary    &{kwargs}
    Remove From Dictionary    ${kwargs_copy}    clear_first
    Send Keys Robustly    ${locator}    ${EMPTY}    clear_first=${TRUE}    &{kwargs_copy}

Append Text To Field
    [Documentation]    Appends text to the current value of an input field using the robust send keys mechanism.
    [Arguments]    ${locator}    ${text}    &{kwargs}
    # Ensure clear_first is FALSE, and remove it from kwargs if present to avoid duplication
    ${kwargs_copy} =    Create Dictionary    &{kwargs}
    Remove From Dictionary    ${kwargs_copy}    clear_first
    Send Keys Robustly    ${locator}    ${text}    clear_first=${FALSE}    &{kwargs_copy}