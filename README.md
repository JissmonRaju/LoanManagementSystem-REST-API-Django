# Loan Management System

## Project Overview
The Loan Management System is a Django-based web application that allows users to apply for loans, track their loan status, and manage repayments. Admin users can approve, reject, and close loans. The project uses PostgreSQL for database management and JWT authentication for secure user login.

## Features
### User Features
- **User Registration and Login:** Register and login with email OTP verification.
- **Loan Application:** Apply for loans with details like amount, tenure, and purpose.
- **View Loans:** View active and closed loans.
- **Loan Status:** Track loan approval, rejection, or closure.
- **View Monthly Pay Date:** View monthly pay amount and time

### Admin Features
- **Loan Management:** Approve, reject, or close loans.
- **User Management:** View all user loans and delete records.
- **Token Blacklisting:** Secure logout by invalidating JWT tokens.

## Technologies Used
- **Backend:** Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT 
- **Email Service:** SendGrid for OTP emails
- **API Testing:** Postman
- **Deployment:** Rende

## API Endpoints
### Authentication
- **Register:** `POST: /api/auth/register/`
- **Login (OTP):** `POST: /api/auth/login/`
- **Verify(OTP):** `POST: /api/auth/verify-otp/`
- **Logout:** `POST: /api/auth/logout/`

### Loan Management
- **Create Loan:** `POST: /api/loans/`
- **View User Loans:** `GET: /api/loans/`
- **Update Loan Status (Admin):** `PATCH: /api/loans/<loan_id>/`
- **Foreclose Loan:** `POST: /api/loans/<loan_id>/foreclose/`
- **Delete Loan (Admin):** `DELETE: /api/loans/<loan_id>/`

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd loan-management-system
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate  # For Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```plaintext
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/loan_db
   SENDGRID_API_KEY=your_sendgrid_api_key
   ```
5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```
6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## Testing the API
1. **Start the server.**
2. **Open Postman** and use the API endpoints listed above.
3. **Set Authorization Headers** where required (JWT tokens for authenticated requests).
4. **Test all possible scenarios:**
   - Valid and invalid logins
   - Loan approvals/rejections by admin
   - Error handling for missing or incorrect data

## Deployment
To deploy on Render:
1. **Create a new Render service** (Web Service).
2. **Connect Git repository.**
3. **Add environment variables** under the "Environment" tab.
4. **Set build and start commands:**
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:$PORT
   ```

## Contributors
- **Jissmon Raju** (Project Owner & Developer)

## License
This project is licensed under the MIT License.


##
Admin side Login-- 
