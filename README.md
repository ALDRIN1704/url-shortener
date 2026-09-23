# URL Shortener — Flask + MySQL

A full-stack URL shortening application built using **Python, Flask, MySQL, Docker, Railway, and Render**.

The application allows authenticated users to generate short URLs, redirect visitors to original URLs, track clicks, view analytics, and generate QR codes for shortened links.

---

## 🚀 Live Deployment

### URL Shortener Application

**Live App:**  
https://url-shortener-prv0.onrender.com/

### Health Check

**Health Endpoint:**  
https://url-shortener-prv0.onrender.com/health

### GitHub Repository

**Source Code:**  
https://github.com/ALDRIN1704/url-shortener

> The Flask application is containerized using Docker and deployed on Render.  
> The production MySQL database is hosted on Railway.

---

## 📌 Overview

This project is a full-stack **URL Shortener** application designed to demonstrate backend development, database modeling, API design, authentication, analytics, containerization, and cloud deployment.

The application allows users to:

- Register and log in
- Submit a long URL
- Generate a unique short URL
- Generate a QR code for the short URL
- Open the short URL and redirect to the original website
- Track the number of times a short URL is opened
- Store individual click events
- View URL analytics from a dashboard
- View only URLs created by their own account

The project uses the following architecture:

- **Python / Flask** — backend APIs, authentication, URL shortening, redirects, click tracking, analytics, and QR code generation
- **MySQL** — stores users, shortened URLs, and click events
- **HTML / CSS / JavaScript** — frontend interface and analytics dashboard
- **Werkzeug** — password hashing and verification
- **Gunicorn** — production WSGI server
- **Docker** — application containerization
- **Railway** — production MySQL database hosting
- **Render** — production application hosting
- **GitHub** — source-code management

---

## ✨ Key Features

| Feature | Description |
|---|---|
| URL Shortening | Generates a unique 6-character code for a long URL |
| Redirect Handling | Redirects a short URL to its original destination |
| Click Tracking | Increments the click count whenever a shortened URL is opened |
| Click History | Stores individual click events for analytics |
| Analytics Dashboard | Displays total URLs, total clicks, top URLs, and recent click activity |
| QR Code Generation | Generates a QR code for every shortened URL |
| User Registration | Allows users to create an account |
| User Login | Authenticates users using hashed passwords |
| Session Authentication | Uses Flask sessions to maintain authenticated users |
| User-specific URLs | Users can view only their own shortened URLs |
| URL Validation | Accepts valid `http://` and `https://` URLs |
| Error Handling | Handles invalid URLs, authentication errors, and unknown short codes |
| Docker Support | Packages the application into a portable container |
| Cloud Database | Uses Railway-hosted MySQL |
| Cloud Deployment | Runs the Dockerized Flask application on Render |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Language | Python 3.12 |
| Backend Framework | Flask 3.1 |
| Database | MySQL |
| Database Driver | `mysql-connector-python` |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Flask Sessions |
| Password Security | Werkzeug |
| QR Code Generation | `qrcode` + Pillow |
| Production Server | Gunicorn |
| Containerization | Docker |
| Application Hosting | Render |
| Database Hosting | Railway |
| Version Control | Git + GitHub |

---

## 🏗️ System Architecture

```text
                     User
                      |
                      v
              Render Web Service
                      |
                      v
               Docker Container
                      |
                      v
              Flask + Gunicorn
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
 Authentication   URL Service    Analytics
        |             |             |
        +-------------+-------------+
                      |
                      v
               Railway MySQL
                      |
            +---------+---------+
            |         |         |
            v         v         v
          users      urls     clicks
```

---

## 🔄 Complete Application Flow

```text
User Registration / Login
          |
          v
     Flask Session
          |
          v
    Enter Long URL
          |
          v
     URL Validation
          |
          v
 Generate Unique Code
          |
          v
   Save URL in MySQL
          |
          v
Generate Short URL + QR
          |
          v
 User Opens Short URL
          |
          v
 Find Code in Database
          |
          v
 Increment Click Count
          |
          v
 Store Click Event
          |
          v
 Redirect to Original URL
          |
          v
   Analytics Dashboard
```

---

## 📁 Project Structure

```text
url-shortener/
│
├── app.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── schema.sql
├── railway_schema.sql
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

---

# ⚙️ Implementation

## 1. Database Design

The application uses three main MySQL tables:

```text
users
  |
  | One user can create many URLs
  v
