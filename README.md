# URL Shortener - Full Assessment Version

Built with Python, Flask and MySQL.

## Included features

- Generate short URLs
- Redirect to original URLs
- Track click count
- Store click events
- Analytics dashboard
- QR code generation
- User registration/login/logout
- Per-user URL ownership
- URL validation

## Install

```bash
pip install -r requirements.txt
```

## MySQL

Run `schema.sql` in MySQL Workbench.

Then edit the password in `app.py`:

```python
"password": "YOUR_PASSWORD"
```

## Start

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

## Demo flow

1. Register a new account.
2. Enter a long URL.
3. Create the short URL.
4. QR code appears automatically.
5. Open the short URL several times.
6. Return to the dashboard.
7. Refresh to see click analytics.

## Main APIs

- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `POST /api/urls`
- `GET /api/urls`
- `GET /api/analytics`
- `GET /api/urls/<short_code>/stats`
- `GET /<short_code>`
