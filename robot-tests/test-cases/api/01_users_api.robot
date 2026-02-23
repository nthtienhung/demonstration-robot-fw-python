*** Settings ***
# Users API Tests
# Tests for JSONPlaceholder API endpoints

Documentation       API tests for JSONPlaceholder Users endpoint
...                 Validates GET and POST requests for /users

Library             RequestsLibrary
Library             Collections

*** Variables ***
${API_BASE_URL}         https://jsonplaceholder.typicode.com
${API_ALIAS}            jsonplaceholder
${USERS_ENDPOINT}       /users
${EXPECTED_USER_COUNT}  10

*** Test Cases ***
Get All Users Successfully
    [Documentation]    Verify GET /users returns list of users
    [Tags]    api    smoke    users

    # Create API session
    Create Session    ${API_ALIAS}    ${API_BASE_URL}

    # Perform GET request
    ${response}=    Get Request    ${API_ALIAS}    ${USERS_ENDPOINT}

    # Assert status code
    Should Be Equal As Numbers    ${response.status_code}    200
    ...    msg=Expected status 200 but got ${response.status_code}

    Log    Status Code: ${response.status_code}

    # Get response JSON
    ${users}=    Set Variable    ${response.json()}

    # Assert user count
    ${user_count}=    Get Length    ${users}
    Should Be Equal As Numbers    ${user_count}    ${EXPECTED_USER_COUNT}
    ...    msg=Expected ${EXPECTED_USER_COUNT} users but got ${user_count}

    Log    Total users returned: ${user_count}

    # Verify first user has required fields
    ${first_user}=    Get From List    ${users}    0
    Dictionary Should Contain Key    ${first_user}    name
    Dictionary Should Contain Key    ${first_user}    email
    Dictionary Should Contain Key    ${first_user}    id

    Log    First user: ${first_user}[name] (${first_user}[email])

    [Teardown]    Delete All Sessions

Get Single User Successfully
    [Documentation]    Verify GET /users/{id} returns specific user
    [Tags]    api    smoke    users

    # Create API session
    Create Session    ${API_ALIAS}    ${API_BASE_URL}

    # Get user with ID 1
    ${user_id}=    Set Variable    1
    ${response}=    Get Request    ${API_ALIAS}    ${USERS_ENDPOINT}/${user_id}

    # Assert status code
    Should Be Equal As Numbers    ${response.status_code}    200
    ...    msg=Expected status 200 but got ${response.status_code}

    Log    Status Code: ${response.status_code}

    # Get response JSON
    ${user}=    Set Variable    ${response.json()}

    # Verify user ID matches
    Should Be Equal As Numbers    ${user}[id]    ${user_id}
    ...    msg=Expected user ID ${user_id} but got ${user}[id]

    # Verify required fields exist
    Dictionary Should Contain Key    ${user}    name
    Dictionary Should Contain Key    ${user}    username
    Dictionary Should Contain Key    ${user}    email

    Log    User retrieved: ${user}[name] (${user}[username])

    # Verify email format
    ${email}=    Set Variable    ${user}[email]
    Should Contain    ${email}    @
    ...    msg=Email should contain @ symbol

    [Teardown]    Delete All Sessions

Get Non-Existent User Returns 404
    [Documentation]    Verify GET /users/{id} with invalid ID returns 404
    [Tags]    api    users    negative

    # Create API session
    Create Session    ${API_ALIAS}    ${API_BASE_URL}

    # Try to get user with non-existent ID
    ${user_id}=    Set Variable    99999
    ${response}=    Get Request    ${API_ALIAS}    ${USERS_ENDPOINT}/${user_id}

    # Assert status code is 404
    Should Be Equal As Numbers    ${response.status_code}    404
    ...    msg=Expected status 404 for non-existent user but got ${response.status_code}

    Log    Correctly returned 404 for non-existent user

    [Teardown]    Delete All Sessions

Create New User Successfully
    [Documentation]    Verify POST /users creates a new user
    [Tags]    api    users    post

    # Create API session
    Create Session    ${API_ALIAS}    ${API_BASE_URL}

    # Generate test user data
    ${test_name}=    Set Variable    Test User
    ${test_username}=    Set Variable    testuser${EMPTY}
    ${test_email}=    Set Variable    testuser@example.com

    # Create user data payload
    ${user_data}=    Create Dictionary
    ...    name=${test_name}
    ...    username=${test_username}
    ...    email=${test_email}

    Log    Creating user with data: ${user_data}

    # Perform POST request
    ${response}=    Post Request    ${API_ALIAS}    ${USERS_ENDPOINT}    json=${user_data}

    # Assert status code (JSONPlaceholder returns 201)
    Should Be Equal As Numbers    ${response.status_code}    201
    ...    msg=Expected status 201 but got ${response.status_code}

    Log    Status Code: ${response.status_code}

    # Get response JSON
    ${created_user}=    Set Variable    ${response.json()}

    # Verify response contains the data we sent
    Should Be Equal    ${created_user}[name]    ${test_name}
    Should Be Equal    ${created_user}[username]    ${test_username}
    Should Be Equal    ${created_user}[email]    ${test_email}

    # Verify ID was generated
    Dictionary Should Contain Key    ${created_user}    id

    Log    User created with ID: ${created_user}[id]

    [Teardown]    Delete All Sessions