urls
  |
  | One URL can have many click events
  v
clicks
```

This gives the following relationships:

```text
users 1 ------ N urls

urls  1 ------ N clicks
```

---

## 👤 Users Table

The `users` table stores registered user accounts.

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Passwords are never stored directly.

Before inserting a user, the password is hashed using Werkzeug:

```python
generate_password_hash(password)
```

During login, the password is verified using:

```python
check_password_hash(
    user["password_hash"],
    password
)
```

---

## 🔗 URLs Table

The `urls` table stores shortened URLs.

```sql
CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    short_code VARCHAR(20) NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    click_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_urls_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

The table stores:

- URL owner
- Short code
- Original URL
- Total click count
- Creation timestamp

The `short_code` column uses a `UNIQUE` constraint to prevent duplicate shortened URLs.

---

## 🖱️ Clicks Table

The `clicks` table stores individual click events.

```sql
CREATE TABLE IF NOT EXISTS clicks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_id INT NOT NULL,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT,

    CONSTRAINT fk_clicks_url
        FOREIGN KEY (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE
);
```

Each click can store:

- URL ID
- Timestamp
- IP address
- Browser/User-Agent information
- Referrer

This design allows more advanced analytics to be added later.

---

## 📇 Database Indexes

Indexes are created for fields that are queried frequently.

```sql
CREATE INDEX idx_urls_short_code
ON urls(short_code);

CREATE INDEX idx_urls_user_id
ON urls(user_id);

CREATE INDEX idx_clicks_url_id
ON clicks(url_id);

CREATE INDEX idx_clicks_clicked_at
ON clicks(clicked_at);
```

These indexes improve lookup and analytics performance.

---

# 2. Flask Backend

The backend is implemented using Flask.

```python
from flask import Flask

app = Flask(__name__)
```

The backend handles:

```text
Authentication
      |
      v
URL Creation
      |
      v
URL Redirection
      |
      v
Click Tracking
      |
      v
Analytics
      |
      v
QR Code Generation
```

The application communicates with MySQL using:

```text
mysql-connector-python
```

---

# 3. Database Configuration

The same application supports both local and production databases.

## Local Development

For local development, the application reads:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME
```

Example:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=url_shortener
```

---

## Production

For production, the application reads:

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

If `DATABASE_URL` is available, Flask extracts the database configuration from the Railway connection URL.

```python
parsed_db = urlparse(DATABASE_URL)

DB_CONFIG = {
    "host": parsed_db.hostname,
    "port": parsed_db.port or 3306,
    "user": unquote(parsed_db.username or ""),
    "password": unquote(parsed_db.password or ""),
    "database": parsed_db.path.lstrip("/")
}
```

This allows the same application to use:

```text
Local MySQL
```

during development and:

```text
Railway MySQL
```

in production.

Sensitive database credentials are therefore not hard-coded into the source code.

---

# 4. URL Validation

Before creating a shortened URL, the application validates the submitted URL.

```python
def is_valid_url(value):
    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False
```

Only valid HTTP and HTTPS URLs are accepted.

---

# 5. Short Code Generation

The application generates a random 6-character code using uppercase letters, lowercase letters, and numbers.

```python
def generate_code(length=6):
    chars = string.ascii_letters + string.digits

    return "".join(
        random.choices(chars, k=length)
    )
```

Example:

```text
aB91xZ
```

Before using the code, the application checks whether it already exists.

```text
Generate Code
      |
      v
Check Database
      |
  +---+---+
  |       |
Exists   Unique
  |       |
  v       v
Retry    Use Code
```

The application attempts to generate a unique code several times before returning an error.

---

# 6. Short URL Creation

A logged-in user submits:

```json
{
  "url": "https://www.example.com/some/very/long/path"
}
```

The backend:

```text
1. Checks authentication
2. Validates the URL
3. Generates a unique short code
4. Stores it in MySQL
5. Builds the short URL
6. Generates a QR code
7. Returns the result
```

Example:

```text
Original URL:

https://www.example.com/some/very/long/path

                |
                v

Short Code:

Ab12Cd

                |
                v

Short URL:

https://url-shortener-prv0.onrender.com/Ab12Cd
```

---

