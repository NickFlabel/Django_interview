# Phone Authentication app

The Phone Authentication and User Profiles App is a Django-based application that offers phone number-based authentication and user profile management. It allows users to seamlessly authenticate using their phone numbers and manage their profiles with ease. This app provides a set of endpoints to facilitate the authentication process, retrieve user profiles, and more.

## Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/NickFlabel/Django_interview.git

2. Start the app using the following command:
    ```bash
    docker-compose up --build

3. The API will be accessable at http://0.0.0.0:8000

### Send User Phone Number for Authorization

    Endpoint: api/account/auth/
    Method: POST
    Description: Send user phone number to initiate authorization process. Generates and sends a verification code to the provided phone number.
    Request Body:

    json

    {
    "phone_number": "<user_phone_number>"
    }

    Response: 200 OK
    Response: 403 Forbidden (if verification code is invalid)

### Send User Phone Code for JWT Token

    Endpoint: api/account/code/
    Method: POST
    Description: Send user phone code along with phone number to obtain JWT token and complete authorization process.
    Request Body:

    json

    {
    "phone_number": "<user_phone_number>",
    "code": "<verification_code>"
    }

    Response: 200 OK (with JWT token)
    Response: 403 Forbidden (if verification code is invalid)

### Get User Profile Info

    Endpoint: api/account/profile/
    Method: GET
    Description: Get user's profile information.
    Authentication: User must be authenticated.
    Response: 200 OK (with user profile data)
    Response: 403 Forbidden (if user is not authenticated or not authorized to view the profile)

### Set Activation Code from Another User

    Endpoint: api/account/activation_code/
    Method: POST
    Description: Set an invite code from another user as the current user's activation code.
    Authentication: User must be authenticated.
    Request Body:

    json

    {
    "code": "<activation_code>"
    }

    Response: 200 OK
    Response: 400 Bad Request (if activation code cannot be set)

### Reset Database for Testing

    Endpoint: api/account/reset/
    Method: GET
    Description: Delete all user information from the database (for testing purposes).
    Response: 200 OK

### API Documentation

    Endpoint: api/account/docs/
    Method: GET
    Description: View interactive API documentation (using Swagger UI).
    Authentication: No authentication required.
