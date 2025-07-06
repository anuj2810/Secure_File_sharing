🔐 Secure File Sharing System (Django + JWT Auth + Role-Based Access)

A secure file sharing platform built with Django REST Framework, featuring:
- 🔐 Role-based access (Admin / OPS / Client)
- 📁 File upload (only by OPS users)
- ✅ Email verification for Client signup
- 📬 Email-based secure file download links
- 🔑 JWT Authentication (Login, Refresh)

---

## 🚀 Features

| Role     | Permissions                                  |
|----------|----------------------------------------------|
| Admin    | LOGIN                                        |
| OPS      | Login, Upload files                          |
| Client   | Signup, Verify Email, View & Download files  |

---

## 🧱 Tech Stack

- **Backend**: Django 5.2.4, Django REST Framework
- **Auth**: JWT (SimpleJWT)
- **Database**: SQLite (default)
- **Email**: Console-based backend for development
- **API Testing**: Postman Collection

---

## 📁 Folder Structure

secure_file_share/
├── users/ # CustomUser model, signup/login, verify
├── files/ # File upload, listing, download
├── secure_file_share/ # Main Django project settings
├── manage.py
├── requirements.txt
└── secure_file_share_collection.json ✅ (Postman Collection)

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. 🔧 Clone & Setup Virtual Environment


git clone (https://github.com/anuj2810/Secure_File_sharing.git)
cd secure_file_share
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
2. 🔐 Apply Migrations & Create Superuser
bash
Copy
Edit
python manage.py migrate
python manage.py createsuperuser
3. 📨 Email Setup (Console for Dev)
Already configured in settings.py:

py
Copy
Edit
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
So email links (verify/download) appear directly in terminal.

4. ▶️ Run Server
bash
Copy
Edit
python manage.py runserver
🧪 API Testing with Postman
📁 secure_file_share_collection.json is included for testing full flow.

➕ Postman Collection Flow
✅ Admin Login (auth)

➕ Create OPS User (no auth)

✅ OPS Login (auth)

📤 File Upload

➕ Client Signup (no auth)

✅ Client Email Verification (auto from console email)

✅ Client Login

📄 Client List Files

🔗 Generate Secure Download Link

⬇️ Download file using tokenized secure link

🔐 JWT Authentication Flow

Endpoint	Method	Purpose

/api/login/	POST	Login → JWT access+refresh

/api/token/refresh/	POST	Refresh access token

/api/signup/	POST	Signup (Client)

/api/verify/<encoded_id>/	GET	Email verification

/api/files/upload/	POST	Upload (OPS only)

/api/files/list/	GET	List files (Client only)

/api/files/generate-download-link/<id>/	POST	Generate secure download

/api/files/download/secure/<token>/	GET	Final download from token

🧠 Postman Environment Variables
Use Postman Environment to store reusable values:

JSON 

    {

  /"base_url": "http://127.0.0.1:8000"
  
  /"admin_email": "admin@example.com"
  
  /"admin_password": "admin123"
  
  /"ops_email": "ops1@example.com"
  
  /"ops_password": "ops123"
  
  /"client_email": "deepak10@example.com"
  
  /"client_password": "client123"
  
  /"uploaded_file_id": "
  
  /"secure_download_token"

  }

👉 After file upload, capture the returned id and store in uploaded_file_id.
👉 After generating the secure link, extract token from URL and store in secure_download_token.

🧑‍💻 Developers
Made with ❤️ by @anuj2810
Guided and supported by ChatGPT (2025) for full-stack architecture, Postman flow, and automation.