# 7. Redirect Handling

When a visitor opens:

```text
https://url-shortener-prv0.onrender.com/Ab12Cd
```

Flask executes the redirect route:

```text
GET /<short_code>
```

The flow is:

```text
Short URL
    |
    v
Extract short_code
    |
    v
Search MySQL
    |
 +--+----------------+
 |                   |
Found             Not Found
 |                   |
 v                   v
Update Click         404
 |
 v
Insert Click Event
 |
 v
Commit Transaction
 |
 v
Redirect to Original URL
```

If the short code does not exist:

```json
{
  "error": "Short URL not found"
}
```

is returned with HTTP status `404`.

---

# 8. Click Tracking

Each successful redirect updates the total click counter:

```sql
UPDATE urls
SET click_count = click_count + 1
WHERE id = %s;
```

A detailed click record is also inserted:

```sql
INSERT INTO clicks (
    url_id,
    ip_address,
    user_agent,
    referrer
)
VALUES (%s, %s, %s, %s);
```

---

## Why Store Both `click_count` and `clicks`?

The application stores analytics in two ways.

### Aggregate Counter

```text
urls.click_count
```

is used for quick total-click retrieval.

### Individual Click Events

```text
clicks
```

stores detailed history.

This makes the design both efficient and flexible.

---

# 9. Analytics Dashboard

The application includes an authenticated analytics dashboard.

It displays:

- Total URLs created by the user
- Total clicks
- Top 5 URLs
- Click activity for the last 7 days

---

## Total URLs and Clicks

The backend uses:

```sql
SELECT
    COUNT(*) AS total_urls,
    COALESCE(SUM(click_count), 0) AS total_clicks
FROM urls
WHERE user_id = %s;
```

---

## Top URLs

The top-performing links are retrieved using:

```sql
SELECT
    short_code,
    original_url,
    click_count
FROM urls
WHERE user_id = %s
ORDER BY
    click_count DESC,
    created_at DESC
LIMIT 5;
```

---

## Last 7 Days Analytics

Daily click activity is calculated using:

```sql
SELECT
    DATE(c.clicked_at) AS day,
    COUNT(*) AS clicks
FROM clicks c
JOIN urls u
    ON u.id = c.url_id
WHERE
    u.user_id = %s
    AND c.clicked_at >= DATE_SUB(
        CURDATE(),
        INTERVAL 6 DAY
    )
GROUP BY DATE(c.clicked_at)
ORDER BY day ASC;
```

The analytics flow is:

```text
clicks table
     |
     v
SQL Aggregation
     |
     v
/api/analytics
     |
     v
Frontend Dashboard
```

---

# 10. QR Code Generation

Every shortened URL also receives a QR code.

The project uses:

```text
qrcode
Pillow
```

The QR code is created using:

```python
img = qrcode.make(short_url)
```

The image is stored temporarily in memory:

```python
buffer = io.BytesIO()
```

It is then converted into Base64:

```python
encoded = base64.b64encode(
    buffer.getvalue()
).decode("utf-8")
```

The frontend receives:

```text
data:image/png;base64,...
```

This means QR image files do not need to be stored on the server.

---

# 11. User Authentication

Authentication uses:

```text
Flask Sessions
+
Werkzeug Password Hashing
```

The application provides:

```text
Register
Login
Logout
Current User Check
```

---

## Registration Flow

```text
Username + Password
        |
        v
Validate Username
        |
        v
Validate Password
        |
        v
Check Existing User
        |
        v
Hash Password
        |
        v
Insert User
        |
        v
Create Session
```

The application requires:

```text
Username: minimum 3 characters

Password: minimum 6 characters
```

---

## Login Flow

```text
Username + Password
        |
        v
Find User
        |
        v
Verify Password Hash
        |
        +-------------+
        |             |
     Invalid        Valid
        |             |
        v             v
       401       Create Session
                      |
                      v
                  Logged In
```

After successful authentication:

```python
session["user_id"] = user["id"]
session["username"] = user["username"]
```

---

## Logout Flow

Logout clears the session:

```python
session.clear()
```

---

# 🔌 API Endpoints

## Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register a user |
| POST | `/api/login` | Login |
| POST | `/api/logout` | Logout |
| GET | `/api/me` | Get current authentication status |

---

