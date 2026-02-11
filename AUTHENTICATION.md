# Authentication System Implementation

## Overview
Custom login and register functionality has been successfully added to The Spielberg project with both backend and frontend components.

## Backend Implementation

### 1. Serializers (`scriptwriter/serializers.py`)
- **UserRegisterSerializer**: Handles user registration with validation
  - Username uniqueness check
  - Email uniqueness check
  - Password confirmation validation
  - Minimum password length of 8 characters
  - Secure password hashing via `create_user()`

- **UserLoginSerializer**: Handles login credentials
  - Username and password fields
  - Password is write-only

- **UserSerializer**: Returns user information
  - Fields: id, username, email

### 2. Views (`scriptwriter/views.py`)
Four new authentication endpoints:

- **`register_user()`** (POST `/api/auth/register/`)
  - Registers new user
  - Automatically logs in user after registration
  - Returns user data on success

- **`login_user()`** (POST `/api/auth/login/`)
  - Authenticates user credentials
  - Creates session on success
  - Returns user data

- **`logout_user()`** (POST `/api/auth/logout/`)
  - Requires authentication
  - Destroys user session
  - Returns success message

- **`get_current_user()`** (GET `/api/auth/user/`)
  - Requires authentication
  - Returns current user information

- **`auth_page()`** (GET `/auth/`)
  - Renders the login/register template

### 3. URLs (`scriptwriter/urls.py`)
Added authentication routes:
- `/auth/` - Login/Register page
- `/api/auth/register/` - Registration endpoint
- `/api/auth/login/` - Login endpoint
- `/api/auth/logout/` - Logout endpoint
- `/api/auth/user/` - Get current user endpoint

### 4. Settings (`spielberg_project/settings.py`)
- Configured REST Framework to use SessionAuthentication
- Added session configuration:
  - 2-week session duration
  - HTTPOnly cookies
  - SameSite=Lax for CSRF protection

## Frontend Implementation

### 1. Authentication Page (`scriptwriter/templates/scriptwriter/auth.html`)
Beautiful standalone login/register page with:
- **Tab-based interface** for switching between login and register
- **Login form**: username, password
- **Register form**: username, email, password, confirm password
- **Real-time validation** and error messages
- **Loading states** during API calls
- **Success messages** with automatic redirect
- **CSRF token handling**
- **Responsive design** matching the app's theme

Features:
- Alpine.js for reactive state management
- Client-side password matching validation
- Detailed error handling for all validation cases
- Auto-redirect to main page after successful auth

### 2. Main Page Updates (`scriptwriter/templates/scriptwriter/index_pro.html`)
Enhanced authentication integration:

- **Header redesign**:
  - Shows username and logout button when authenticated
  - Shows "Login / Register" link when not authenticated
  - Better visual hierarchy

- **Auth checking**:
  - Calls `/api/auth/user/` on page load
  - Stores current user information
  - Conditionally loads data based on auth status

- **Logout functionality**:
  - Logout button in header
  - Clears session via API
  - Redirects to auth page

- **Protected content**:
  - Shows auth warning on protected tabs
  - Links to new `/auth/` page instead of Django admin

## Security Features

1. **Session-based authentication** - Secure, server-side sessions
2. **CSRF protection** - All forms include CSRF tokens
3. **Password validation** - Django's built-in validators
4. **HTTPOnly cookies** - Prevents XSS attacks
5. **Password hashing** - Django's secure password storage
6. **Username/email uniqueness** - Prevents duplicate accounts

## Usage

### For Users:
1. Visit `/auth/` to access login/register page
2. Register a new account or login with existing credentials
3. Access full functionality on the main page
4. Logout via header button

### For Developers:
All API endpoints use standard Django authentication:
```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    user = request.user  # Access current user
    # ... your code
```

## Testing

To test the implementation:

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Visit `http://localhost:8000/auth/`

3. Test registration:
   - Create a new account
   - Verify validation errors for duplicate usernames/emails
   - Verify password confirmation

4. Test login:
   - Login with created account
   - Verify redirect to main page
   - Verify user info in header

5. Test logout:
   - Click logout button
   - Verify redirect to auth page
   - Verify cannot access protected endpoints

## API Endpoints Summary

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/auth/` | GET | No | Login/Register page |
| `/api/auth/register/` | POST | No | Register new user |
| `/api/auth/login/` | POST | No | Login user |
| `/api/auth/logout/` | POST | Yes | Logout user |
| `/api/auth/user/` | GET | Yes | Get current user |

## Next Steps (Optional Enhancements)

1. **Password reset** - Add email-based password reset
2. **Email verification** - Verify email addresses on registration
3. **Social authentication** - Add OAuth providers (Google, GitHub)
4. **Two-factor authentication** - Add 2FA support
5. **Profile page** - Allow users to update their information
6. **Remember me** - Extended session option
