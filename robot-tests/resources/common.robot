*** Settings ***
# Common Robot Framework Resource File
# Contains shared settings, libraries, and keywords

Documentation     Common resource file for all test suites
...               Uses Page Object Model - NO selectors in test files

# ==================== Libraries ====================
Library           SeleniumLibrary
Library           RequestsLibrary
Library           Collections
Library           String
Library           DateTime

# Page Object Library (contains all page objects with XPath locators)
Library           pages.page_factory

# Custom Libraries
Library           custom-libraries.TestDataGenerator.generator
Library           custom-libraries.VisualValidator.visual_ai
Library           custom-libraries.CustomReporter.reporter

# ==================== Variables ====================
${BASE_URL}           https://the-internet.herokuapp.com
${API_BASE_URL}       https://jsonplaceholder.typicode.com
${BROWSER}            chrome
${HEADLESS}           ${True}
${TIMEOUT}            10s

# Test Data from config
${VALID_USERNAME}     tomsmith
${VALID_PASSWORD}     SuperSecretPassword!
${INVALID_USERNAME}   invalid_user
${INVALID_PASSWORD}   wrong_password

# ==================== Keywords ====================

# ==================== Browser Setup Keywords ====================

Open Browser And Navigate To Home
    [Documentation]    Open browser and navigate to base URL
    [Arguments]    ${url}=${BASE_URL}
    ${browser}=    Get Browser
    ${home_page}=    Get Home Page    ${url}
    [Return]    ${home_page}

Open Browser And Navigate To Login
    [Documentation]    Open browser and navigate to login page
    ${login_page}=    Get Login Page
    [Return]    ${login_page}

Close Browser Session
    [Documentation]    Close all browsers
    Close Browser

Setup Browser
    [Documentation]    Setup browser for test suite
    Open Browser    ${BASE_URL}    ${BROWSER}    options=headless=${HEADLESS}
    Set Selenium Timeout    ${TIMEOUT}

Teardown Browser
    [Documentation]    Teardown browser after test suite
    Close All Browsers

# ==================== Page Object Keywords ====================
# These keywords call page object methods - NO selectors here

# Home Page Keywords
Home Page Get Heading
    [Documentation]    Get home page heading
    [Arguments]    ${home_page}
    ${heading}=    Call Method    ${home_page}    get_page_heading
    [Return]    ${heading}

Home Page Navigate To Login
    [Documentation]    Navigate from home to login page
    [Arguments]    ${home_page}
    ${login_page}=    Call Method    ${home_page}    navigate_to_login
    [Return]    ${login_page}

# Login Page Keywords
Login Page Enter Username
    [Documentation]    Enter username on login page
    [Arguments]    ${login_page}    ${username}
    Call Method    ${login_page}    enter_username    ${username}

Login Page Enter Password
    [Documentation]    Enter password on login page
    [Arguments]    ${login_page}    ${password}
    Call Method    ${login_page}    enter_password    ${password}

Login Page Click Login
    [Documentation]    Click login button
    [Arguments]    ${login_page}
    Call Method    ${login_page}    click_login_button

Login Page Login
    [Documentation]    Perform login with credentials
    [Arguments]    ${login_page}    ${username}    ${password}
    ${result_page}=    Call Method    ${login_page}    login    ${username}    ${password}
    [Return]    ${result_page}

Login Page Get Error Message
    [Documentation]    Get error message from login page
    [Arguments]    ${login_page}
    ${error}=    Call Method    ${login_page}    get_error_message
    [Return]    ${error}

Login Page Is Login Successful
    [Documentation]    Check if login was successful
    [Arguments]    ${login_page}
    ${success}=    Call Method    ${login_page}    is_login_successful
    [Return]    ${success}

Login Page Get Secure Area Heading
    [Documentation]    Get secure area heading after login
    [Arguments]    ${page}
    ${heading}=    Call Method    ${page}    get_secure_area_heading
    [Return]    ${heading}

Login Page Is Logout Button Visible
    [Documentation]    Check if logout button is visible
    [Arguments]    ${page}
    ${visible}=    Call Method    ${page}    is_logout_button_visible
    [Return]    ${visible}

# ==================== Screenshot Keywords ====================

Capture Screenshot If Failed
    [Documentation]    Capture screenshot if test failed
    [Arguments]    ${test_name}    ${status}
    Run Keyword If    '${status}' == 'FAIL'    Capture Page Screenshot    ${test_name}

Capture And Compare Screenshot
    [Documentation]    Capture screenshot and compare with baseline
    [Arguments]    ${element_name}
    ${screenshot_path}=    Capture Page Screenshot    ${screenshot_dir}/${element_name}_${datetime}.png
    ${result}=    Compare Visual    ${element_name}    current_path=${screenshot_path}
    Log    Similarity: ${result}[similarity]
    Should Be True    ${result}[similarity] >= ${result}[threshold]

# ==================== Test Data Keywords ====================

Generate Random User Data
    [Documentation]    Generate random user data for testing
    ${user}=    Generate Random User
    [Return]    ${user}

Generate Test Email
    [Documentation]    Generate test email address
    [Arguments]    ${domain}=${None}
    ${email}=    Generate Email    ${domain}
    [Return]    ${email}

Generate Test Password
    [Documentation]    Generate test password
    [Arguments]    ${length}=12
    ${password}=    Generate Password    ${length}
    [Return]    ${password}

# ==================== Assertion Keywords ====================

Heading Should Be
    [Documentation]    Assert heading equals expected value
    [Arguments]    ${actual}    ${expected}
    Should Be Equal    ${actual}    ${expected}
    ...    msg=Expected heading "${expected}" but got "${actual}"

Error Message Should Contain
    [Documentation]    Assert error message contains text
    [Arguments]    ${actual}    ${expected}
    Should Contain    ${actual}    ${expected}
    ...    msg=Expected error message to contain "${expected}"

Status Should Be Success
    [Documentation]    Assert login was successful
    [Arguments]    ${is_successful}
    Should Be True    ${is_successful}
    ...    msg=Expected login to be successful

# ==================== API Keywords ====================

Create API Session
    [Documentation]    Create API session for testing
    [Arguments]    ${alias}=api_session    ${base_url}=${API_BASE_URL}
    Create Session    ${alias}    ${base_url}

Get API Response
    [Documentation]    Perform GET request
    [Arguments]    ${alias}    ${endpoint}
    ${response}=    Get Request    ${alias}    ${endpoint}
    [Return]    ${response}

Post API Request
    [Documentation]    Perform POST request
    [Arguments]    ${alias}    ${endpoint}    ${data}
    ${response}=    Post Request    ${alias}    ${endpoint}    json=${data}
    [Return]    ${response}

Assert API Status Code
    [Documentation]    Assert API response status code
    [Arguments]    ${response}    ${expected_code}
    Should Be Equal As Numbers    ${response.status_code}    ${expected_code}

Assert Response Contains Key
    [Documentation]    Assert JSON response contains key
    [Arguments]    ${response}    ${key}
    ${json}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    ${key}

# ==================== Reporting Keywords ====================

Start Test Reporting
    [Documentation]    Start reporting for a test
    [Arguments]    ${test_name}    ${tags}=${EMPTY}
    Start Test Report    ${test_name}    ${tags}

End Test Reporting
    [Documentation]    End reporting for a test
    [Arguments]    ${test_name}    ${status}    ${message}=${EMPTY}
    End Test Report    ${test_name}    ${status}    ${message}

Generate Enhanced Report
    [Documentation]    Generate enhanced HTML report
    ${path}=    Generate Custom Report
    Log    Enhanced report generated: ${path}
