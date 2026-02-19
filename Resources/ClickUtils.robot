*** Settings ***
Library           SeleniumLibrary

*** Keywords ***
Highlight Element For Click
    [Documentation]    Highlights a web element for visual feedback during a click operation.
    [Arguments]    ${locator}    ${color}=yellow    ${duration}=0.5
    ${element} =    Get WebElement    ${locator}
    ${original_style} =    Execute JavaScript    return arguments[0].getAttribute('style');    ${element}
    Execute JavaScript    arguments[0].setAttribute('style', arguments[1]);    ${element}    border: 3px solid ${color}; background: rgba(255,255,0,0.3);
    Sleep    ${duration}
    # Restore original style
    IF    '${original_style}' != '${NONE}' and '${original_style}' != ''
        Execute JavaScript    arguments[0].setAttribute('style', arguments[1]);    ${element}    ${original_style}
    ELSE
        Execute JavaScript    arguments[0].removeAttribute('style');    ${element}
    END

Smart Click Element
    [Documentation]    Waits for, validates, highlights, hovers, and clicks an element.
    [Arguments]    ${locator}    ${element_color}=yellow    ${timeout}=10    ${do_click}=${TRUE}
    
    Log To Console    ======================================================================
    Log To Console    [Smart Click Element] 🚀 Tıklama işlemi başlıyor...
    Log To Console    [Smart Click Element]    ├─ Locator: ${locator}
    Log To Console    [Smart Click Element]    ├─ Rengi: ${element_color}
    Log To Console    [Smart Click Element]    └─ Tıklama yap: ${do_click}
    Log To Console    ${'='*70}

    # 1. WAIT: Wait for element presence and visibility
    Wait Until Element Is Visible    ${locator}    timeout=${timeout}
    Log To Console    [Smart Click Element] Element bulundu ve görünür: ${locator}

    # 2. SCROLL: Elementi ekranın ortasına getir
    Scroll Element Into View    ${locator}
    Log To Console    [Smart Click Element] Element ekrana kaydırıldı: ${locator}

    # 3. GET INFO: Get button name (text) and log it
    ${button_name} =    Run Keyword And Return Status    Get Text    ${locator}
    IF    ${button_name} is ${FALSE}
        ${button_name} =    Get Element Attribute    ${locator}    value
        IF    ${button_name} is ${NONE}
            ${button_name} =    Set Variable    Unnamed Element
        END
    END
    Log To Console    --- Etkileşime geçilen Element: ${button_name} (Locator: ${locator}) ---

    # 4. HIGHLIGHT: Highlight the element
    Highlight Element For Click    ${locator}    ${element_color}
    Log To Console    [Smart Click Element] Element vurgulandı: ${locator}

    # 5. ASSERT (Validation): Visibility check
    Element Should Be Visible    ${locator}
    Log To Console    [Smart Click Element] Görünürlük: Tamam

    # 6. HOVER: Hover over the element
    Mouse Over    ${locator}
    Log To Console    [Smart Click Element] Fare elementin üzerine geldi: ${locator}

    IF    ${do_click}
        # 7. CLICKABILITY CHECK
        Wait Until Element Is Enabled    ${locator}    timeout=${timeout}
        Log To Console    [Smart Click Element] Element tıklanabilir: ${locator}

        # Perform the click
        Click Element    ${locator}
        Log To Console    [Smart Click Element] ✅ Standart tıklama başarılı: ${locator}.
    ELSE
        Log To Console    [Smart Click Element] Tıklama işlemi talep edilmedi.
    END
    Log To Console    [Smart Click Element] ✅ İşlem BAŞARILI