## URL APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/urls` | Create a shortened URL |
| GET | `/api/urls` | List URLs belonging to authenticated user |
| GET | `/api/urls/<short_code>/stats` | Get detailed statistics for a URL |
| GET | `/<short_code>` | Redirect to original URL |

---

## Analytics API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics` | Get dashboard analytics |

---

## Health API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check whether the application is running |

---

# 🧪 API Examples

## Register

```http
POST /api/register
Content-Type: application/json
```

Request:

```json
{
  "username": "aldrin",
  "password": "password123"
}
```

Example response:

```json
{
  "message": "Registration successful",
  "username": "aldrin"
}
```

---

## Login

```http
POST /api/login
Content-Type: application/json
```

Request:

```json
{
  "username": "aldrin",
  "password": "password123"
}
```

Example response:

```json
{
  "message": "Login successful",
  "username": "aldrin"
}
```

---

## Create Short URL

```http
POST /api/urls
Content-Type: application/json
```

Request:

```json
{
  "url": "https://www.google.com"
}
```

Example response:

```json
{
  "shortCode": "Ab12Cd",
  "shortUrl": "https://url-shortener-prv0.onrender.com/Ab12Cd",
  "originalUrl": "https://www.google.com",
  "qrCode": "data:image/png;base64,..."
}
```

---

## Get Analytics

```http
GET /api/analytics
```

Example response:

```json
{
  "totalUrls": 5,
  "totalClicks": 27,
  "topUrls": [],
  "dailyClicks": []
}
```

---

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

# 💻 Running Locally

## Prerequisites

Install:

- Python 3.12 or compatible version
- MySQL
- Git
- pip

Docker is optional for normal local development.

---

## 1. Clone the Repository

```bash
git clone https://github.com/ALDRIN1704/url-shortener.git
cd url-shortener
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:

```text
Flask==3.1.0
mysql-connector-python==9.2.0
qrcode[pil]==8.0
gunicorn==23.0.0
```

---

## 3. Create the Local MySQL Database

Open MySQL Workbench.

Run:

```sql
CREATE DATABASE url_shortener;

USE url_shortener;
```

Then execute the project's:

```text
schema.sql
```

Verify the tables:

```sql
SHOW TABLES;
```

Expected:

```text
users
urls
clicks
```

---

## 4. Configure Environment Variables

For local development:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=url_shortener
SECRET_KEY=your_secret_key
```

---

## 5. Run the Application

```bash
python app.py
```

The development server runs at:

```text
http://localhost:5000
```

---

## 6. Test the Application

Test the following flow:

```text
Register
   |
   v
Login
   |
   v
Create Short URL
   |
   v
View QR Code
   |
   v
Open Short URL
   |
   v
Return to Dashboard
   |
   v
Check Updated Click Count
```

---

# 🐳 Docker Implementation

Docker is used to package the application and all Python dependencies into a reproducible environment.

The application uses:

```dockerfile
FROM python:3.12-slim
```

as the base image.

---

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} app:app"]
```

---

## Build Docker Image

From the project directory:

```bash
docker build -t url-shortener .
```

---

## Verify the Image

```bash
docker images
```

Example:

```text
REPOSITORY        TAG
url-shortener     latest
```

---

## Run Docker with Local MySQL

On Windows, the MySQL server running on the host machine is accessed from Docker using:

```text
host.docker.internal
```

Example PowerShell command:

```powershell
docker run `
--name url-shortener-app `
-p 10000:10000 `
-e DB_HOST=host.docker.internal `
-e DB_PORT=3306 `
-e DB_USER=root `
-e DB_PASSWORD="YOUR_PASSWORD" `
-e DB_NAME=url_shortener `
-e SECRET_KEY="local-secret" `
url-shortener
```

Open:

```text
http://localhost:10000
```

---

# ☁️ Production Deployment

The production architecture is:

```text
GitHub
   |
   v
Render
   |
   v
Docker Container
   |
   v
Gunicorn
   |
   v
Flask
   |
   v
Railway MySQL
```

---

# 🚂 Railway MySQL Deployment

Railway is used to host the production MySQL database.

## Step 1 — Create Railway Project

Create a new project in Railway.

Add:

```text
Database
   |
   v
MySQL
```

Railway automatically provisions the MySQL service.

---

## Step 2 — Enable Public Access

