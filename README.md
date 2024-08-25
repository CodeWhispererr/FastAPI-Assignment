## FastAPI User Management System

This is a FastAPI application for user management, including registration, login, updating preferences, linking an ID, and deleting accounts. The application uses JWT for authentication and MongoDB as the database.

### Features

- **User Registration**: Register a new user with a username, email, and password.
- **User Login**: Authenticate users and create a JWT access token.
- **Update Preferences**: Users can update their theme, notification preferences, and language settings.
- **Link ID**: Users can link a specific ID to their account.
- **Delete Account**: Users can delete their account and associated data.
- **Logout**: Users can log out by deleting the JWT token.

### Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CodeWhispererr/FastAPI-Assignment.git
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MongoDB:**

   Ensure MongoDB is running and accessible. Update the `get_db()` function in `database.py` with your MongoDB URI.

4. **Run the application:**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the application:**

   Open your browser and navigate to `http://127.0.0.1:8000`.

### Test User Credentials

To test the application, you can use the following test user credentials:

- **Email**: `test@example.com`
- **Password**: `123456`

### Endpoints

- **`GET /`**: Home page.
- **`GET /login`**: Login page.
- **`POST /login`**: Authenticate user.
- **`GET /register`**: Registration page.
- **`POST /register`**: Register a new user.
- **`GET /home`**: User's home page, displays user data and preferences.
- **`POST /update-preferences`**: Update user preferences.
- **`POST /link-id`**: Link an ID to the user's account.
- **`POST /delete-account`**: Delete the user's account and associated data.
- **`GET /logout`**: Logout and remove the JWT token.

### Dependencies

- **FastAPI**
- **Jinja2**
- **PyJWT (jose)**
- **Passlib**
- **pymongo**
