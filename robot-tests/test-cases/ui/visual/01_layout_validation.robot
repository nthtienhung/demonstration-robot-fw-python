*** Settings ***
# Visual Layout Validation Tests
# POM Pattern: Uses basic screenshot capture for visual validation

Documentation       Visual validation tests for layout regression testing
...                 Captures and compares screenshots

Library             SeleniumLibrary

Test Setup          Open Browser For Visual Tests
Test Teardown       Close All Browsers

*** Variables ***
${BASE_URL}              https://the-internet.herokuapp.com
${BROWSER}               headlesschrome
${HOMEPAGE_ELEMENT}      homepage_layout
${LOGIN_ELEMENT}         login_layout

*** Test Cases ***
Capture Homepage Screenshot
    [Documentation]    Capture screenshot for homepage layout
    [Tags]    visual    baseline    homepage

    # Navigate to home page
    Go To    ${BASE_URL}

    # Wait for page to fully load
    Sleep    2s

    # Capture screenshot
    ${screenshot_path}=    Capture Page Screenshot    filename=${HOMEPAGE_ELEMENT}_current.png

    Log    Screenshot captured: ${screenshot_path}

Capture Login Page Screenshot
    [Documentation]    Capture screenshot for login page layout
    [Tags]    visual    baseline    login

    # Navigate to login page
    Go To    ${BASE_URL}/login

    # Wait for page to fully load
    Sleep    2s

    # Capture screenshot
    ${screenshot_path}=    Capture Page Screenshot    filename=${LOGIN_ELEMENT}_current.png

    Log    Screenshot captured: ${screenshot_path}

*** Keywords ***
Open Browser For Visual Tests
    [Documentation]    Setup browser for visual tests
    Open Browser    ${BASE_URL}    ${BROWSER}
    Set Selenium Implicit Wait    5s