Because the application runs on Render and the database runs on Railway, Render needs an externally accessible MySQL endpoint.

Open:

```text
MySQL Service
   |
   v
Settings
   |
   v
Networking
   |
   v
Public Access
```

Enable the TCP proxy.

MySQL listens internally on:

```text
3306
```

Railway then provides:

```text
MYSQL_PUBLIC_URL
```

---

## Step 3 — Create Production Tables

Run:

```text
railway_schema.sql
```

against the Railway MySQL database.

The file creates:

```text
users
urls
clicks
```

and the required indexes.

Verify:

```sql
SHOW TABLES;
```

Expected:

```text
clicks
urls
users
```

---

# 🌐 Render Deployment

Render hosts the Dockerized Flask application.

## Step 1 — Push Source Code to GitHub

Repository:

```text
https://github.com/ALDRIN1704/url-shortener
```

Typical Git commands:

```bash
git init
git add .
git commit -m "Complete URL Shortener"
git branch -M main
git remote add origin https://github.com/ALDRIN1704/url-shortener.git
git push -u origin main
```

---

## Step 2 — Create Render Web Service

In Render:

```text
New
 |
 v
Web Service
 |
 v
Connect GitHub
 |
 v
Select ALDRIN1704/url-shortener
```

Choose:

```text
Runtime: Docker
```

Render automatically reads the repository's `Dockerfile`.

---

## Step 3 — Configure Environment Variables

The production application uses:

```text
DATABASE_URL
SECRET_KEY
```

### `DATABASE_URL`

Copy Railway's:

```text
MYSQL_PUBLIC_URL
```

and store it in Render as:

```text
DATABASE_URL
```

Example structure:

```text
mysql://username:password@hostname:port/database
```

The actual database URL must never be committed to GitHub.

---

### `SECRET_KEY`

Generate a secure Flask secret locally:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Add the generated value to Render as:

```text
SECRET_KEY
```

---

## Step 4 — Render Build Process

During deployment, Render performs:

```text
GitHub Repository
       |
       v
Read Dockerfile
       |
       v
Pull Python 3.12 Image
       |
       v
Install requirements.txt
       |
       v
Copy Application Files
       |
       v
Build Docker Image
       |
       v
Start Gunicorn
       |
       v
Start Flask Application
       |
       v
Connect to Railway MySQL
```

---

## Step 5 — Gunicorn Production Server

The Docker container starts Gunicorn using:

```text
gunicorn --bind 0.0.0.0:${PORT:-10000} app:app
```

Render provides the `PORT` environment variable.

Binding to:

```text
0.0.0.0
```

allows Render to route public traffic to the application.

---

# 🎉 Production Result

The complete production environment is:

```text
HTML + CSS + JavaScript
          |
          v
        Flask
          |
          v
       Gunicorn
          |
          v
        Docker
          |
          v
        Render
          |
          v
    Railway MySQL
```

The deployed application is available at:

**https://url-shortener-prv0.onrender.com/**

---

# ✅ Production Testing Flow

The production application was tested using the following flow:

```text
Open Live Application
        |
        v
Register Account
        |
        v
Login
        |
        v
Enter Long URL
        |
        v
Create Short URL
        |
        v
Display QR Code
        |
        v
Open Short URL
        |
        v
Find URL in Railway MySQL
        |
        v
Increment Click Count
        |
        v
Store Click Event
        |
        v
Redirect to Original URL
        |
        v
Return to Dashboard
        |
        v
Refresh Analytics
        |
        v
View Updated Click Data
```

---

# 🔐 Security Considerations

The application implements several basic security practices:

- Passwords are hashed using Werkzeug
- Plain-text passwords are never stored in MySQL
- SQL queries use parameterized values
- Flask sessions are used for authentication
- URLs belong to individual users
- Analytics endpoints require authentication
- Database credentials are stored using environment variables
- Production credentials are not committed to GitHub
- Flask's secret key is stored as an environment variable
- Short codes have a database-level unique constraint
- Submitted URLs are validated before storage

---

# ⚠️ Current Limitations

The application is designed as an assessment/demo project and can be improved further for large-scale production use.

Current areas for improvement include:

- Stronger short-code generation for very high traffic
- Rate limiting
- CSRF protection
- Email-based account verification
- Password reset flow
- HTTPS-only secure cookie configuration
- Automated tests
- Database migrations
- Connection pooling configuration
- More advanced analytics
- Custom domains

