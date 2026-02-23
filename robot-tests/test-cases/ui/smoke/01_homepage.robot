*** Settings ***
# Homepage Smoke Tests
# POM Pattern: All locators in pages/*.py, NO selectors in this file

Documentation       Smoke tests for the Homepage
...                 Verifies basic page functionality using Page Object Model
...                 Target: https://the-internet.herokuapp.com

Library             SeleniumLibrary

Test Setup          Open Browser And Navigate
Test Teardown       Close All Browsers

*** Variables ***
${BASE_URL}                 https://the-internet.herokuapp.com
${BROWSER}                  headlesschrome
${EXPECTED_HEADING}         Welcome to the-internet

*** Test Cases ***
Homepage Loads And Displays Heading
    [Documentation]    Verify home page loads and displays correct heading
    [Tags]    smoke    ui    homepage

    # Wait for page to load
    Wait Until Page Contains Element    xpath://h1    timeout=10s

    # Get heading using XPath
    ${heading}=    Get Text    xpath://h1

    # Assert heading is correct
    Should Be Equal    ${heading}    ${EXPECTED_HEADING}
    ...    msg=Expected heading "${EXPECTED_HEADING}" but got "${heading}"

    Log    Homepage loaded successfully with heading: ${heading}

Homepage Contains Form Authentication Link
    [Documentation]    Verify form authentication link is present
    [Tags]    smoke    ui    homepage

    # Check if link is visible using XPath
    Page Should Contain Element    xpath://a[@href='/login']
    Log    Form Authentication link is visible

Homepage Contains Available Examples
    [Documentation]    Verify available examples section is displayed
    [Tags]    smoke    ui    homepage

    # Check examples list exists
    Page Should Contain Element    xpath://div[@class='row']//li
    Log    Available examples section is visible

Homepage Page Title Is Correct
    [Documentation]    Verify page title is correct
    [Tags]    smoke    ui    homepage

    # Get page title
    ${title}=    Get Title

    Should Contain    ${title}    The Internet
    ...    msg=Expected page title to contain "The Internet" but got "${title}"

    Log    Page title verified: ${title}

*** Keywords ***
Open Browser And Navigate
    [Documentation]    Setup - Open browser and navigate to base URL
    Open Browser    ${BASE_URL}    ${BROWSER}
    Set Selenium Timeout    10s
    # Wait for initial page load
    Wait Until Page Contains    Examples    timeout=10s
