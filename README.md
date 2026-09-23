<div align="center">

# 🔗 URL Shortener

### A full-stack URL shortening application with authentication, analytics, QR codes, and cloud deployment.

Built using **Python • Flask • MySQL • Docker • Railway • Render**

<br/>

[![Live Demo](https://img.shields.io/badge/Live_Demo-Open_App-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://url-shortener-prv0.onrender.com/)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-MySQL-purple?style=flat-square&logo=railway&logoColor=white)

</div>

---

# 🌐 Live Application

## 🔗 [https://url-shortener-prv0.onrender.com/](https://url-shortener-prv0.onrender.com/)

> The application is deployed using Docker on Render and connected to a MySQL database hosted on Railway.

---

# 📌 Project Overview

This project is a complete **URL Shortener backend application** that allows users to convert long URLs into short, shareable links.

Along with basic URL shortening, the application also supports:

- 🔗 Short URL generation
- ↪️ Automatic redirection
- 📊 Click tracking
- 📈 Analytics dashboard
- 📱 QR code generation
- 🔐 User registration and login
- 👤 User-specific URLs
- 🗃️ MySQL database storage
- 🐳 Docker containerization
- ☁️ Cloud deployment

---

# ✨ Features

| Feature | Description |
|---|---|
| 🔗 URL Shortening | Converts long URLs into unique short links |
| ↪️ Redirect | Redirects short links to their original destination |
| 📊 Click Tracking | Tracks how many times each short URL is visited |
| 📈 Analytics Dashboard | Shows total URLs, total clicks, and recent activity |
| 📱 QR Code | Generates QR codes for shortened URLs |
| 🔐 Authentication | Register, login, and logout functionality |
| 👤 User URLs | Each user can only view their own URLs |
| 🧾 Click History | Stores individual click events |
| ✅ URL Validation | Rejects invalid URLs |
| 🚫 Error Handling | Handles invalid short codes and database errors |
| 🐳 Docker | Runs the application in a production container |
| ☁️ Deployment | Flask app on Render and MySQL on Railway |

---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python |
| Framework | Flask |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Flask Sessions |
| Password Security | Werkzeug |
| QR Generation | Python `qrcode` |
| Production Server | Gunicorn |
| Containerization | Docker |
| Database Hosting | Railway |
| Application Hosting | Render |
| Version Control | Git / GitHub |

---

# 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │      USER       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     RENDER      │
                    │   Web Service   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     DOCKER      │
                    │    Container    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Flask + Gunicorn│
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
      Authentication     URL Shortener     Analytics
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Railway MySQL   │
                    └────────┬────────┘
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
                users       urls      clicks
📁 Project Structure
url-shortener/
│
├── app.py
│
├── Dockerfile
├── .dockerignore
│
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
🚀 Implementation Flow

The project was developed step-by-step, starting with the core URL shortening functionality and then adding advanced features.

1️⃣ Database Design

The application uses three MySQL tables:

users
   │
   │ 1 user can create many URLs
   ▼
urls
   │
   │ 1 URL can receive many clicks
   ▼
clicks
👤 Users Table

Stores registered users.

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Passwords are never stored directly.

Before storing a password, Flask uses Werkzeug:

generate_password_hash(password)

During login:

check_password_hash(
    user["password_hash"],
    password
)
🔗 URLs Table

Stores shortened URLs.

CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    short_code VARCHAR(20)
        NOT NULL
        UNIQUE,

    original_url TEXT
        NOT NULL,

    click_count INT
        NOT NULL
        DEFAULT 0,

    created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

Each URL belongs to a specific user.

🖱️ Clicks Table

Stores every click event.

CREATE TABLE clicks (
    id INT AUTO_INCREMENT PRIMARY KEY,

    url_id INT NOT NULL,

    clicked_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    ip_address VARCHAR(45),

    user_agent TEXT,

    referrer TEXT,

    FOREIGN KEY (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE
);

This allows the application to support more advanced analytics in the future.

2️⃣ Flask Backend

The backend was implemented using Flask.

from flask import Flask

app = Flask(__name__)

Flask handles:

User Authentication
        │
        ▼
URL Creation
        │
        ▼
URL Redirection
        │
        ▼
Click Tracking
        │
        ▼
Analytics
        │
        ▼
QR Code Generation
3️⃣ Database Connection

The application supports both:

Local MySQL
Production Railway MySQL

For local development:

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "url_shortener"
}

For production, the application checks:

DATABASE_URL = os.getenv("DATABASE_URL")

Render stores the production Railway connection string inside:

DATABASE_URL

This keeps database credentials outside the source code.

4️⃣ Short URL Generation

When the user enters a long URL:

https://example.com/some/very/long/path

the backend generates a short code:

aB91xZ

The final short URL becomes:

https://url-shortener-prv0.onrender.com/aB91xZ

The short code and original URL are stored in MySQL.

Short Code Generation

A random combination of letters and numbers is generated:

import random
import string

def generate_code(length=6):

    characters = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        random.choices(
            characters,
            k=length
        )
    )

The database also has:

UNIQUE

on short_code to avoid duplicates.

5️⃣ URL Redirect Flow

When someone opens:

https://url-shortener-prv0.onrender.com/aB91xZ

the application performs:

Short URL
    │
    ▼
Read short_code
    │
    ▼
Search MySQL
    │
    ├───────────────┐
    │               │
  Found          Not Found
    │               │
    ▼               ▼
Update Clicks       404
    │
    ▼
Store Click Event
    │
    ▼
Redirect
    │
    ▼
Original Website
6️⃣ Click Tracking

Every time a short link is opened:

UPDATE urls
SET click_count = click_count + 1
WHERE id = ?;

The application also stores the click event:

INSERT INTO clicks (
    url_id,
    ip_address,
    user_agent,
    referrer
)
VALUES (?, ?, ?, ?);
Why Store Both?

The urls table stores:

click_count

for fast access.

The clicks table stores:

every individual click

for detailed analytics.

This gives both performance and flexibility.

7️⃣ Analytics Dashboard

The analytics dashboard displays:

Total URLs
Total Clicks
Top URLs
Recent Click Activity

Example SQL:

SELECT
    COUNT(*) AS total_urls,
    COALESCE(
        SUM(click_count),
        0
    ) AS total_clicks
FROM urls
WHERE user_id = ?;

Daily click analytics are generated from:

clicks.clicked_at

using:

GROUP BY DATE(clicked_at)
8️⃣ QR Code Generation

The project uses:

qrcode
Pillow

QR generation:

import qrcode

img = qrcode.make(short_url)

The QR code is converted into Base64 and returned to the frontend.

This means QR images do not need to be stored as physical files.

9️⃣ User Authentication

The application supports:

Register
Login
Logout
Registration Flow
Username + Password
        │
        ▼
Validate Input
        │
        ▼
Hash Password
        │
        ▼
Save User
        │
        ▼
Create Session
Login Flow
Username + Password
        │
        ▼
Find User
        │
        ▼
Check Password Hash
        │
        ▼
Create Flask Session
        │
        ▼
Logged In

Flask stores:

session["user_id"] = user["id"]

Each URL is linked to:

user_id

so users only see their own URLs.

🔌 API Endpoints
Authentication
Register
POST /api/register

Request:

{
    "username": "demo",
    "password": "password123"
}
Login
POST /api/login
Logout
POST /api/logout
Current User
GET /api/me
🔗 URL APIs
Create Short URL
POST /api/urls

Request:

{
    "url": "https://www.google.com"
}

Response:

{
    "shortCode": "Ab12Cd",

    "shortUrl":
    "https://url-shortener-prv0.onrender.com/Ab12Cd",

    "originalUrl":
    "https://www.google.com",

    "qrCode":
    "data:image/png;base64,..."
}
Get User URLs
GET /api/urls
Get URL Statistics
GET /api/urls/<short_code>/stats
Analytics Dashboard
GET /api/analytics
Redirect
GET /<short_code>
Health Check
GET /health

Response:

{
    "status": "ok"
}
💻 Local Setup
1️⃣ Clone Repository
git clone YOUR_GITHUB_REPOSITORY_URL

cd url-shortener
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Create MySQL Database

Open MySQL Workbench.

Run:

CREATE DATABASE url_shortener;

Then:

USE url_shortener;

Run:

schema.sql

Verify:

SHOW TABLES;

Expected:

users
urls
clicks
4️⃣ Configure Database

Environment variables:

DB_HOST=localhost

DB_PORT=3306

DB_USER=root

DB_PASSWORD=your_password

DB_NAME=url_shortener

SECRET_KEY=your_secret_key
5️⃣ Run Flask
python app.py

Open:

http://localhost:5000
🐳 Docker Implementation

Docker was added so the application behaves consistently in both local and production environments.

Dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

CMD [
    "sh",
    "-c",
    "gunicorn --bind 0.0.0.0:${PORT:-10000} app:app"
]
Build Docker Image
docker build \
-t url-shortener \
.
Verify Docker Image
docker images

Expected:

REPOSITORY        TAG
url-shortener     latest
Run Docker Locally

For Windows:

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

Open:

http://localhost:10000
☁️ Deployment Architecture

The application is deployed using:

                     GitHub
                       │
                       ▼
                     Render
                       │
                       ▼
                 Docker Container
                       │
                       ▼
                Flask + Gunicorn
                       │
                       ▼
                   Railway
                     MySQL
🚂 Railway MySQL Deployment
Step 1

Create a new Railway project.

Add:

Database
    ↓
MySQL

Railway automatically provisions MySQL.

Step 2

Open:

MySQL Service
    ↓
Settings
    ↓
Networking
    ↓
Public Access

Enable the TCP proxy.

Application port:

3306

Railway generates:

MYSQL_PUBLIC_URL
Step 3

Create the production tables.

Use:

railway_schema.sql

Run:

SHOW TABLES;

Expected:

clicks
urls
users
🌐 Render Deployment
Step 1 — Push to GitHub
git init

git add .

git commit \
-m "Complete URL Shortener"

git branch \
-M main

git remote add origin \
YOUR_GITHUB_REPOSITORY_URL

git push \
-u origin main
Step 2 — Create Render Web Service

In Render:

New
 ↓
Web Service
 ↓
Connect GitHub
 ↓
Select Repository

Choose:

Runtime: Docker

Render automatically detects:

Dockerfile
Step 3 — Environment Variables

Inside:

Render
 ↓
Environment

add:

DATABASE_URL

SECRET_KEY
DATABASE_URL

Copy Railway:

MYSQL_PUBLIC_URL

into Render:

DATABASE_URL

Example format:

mysql://username:password@host:port/database
SECRET_KEY

Generate:

python -c \
"import secrets; print(secrets.token_hex(32))"

Add the generated value to Render.

Step 4 — Deploy

Render performs:

GitHub
   │
   ▼
Read Dockerfile
   │
   ▼
Build Docker Image
   │
   ▼
Install Python Packages
   │
   ▼
Start Gunicorn
   │
   ▼
Flask Application
   │
   ▼
Connect Railway MySQL

Gunicorn starts with:

0.0.0.0:$PORT

This allows Render to expose the Docker container publicly.

🎉 Deployment Result

The application is live at:

🌐 https://url-shortener-prv0.onrender.com/

Production environment:

HTML / CSS / JavaScript
          │
          ▼
       Flask
          │
          ▼
      Gunicorn
          │
          ▼
       Docker
          │
          ▼
       Render
          │
          ▼
   Railway MySQL
🧪 Production Testing Flow

The final application was tested using the following flow:

Open Application
       │
       ▼
Register User
       │
       ▼
Login
       │
       ▼
Enter Long URL
       │
       ▼
Generate Short URL
       │
       ▼
Generate QR Code
       │
       ▼
Open Short URL
       │
       ▼
Track Click
       │
       ▼
Store Click in MySQL
       │
       ▼
Refresh Dashboard
       │
       ▼
Updated Analytics
🔐 Security

The application follows several basic security practices.

✔ Password hashing

✔ Environment variables

✔ Parameterized SQL queries

✔ Flask session authentication

✔ Unique short codes

✔ User-specific URL ownership

✔ Credentials excluded from source code
📈 Future Improvements

Possible future enhancements:

Custom URL aliases

URL expiration

Email verification

Password reset

Rate limiting

Redis caching

Custom domains

Geographical analytics

Browser analytics

Device analytics

Downloadable QR codes

Docker Compose

Automated tests

CI/CD pipeline

Admin dashboard

API keys

Background analytics processing
🎯 Concepts Demonstrated

This project demonstrates practical knowledge of:

Python Backend Development

Flask Framework

REST APIs

MySQL Database Design

Relational Database Relationships

Authentication

Password Hashing

Sessions

URL Redirection

Click Tracking

Analytics

QR Code Generation

Environment Variables

Docker

Gunicorn

Railway

Render

Git / GitHub

Cloud Deployment
🔄 Complete Project Flow
Long URL
   │
   ▼
Flask Backend
   │
   ▼
Generate Unique Code
   │
   ▼
Store in MySQL
   │
   ▼
Return Short URL + QR
   │
   ▼
User Opens Short URL
   │
   ▼
Flask Finds Original URL
   │
   ▼
Increment Click Count
   │
   ▼
Store Click Event
   │
   ▼
Redirect User
   │
   ▼
Analytics Dashboard Updated
📚 What I Learned

Through this project I implemented a complete backend system starting from database design and API development to Docker containerization and cloud deployment.

The project helped me understand how a real application moves through:

Development
    ↓
Database Design
    ↓
Backend APIs
    ↓
Authentication
    ↓
Testing
    ↓
Docker
    ↓
Cloud Database
    ↓
Cloud Deployment
    ↓
Production
👨‍💻 Author

Your Name

GitHub: https://github.com/YOUR_USERNAME

<div align="center">
⭐ URL Shortener

Python • Flask • MySQL • Docker • Railway • Render

<br/>
🔗 Open Live Application
<br/>

Built as a backend development assessment project.

</div> ```

Replace only these two placeholders before pushing:

YOUR_GITHUB_REPOSITORY_URL
YOUR_USERNAME

This version will look much cleaner on GitHub because it has a centered header, badges, architecture diagrams, tables, implementation flow, Docker + Railway + Render deployment steps, API documentation, security notes, and a clear end-to-end explanation.

give full readme.md

Done — here is the full polished README.md file:

Download the complete README.md

It includes the live deployment link, project overview, features, architecture, database design, implementation flow, API documentation, local setup, Docker setup, Railway MySQL deployment, Render deployment, security notes, testing flow, and future improvements. 

README.md
Document

Library
/
README.md

<div align="center">

🔗 URL Shortener
A full-stack URL shortening application with authentication, analytics, QR codes, and cloud deployment.

Built using Python • Flask • MySQL • Docker • Railway • Render

<br/>












</div>

🌐 Live Application
🔗 https://url-shortener-prv0.onrender.com/

The application is deployed using Docker on Render and connected to a MySQL database hosted on Railway.

📌 Project Overview

This project is a complete URL Shortener web application that allows users to convert long URLs into short, shareable links.

Along with the core URL shortening functionality, the project includes:

🔗 Short URL generation
↪️ URL redirection
📊 Click tracking
📈 Analytics dashboard
📱 QR code generation
🔐 User authentication
👤 User-specific links
🗃️ MySQL database storage
🐳 Docker containerization
☁️ Cloud deployment

The main goal of the project was to demonstrate backend development skills including API design, database modeling, authentication, analytics, containerization, and deployment.

✨ Features
Feature	Description
🔗 URL Shortening	Converts long URLs into unique short links
↪️ Redirect	Redirects short links to the original destination
📊 Click Tracking	Tracks how many times each short URL is visited
📈 Analytics Dashboard	Shows total URLs, total clicks, and recent activity
📱 QR Code Generation	Generates a QR code for every short URL
🔐 Authentication	Register, login, and logout functionality
👤 User-specific URLs	Each user can only access their own URLs
🧾 Click History	Stores individual click events
✅ URL Validation	Rejects invalid URLs
🚫 Error Handling	Handles invalid short codes and database errors
🐳 Docker Support	Runs consistently inside a production container
☁️ Cloud Deployment	Flask app on Render and MySQL on Railway
🛠️ Tech Stack
Category	Technology
Backend	Python
Web Framework	Flask
Database	MySQL
Frontend	HTML, CSS, JavaScript
Authentication	Flask Sessions
Password Security	Werkzeug
QR Generation	qrcode + Pillow
Production Server	Gunicorn
Containerization	Docker
Database Hosting	Railway
Application Hosting	Render
Version Control	Git / GitHub
🏗️ System Architecture
                    ┌─────────────────┐
                    │      USER       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     RENDER      │
                    │   Web Service   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     DOCKER      │
                    │    Container    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Flask + Gunicorn│
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
      Authentication     URL Shortener     Analytics
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Railway MySQL   │
                    └────────┬────────┘
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
                users       urls      clicks
📁 Project Structure
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
🚀 Implementation Flow

The project was developed in small stages. The core backend functionality was completed first, and then authentication, analytics, QR codes, Docker, and deployment were added.

1️⃣ Database Design

The application uses three MySQL tables:

users
   │
   │ one user can create many URLs
   ▼
urls
   │
   │ one URL can receive many clicks
   ▼
clicks
👤 users Table

The users table stores registered users.

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Passwords are never stored as plain text.

Werkzeug is used to hash passwords before saving them:

generate_password_hash(password)

During login, the password is checked using:

check_password_hash(user["password_hash"], password)
🔗 urls Table

The urls table stores shortened URLs.

CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    short_code VARCHAR(20) NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    click_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

Each URL belongs to one authenticated user.

The short_code column is marked as UNIQUE so that duplicate short codes cannot be stored.

🖱️ clicks Table

The clicks table stores every click event.

CREATE TABLE clicks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_id INT NOT NULL,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT,

    FOREIGN KEY (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE
);

This makes it possible to build more advanced analytics later, such as:

clicks by date
clicks by browser
referrer tracking
device information
geographic analytics
2️⃣ Flask Backend

The backend was implemented using Flask.

from flask import Flask

app = Flask(__name__)

Flask handles:

Authentication
      ↓
URL Creation
      ↓
URL Redirection
      ↓
Click Tracking
      ↓
Analytics
      ↓
QR Code Generation

The backend communicates with MySQL using mysql-connector-python.

3️⃣ Database Connection

The application supports both local development and production deployment.

Local Development

For local development, the application uses environment variables such as:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=url_shortener
Production

In production, the application reads:

DATABASE_URL = os.getenv("DATABASE_URL")

The value of DATABASE_URL is the public Railway MySQL connection URL.

This makes it possible to use the same code locally and in production without storing database credentials inside the source code.

4️⃣ Short URL Generation

When a user enters a long URL:

https://example.com/some/very/long/path

the backend generates a random short code:

aB91xZ

The final short URL becomes:

https://url-shortener-prv0.onrender.com/aB91xZ

The original URL and short code are then stored in MySQL.

Short Code Generation

A random combination of letters and numbers is generated:

import random
import string

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(
        random.choices(characters, k=length)
    )

The database also has a UNIQUE constraint on short_code.

5️⃣ URL Redirect Flow

When someone opens a short URL, the backend extracts the short code and searches for it in MySQL.

Short URL
    │
    ▼
Read short_code
    │
    ▼
Search MySQL
    │
    ├───────────────┐
    │               │
  Found          Not Found
    │               │
    ▼               ▼
Update Clicks      404
    │
    ▼
Store Click Event
    │
    ▼
Redirect
    │
    ▼
Original Website

The Flask redirect route performs the following steps:

1. Find the URL using short_code
2. Return 404 if the code does not exist
3. Increment the URL's click counter
4. Store a new click event
5. Redirect to the original URL
6️⃣ Click Tracking

Every time a short link is opened, the application updates:

UPDATE urls
SET click_count = click_count + 1
WHERE id = ?;

It also records an individual click event:

INSERT INTO clicks (
    url_id,
    ip_address,
    user_agent,
    referrer
)
VALUES (?, ?, ?, ?);
Why Store Both?

The urls table stores:

click_count

This allows the application to quickly display the total number of clicks.

The clicks table stores:

every individual click

This allows detailed analytics to be generated later.

7️⃣ Analytics Dashboard

The analytics dashboard displays:

total number of URLs
total number of clicks
top-performing URLs
recent click activity

Example aggregation query:

SELECT
    COUNT(*) AS total_urls,
    COALESCE(SUM(click_count), 0) AS total_clicks
FROM urls
WHERE user_id = ?;

Daily click activity is calculated from the clicks table using:

GROUP BY DATE(clicked_at)

Flow:

clicks table
    │
    ▼
SQL aggregation
    │
    ▼
Analytics API
    │
    ▼
Dashboard
8️⃣ QR Code Generation

Every generated short URL also receives a QR code.

The project uses:

qrcode
Pillow

Example:

import qrcode

img = qrcode.make(short_url)

The generated image is converted to Base64 and returned to the frontend.

This means QR images do not need to be stored as files on the server.

9️⃣ User Authentication

The application supports:

Register
Login
Logout
Registration Flow
Username + Password
        │
        ▼
Validate Input
        │
        ▼
Hash Password
        │
        ▼
Save User in MySQL
        │
        ▼
Create Session
Login Flow
Username + Password
        │
        ▼
Find User
        │
        ▼
Check Password Hash
        │
        ▼
Create Flask Session
        │
        ▼
Logged In

After successful login:

session["user_id"] = user["id"]

Each shortened URL stores the user ID, so every user sees only the links created from their own account.

🔌 API Endpoints
Authentication APIs
Register
POST /api/register

Example request:

{
    "username": "demo",
    "password": "password123"
}
Login
POST /api/login
Logout
POST /api/logout
Current User
GET /api/me
URL APIs
Create Short URL
POST /api/urls

Example request:

{
    "url": "https://www.google.com"
}

Example response:

{
    "shortCode": "Ab12Cd",
    "shortUrl": "https://url-shortener-prv0.onrender.com/Ab12Cd",
    "originalUrl": "https://www.google.com",
    "qrCode": "data:image/png;base64,..."
}
Get User URLs
GET /api/urls
Get URL Statistics
GET /api/urls/<short_code>/stats
Analytics Dashboard
GET /api/analytics
Redirect
GET /<short_code>
Health Check
GET /health

Example response:

{
    "status": "ok"
}
💻 Running the Project Locally
1️⃣ Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL
cd url-shortener
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Create the Local MySQL Database

Open MySQL Workbench and run:

CREATE DATABASE url_shortener;
USE url_shortener;

Then execute:

schema.sql

Verify:

SHOW TABLES;

Expected:

users
urls
clicks
4️⃣ Configure Local Database Variables

Example environment variables:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=url_shortener
SECRET_KEY=your_secret_key
5️⃣ Start Flask
python app.py

Open:

http://localhost:5000
🐳 Docker Implementation

Docker was added so the application behaves consistently in development and production.

The project uses the following Dockerfile:

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} app:app"]
Build the Docker Image
docker build -t url-shortener .
Verify the Image
docker images

Expected:

REPOSITORY        TAG
url-shortener     latest
Run Docker Locally

For Windows:

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

Open:

http://localhost:10000
☁️ Deployment Architecture

The production deployment follows this architecture:

                     GitHub
                       │
                       ▼
                     Render
                       │
                       ▼
                 Docker Container
                       │
                       ▼
                Flask + Gunicorn
                       │
                       ▼
                   Railway
                     MySQL
🚂 Railway MySQL Deployment
Step 1 — Create a Railway Project

Create a new Railway project.

Add:

Database
   ↓
MySQL

Railway automatically provisions a MySQL server.

Step 2 — Enable Public Access

Since the Flask application is hosted on Render, the MySQL database must be accessible externally.

Open:

MySQL Service
   ↓
Settings
   ↓
Networking
   ↓
Public Access

Enable the TCP proxy.

The MySQL application port is:

3306

Railway then generates:

MYSQL_PUBLIC_URL
Step 3 — Create Production Tables

Use:

railway_schema.sql

to create:

users
urls
clicks

Verify using:

SHOW TABLES;

Expected:

clicks
urls
users
🌐 Render Deployment
Step 1 — Push the Project to GitHub
git init
git add .
git commit -m "Complete URL Shortener"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
Step 2 — Create a Render Web Service

In Render:

New
 ↓
Web Service
 ↓
Connect GitHub
 ↓
Select Repository

Choose:

Runtime: Docker

Render automatically detects the project's:

Dockerfile
Step 3 — Configure Environment Variables

Inside Render:

Environment

add:

DATABASE_URL
SECRET_KEY
DATABASE_URL

Copy the Railway:

MYSQL_PUBLIC_URL

and paste it into Render as:

DATABASE_URL

Example format:

mysql://username:password@host:port/database

The real value must never be committed to GitHub.

SECRET_KEY

Generate a secure secret:

python -c "import secrets; print(secrets.token_hex(32))"

Paste the result into Render.

Step 4 — Deploy

Render then performs:

GitHub
   │
   ▼
Read Dockerfile
   │
   ▼
Build Docker Image
   │
   ▼
Install Dependencies
   │
   ▼
Start Gunicorn
   │
   ▼
Run Flask Application
   │
   ▼
Connect to Railway MySQL

Gunicorn listens on:

0.0.0.0:$PORT

which allows Render to expose the container publicly.

🎉 Deployment Result

The application is live at:

🌐 https://url-shortener-prv0.onrender.com/

Production stack:

HTML / CSS / JavaScript
          │
          ▼
        Flask
          │
          ▼
       Gunicorn
          │
          ▼
        Docker
          │
          ▼
        Render
          │
          ▼
    Railway MySQL
🧪 Production Testing Flow

The final deployed application was tested using the following flow:

Open Application
       │
       ▼
Register User
       │
       ▼
Login
       │
       ▼
Enter Long URL
       │
       ▼
Generate Short URL
       │
       ▼
Generate QR Code
       │
       ▼
Open Short URL
       │
       ▼
Track Click
       │
       ▼
Store Click in MySQL
       │
       ▼
Refresh Dashboard
       │
       ▼
Updated Analytics
🔐 Security Considerations

The application includes several basic security practices:

✅ Password hashing
✅ Environment variables for credentials
✅ Parameterized SQL queries
✅ Flask session authentication
✅ Unique short code constraint
✅ User-specific URL ownership
✅ Database passwords excluded from source code
✅ Production secrets stored in Render environment variables
📈 Future Improvements

Possible future enhancements include:

custom URL aliases
URL expiration
email verification
password reset
Redis caching
rate limiting
custom domains
geographic analytics
browser analytics
device analytics
downloadable QR codes
Docker Compose
automated testing
CI/CD pipeline
admin dashboard
API keys
background analytics processing
🎯 Concepts Demonstrated

This project demonstrates practical knowledge of:

Python Backend Development

Flask Framework

REST API Design

MySQL Database Modeling

Relational Database Relationships

Authentication

Password Hashing

Sessions

URL Redirection

Click Tracking

Analytics

QR Code Generation

Environment Variables

Docker

Gunicorn

Railway

Render

Git / GitHub

Cloud Deployment
🔄 Complete Project Flow
Long URL
   │
   ▼
Flask Backend
   │
   ▼
Generate Unique Code
   │
   ▼
Store in MySQL
   │
   ▼
Return Short URL + QR
   │
   ▼
User Opens Short URL
   │
   ▼
Flask Finds Original URL
   │
   ▼
Increment Click Count
   │
   ▼
Store Click Event
   │
   ▼
Redirect User
   │
   ▼
Analytics Dashboard Updated
📚 What I Learned

Through this project, I implemented a complete backend system starting from database design and API development to Docker containerization and cloud deployment.

The project helped me understand how a real application moves through:

Development
    ↓
Database Design
    ↓
Backend APIs
    ↓
Authentication
    ↓
Testing
    ↓
Docker
    ↓
Cloud Database
    ↓
Cloud Deployment
    ↓
Production

It also helped demonstrate how different services work together in a real deployment:

GitHub
   ↓
Render
   ↓
Docker
   ↓
Flask + Gunicorn
   ↓
Railway MySQL
✅ Final Result

The finished project includes:

✔ URL Shortening
✔ Redirect Handling
✔ Click Tracking
✔ Analytics Dashboard
✔ QR Code Generation
✔ Registration
✔ Login / Logout
✔ User-specific URLs
✔ MySQL Database
✔ Docker Containerization
✔ Railway Database Hosting
✔ Render Application Hosting
✔ Production Deployment
👨‍💻 Author

ALDRIN LIJO

GitHub: https://github.com/ALDRIN1704

<div align="center">

🔗 URL Shortener
Python • Flask • MySQL • Docker • Railway • Render

<br/>

🌐 Open Live Application

<br/>

Built as a backend development assessment project.

</div>
