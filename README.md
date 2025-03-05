# Loan Management System  
**LIVE URL**
-- https://loan-management.onrender.com/api/auth/register

## Project Overview  
The Loan Management System is a Django-based web application that allows users to apply for loans, track loan status, and manage repayments. Admin users can approve, reject, and close loans. The project uses PostgreSQL for database management and JWT authentication for secure user login.  

## Features  
### User Features  
- **User Registration and Login:** Register and login with email OTP verification.  
- **Loan Application:** Apply for loans with details like **amount**, **tenure**, and **interest**.  
- **View Loans:** View active and closed loans.  
- **Loan Status:** Track loan approval, rejection, or closure.  
- **Payment Schedule:** View monthly payment details via `/loans/<pk>/schedule/`.  

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
- **Deployment:** Render  

## API Endpoints (Updated) 

1. ### Authentication  
- **Register:** POST /api/auth/register/  
- **Request OTP:** POST /api/auth/request-otp/  
- **Verify OTP:** POST /api/auth/verify-otp/  
- **Logout:** POST /api/auth/logout/  
- **User List (Admin):** GET /api/auth/users/  

2. ### Loan Management  
- **Create Loan:** POST /loans/  
- **List User Loans:** GET /loans/  
- **Loan Details:** GET /loans/<pk>/  
- **Admin Loan List:** GET /admin/loans/  
- **Update Loan Status (Admin):** PATCH /api/admin/loans/<loan_id>/status/  
- **Foreclose Loan:** POST /loans/<pk>/foreclose/  
- **Payment Schedule:** GET /loans/<pk>/schedule/  

3. ### Tokens  
- **JWT Token Obtain:** POST /api/token/  
- **JWT Token Refresh:** POST /api/token/refresh/  

## Setup Instructions  
1. **Clone the repository:**  
   git clone <repo-url>  
   cd loan-management-system  

2. **Create a virtual environment:**  
   python -m venv venv  
   source venv/bin/activate  # Linux/macOS  
   venv\Scripts\activate     # Windows  

3. **Install dependencies:**  
   pip install -r requirements.txt  

4. **Set up environment variables:**  
   Create a `.env` file in the root directory with:  
   SECRET_KEY=your_secret_key  
   DEBUG=True  
   DATABASE_URL=postgres://user:password@localhost:5432/loan_db  
   SENDGRID_API_KEY=your_sendgrid_api_key  

5. **Apply database migrations:**  
   python manage.py migrate  

6. **Run the server:**  
   python manage.py runserver  

## Sample API Requests  
### User Registration (POST /api/auth/register/)  
{  
  "email": "user@example.com",  
  "username":"user",
  "password": "securepassword123"  
}  
### User Login (POST /api/auth/login/) 
{  
  "email": "user@example.com",  
  "username":"user",
  "password": "securepassword123"  
}  
### Request OTP (POST /api/auth/request-otp/)  ### OPTIONAL
{  
  "email": "user@example.com",  
   
}  
### User Verify Otp (POST /api/auth/verify-otp/) 
{  
  "email": "user@example.com",  
  "otp": "123456"  
}  
**Response**
{
   "refresh":"eyvbhjkbvtdfagvgbacgscs5467yc45uiyghdgsuygskyfgscsfsvfsgd",
   "access":"eydcfgvhjjvhjbhna566tuybgavgjhbagsjjknbfahzghnbvcasraysu7"
}

### Users List (GET /api/auth/user/) 

### Token Refreshing ( POST /api/token/refresh/) ---> Use Refresh token when Logged In

## Copy & Paste the access token in Authorization header's selecting Bearer Token

### Create Loan (POST /loans/)  
{  
  "amt": 15000,  
  "tenure": 6,  
  "interest": 10.2  
}  

### View All Loans (GET /api/loans/)  

### View Single Loan Detail (GET /loans/<int:pk>/)  

### View Loan EMI Dates (GET /api/loans/<int:pk>/schedule/)
**Response:**  
```json  
{
  "status": "success",
  "data": [
    {
      "installment_no": 1,
      "due_date": "2024-03-24",
      "amount": 920.59
    },
    // ... other installments
  ]
}
```

### Update Loan Status (Admin PATCH /api/admin/loans/1/status/)  

### Foreclose Loan (Admin POST /loans/<int:pk>/foreclose/)  


## Testing the API  
1. Use Postman to test endpoints.  
2. Include JWT tokens in the `Authorization: Bearer <token>` header for all authenticated routes.  
3. Test edge cases like invalid OTP, insufficient loan amounts, or unauthorized admin actions.  

## Deployment on Render  
1. **Connect your Git repository** to Render.  
2. **Add environment variables** in Render's dashboard (same as `.env` file).  
3. **Set build command:**  
   python manage.py migrate  
4. **Set start command:**  
   python manage.py runserver 0.0.0.0:$PORT
5. DEBUG=False 

**LIVE API URL LINK**
-- https://loanmanagementsystem-mcil.onrender.com



## Contributors  
- **Jissmon Raju** (Project Owner & Developer)  

## License  
MIT License.  