---

# 📈 Future Improvements

Potential improvements include:

- Custom short URL aliases
- URL expiration dates
- Password reset
- Email verification
- Redis caching
- Rate limiting
- Custom domains
- Browser analytics
- Device analytics
- Geographic analytics
- Downloadable QR codes
- URL delete/edit functionality
- Docker Compose
- Automated unit tests
- Integration tests
- CI/CD pipeline
- Admin dashboard
- API keys
- Background analytics processing
- Database migrations using Alembic or Flask-Migrate

---

# 🎯 Concepts Demonstrated

This project demonstrates practical understanding of:

- Python backend development
- Flask application development
- REST API design
- MySQL database modeling
- One-to-many relational database relationships
- SQL queries
- Database indexing
- Authentication
- Password hashing
- Session management
- URL validation
- URL redirection
- Click tracking
- Analytics aggregation
- QR code generation
- Environment variables
- Docker containerization
- Gunicorn
- Cloud databases
- Railway
- Render
- Git
- GitHub
- Production deployment

---

# 📚 Development Journey

The project was implemented progressively:

```text
Requirement Analysis
        |
        v
Database Modeling
        |
        v
Create Flask Backend
        |
        v
Implement URL Shortening
        |
        v
Implement Redirect
        |
        v
Add Click Tracking
        |
        v
Build Analytics
        |
        v
Add QR Generation
        |
        v
Add Authentication
        |
        v
Test Locally
        |
        v
Create Docker Image
        |
        v
Test Docker Locally
        |
        v
Push to GitHub
        |
        v
Create Railway MySQL
        |
        v
Configure Production Database
        |
        v
Deploy Docker App on Render
        |
        v
Configure Environment Variables
        |
        v
Production Testing
```

---

# 💡 What I Learned

Through this project, I gained practical experience building a complete backend application from database design through production deployment.

The project provided hands-on experience with:

```text
Backend Development
        |
        v
API Design
        |
        v
Database Design
        |
        v
Authentication
        |
        v
Analytics
        |
        v
Docker
        |
        v
Cloud Database
        |
        v
Cloud Deployment
        |
        v
Production Debugging
```

One important deployment lesson was understanding the difference between:

```text
localhost MySQL
```

and:

```text
remote Railway MySQL
```

The local application connected to:

```text
localhost:3306
```

while the deployed Render application uses Railway's public MySQL URL through:

```text
DATABASE_URL
```

This allowed the same Flask application to run correctly in both development and production environments.

---

# ✅ Final Result

The completed project includes:

- ✅ User registration
- ✅ User login/logout
- ✅ Password hashing
- ✅ URL shortening
- ✅ Unique short codes
- ✅ URL validation
- ✅ Redirect handling
- ✅ Click tracking
- ✅ Individual click-event storage
- ✅ Analytics dashboard
- ✅ Top URL analytics
- ✅ 7-day click analytics
- ✅ QR code generation
- ✅ User-specific URLs
- ✅ MySQL database
- ✅ Database indexes
- ✅ Docker containerization
- ✅ Gunicorn production server
- ✅ Railway MySQL hosting
- ✅ Render application hosting
- ✅ GitHub repository
- ✅ Production deployment

---

## 🔗 Important Links

**Live Application:**  
https://url-shortener-prv0.onrender.com/

**Health Check:**  
https://url-shortener-prv0.onrender.com/health

**GitHub Repository:**  
https://github.com/ALDRIN1704/url-shortener

**GitHub Profile:**  
https://github.com/ALDRIN1704

---

## 👨‍💻 Author

**Aldrin Lijo E M**

GitHub:  
https://github.com/ALDRIN1704

Repository:  
https://github.com/ALDRIN1704/url-shortener

---

## 📄 Project Summary

```text
Long URL
    |
    v
Flask API
    |
    v
URL Validation
    |
    v
Generate Short Code
    |
    v
MySQL Storage
    |
    v
Short URL + QR Code
    |
    v
Visitor Opens Short URL
    |
    v
Click Tracking
    |
    v
Redirect
    |
    v
Analytics Dashboard
```

**URL Shortener** demonstrates a complete backend development workflow using **Python, Flask, MySQL, Docker, Railway, and Render**, from local development to a publicly accessible production application.
