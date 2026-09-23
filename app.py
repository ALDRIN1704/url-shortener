from flask import Flask, request, jsonify, redirect, render_template, session
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse, unquote
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import os
import io
import base64
import qrcode

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    parsed_db = urlparse(DATABASE_URL)
    DB_CONFIG = {
        "host": parsed_db.hostname,
        "port": parsed_db.port or 3306,
        "user": unquote(parsed_db.username or ""),
        "password": unquote(parsed_db.password or ""),
        "database": parsed_db.path.lstrip("/")
    }
else:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "1704@Aldrin"),
        "database": os.getenv("DB_NAME", "url_shortener")
    }

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def is_valid_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

def current_user_id():
    return session.get("user_id")

def require_login_json():
    if not current_user_id():
        return jsonify({"error": "Authentication required"}), 401
    return None

def create_unique_code(cursor):
    for _ in range(10):
        code = generate_code()
        cursor.execute("SELECT id FROM urls WHERE short_code = %s", (code,))
        if cursor.fetchone() is None:
            return code
    raise RuntimeError("Could not generate a unique short code")

def make_qr_data_url(text):
    img = qrcode.make(text)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

@app.route("/")
def home():
    return render_template("index.html", logged_in=bool(current_user_id()), username=session.get("username"))

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Username already exists"}), 409

        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        connection.commit()

        session["user_id"] = cursor.lastrowid
        session["username"] = username

        return jsonify({"message": "Registration successful", "username": username}), 201

    except Error as exc:
        if connection:
            connection.rollback()
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid username or password"}), 401

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return jsonify({"message": "Login successful", "username": user["username"]})

    except Error as exc:
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route("/api/me")
def me():
    return jsonify({
        "loggedIn": bool(current_user_id()),
        "username": session.get("username")
    })

@app.route("/api/urls", methods=["POST"])
def create_url():
    auth_error = require_login_json()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    original_url = (data.get("url") or "").strip()

    if not original_url:
        return jsonify({"error": "URL is required"}), 400
    if not is_valid_url(original_url):
        return jsonify({"error": "Please provide a valid http:// or https:// URL"}), 400

    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        short_code = create_unique_code(cursor)

        cursor.execute(
            """
            INSERT INTO urls (user_id, short_code, original_url)
            VALUES (%s, %s, %s)
            """,
            (current_user_id(), short_code, original_url)
        )
        connection.commit()

        short_url = request.host_url.rstrip("/") + "/" + short_code
        qr_code = make_qr_data_url(short_url)

        return jsonify({
            "shortCode": short_code,
            "shortUrl": short_url,
            "originalUrl": original_url,
            "qrCode": qr_code
        }), 201

    except Error as exc:
        if connection:
            connection.rollback()
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/api/urls", methods=["GET"])
def list_urls():
    auth_error = require_login_json()
    if auth_error:
        return auth_error

    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, short_code, original_url, click_count, created_at
            FROM urls
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (current_user_id(),)
        )
        urls = cursor.fetchall()

        for item in urls:
            item["shortUrl"] = request.host_url.rstrip("/") + "/" + item["short_code"]
            item["created_at"] = item["created_at"].isoformat() if item["created_at"] else None

        return jsonify(urls)

    except Error as exc:
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/api/analytics", methods=["GET"])
def analytics():
    auth_error = require_login_json()
    if auth_error:
        return auth_error

    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT COUNT(*) AS total_urls,
                   COALESCE(SUM(click_count), 0) AS total_clicks
            FROM urls
            WHERE user_id = %s
            """,
            (current_user_id(),)
        )
        summary = cursor.fetchone()

        cursor.execute(
            """
            SELECT short_code, original_url, click_count
            FROM urls
            WHERE user_id = %s
            ORDER BY click_count DESC, created_at DESC
            LIMIT 5
            """,
            (current_user_id(),)
        )
        top_urls = cursor.fetchall()

        cursor.execute(
            """
            SELECT DATE(c.clicked_at) AS day, COUNT(*) AS clicks
            FROM clicks c
            JOIN urls u ON u.id = c.url_id
            WHERE u.user_id = %s
              AND c.clicked_at >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(c.clicked_at)
            ORDER BY day ASC
            """,
            (current_user_id(),)
        )
        daily = cursor.fetchall()

        for row in daily:
            row["day"] = row["day"].isoformat() if row["day"] else None

        return jsonify({
            "totalUrls": summary["total_urls"],
            "totalClicks": int(summary["total_clicks"]),
            "topUrls": top_urls,
            "dailyClicks": daily
        })

    except Error as exc:
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/api/urls/<short_code>/stats", methods=["GET"])
def get_stats(short_code):
    auth_error = require_login_json()
    if auth_error:
        return auth_error

    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, short_code, original_url, click_count, created_at
            FROM urls
            WHERE short_code = %s AND user_id = %s
            """,
            (short_code, current_user_id())
        )
        url = cursor.fetchone()

        if not url:
            return jsonify({"error": "Short URL not found"}), 404

        cursor.execute(
            """
            SELECT DATE(clicked_at) AS day, COUNT(*) AS clicks
            FROM clicks
            WHERE url_id = %s
            GROUP BY DATE(clicked_at)
            ORDER BY day DESC
            LIMIT 7
            """,
            (url["id"],)
        )
        daily_clicks = cursor.fetchall()

        for row in daily_clicks:
            row["day"] = row["day"].isoformat() if row["day"] else None

        short_url = request.host_url.rstrip("/") + "/" + url["short_code"]

        return jsonify({
            "shortCode": url["short_code"],
            "shortUrl": short_url,
            "originalUrl": url["original_url"],
            "clicks": url["click_count"],
            "createdAt": url["created_at"].isoformat() if url["created_at"] else None,
            "dailyClicks": daily_clicks,
            "qrCode": make_qr_data_url(short_url)
        })

    except Error as exc:
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/<short_code>")
def redirect_to_url(short_code):
    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, original_url FROM urls WHERE short_code = %s",
            (short_code,)
        )
        url = cursor.fetchone()

        if not url:
            return jsonify({"error": "Short URL not found"}), 404

        cursor.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE id = %s",
            (url["id"],)
        )

        cursor.execute(
            """
            INSERT INTO clicks (url_id, ip_address, user_agent, referrer)
            VALUES (%s, %s, %s, %s)
            """,
            (
                url["id"],
                request.remote_addr,
                request.headers.get("User-Agent"),
                request.referrer
            )
        )

        connection.commit()
        return redirect(url["original_url"])

    except Error as exc:
        if connection:
            connection.rollback()
        return jsonify({"error": f"Database error: {exc}"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
