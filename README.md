# URLShortener

A URL-shortening application built with **Python, Flask, and MySQL**. It
provides a REST API for creating short codes for long URLs and managing
stored URL mappings.

The backend separates request handling, URL processing, and database
operations into individual Python modules. A frontend is included in the
`templates/` and `static/` directories.

## Features

-   Generate a five-character short code using letters and numbers.
-   Validate submitted URLs before storing them.
-   Store URL mappings in a MySQL database.
-   Retrieve a URL mapping by its short code.
-   Update the destination URL associated with a short code.
-   Delete a stored URL mapping.
-   Retrieve URL information and access-count statistics.
-   Return JSON responses from the REST API.
-   Configure cross-origin requests for a local frontend.

## Technology Stack

  Technology                 Purpose
  -------------------------- ------------------------------------------------
  Python                     Backend application logic
  Flask                      REST API and routing
  Flask-CORS                 Cross-origin requests from the frontend
  MySQL                      Persistent URL mapping storage
  `mysql-connector-python`   Connects Python to MySQL
  `python-dotenv`            Loads configuration from environment variables
  `validators`               Validates submitted URLs
  HTML / JavaScript          Frontend interface and API requests

## Project Structure

``` text
URLShortener/
├── REST_API.py       # Flask application and API endpoints
├── db.py             # MySQL connection and database operations
├── parse_URL.py      # Short-code generation and URL processing
├── requirements.txt  # Python dependencies with pinned versions
├── templates/        # HTML templates
├── static/           # Frontend assets, including JavaScript
└── .gitignore
```

## Getting Started

### Prerequisites

-   Python 3
-   MySQL Server
-   A frontend development server (for example, Visual Studio Code Live
    Server) if you want to use the browser interface

### 1. Clone the repository

``` bash
git clone https://github.com/Grotle4/URLShortener.git
cd URLShortener
```

### 2. Create and activate a virtual environment

``` bash
python -m venv .venv
```

On Windows PowerShell:

``` powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

``` bash
source .venv/bin/activate
```

### 3. Install dependencies

Install the project's pinned Python dependencies from
`requirements.txt`:

``` bash
python -m pip install -r requirements.txt
```

Using a virtual environment is recommended so these packages do not
affect other Python projects.

### 4. Configure MySQL

Start MySQL and create a database for the application. For example:

``` sql
CREATE DATABASE urlshortener;
```

The database module expects a table named `urls` with fields
corresponding to the database queries. Ensure the table schema matches
`db.py`, including the fields used for the original URL, short code,
timestamps, and access count.

### 5. Configure environment variables

Create a `.env` file in the project root with the database settings read
by `db.py`. The expected variable names are:

``` dotenv
USER=your_mysql_username
PASSWORD=your_mysql_password
HOST=localhost
DB=urlshortener
```

Replace these example values with your own MySQL credentials and
database name. Keep `.env` out of version control and never commit real
credentials.

### 6. Start the API

From the repository root, run:

``` bash
python REST_API.py
```

The Flask application listens on port `5000`:

``` text
http://127.0.0.1:5000
```

The root route (`/`) currently returns a 404 response. Use the API
endpoints below to interact with the service.

### 7. Start the frontend

Serve the frontend files with your preferred local development server.
The current CORS configuration in `REST_API.py` allows this origin:

``` text
http://127.0.0.1:5500
```

If your frontend runs on a different origin, update the CORS
configuration to match it. For production, allow only trusted origins.

## REST API

Base URL:

``` text
http://127.0.0.1:5000
```

Requests that send a body should use JSON and the
`Content-Type: application/json` header.

### Endpoints

  ------------------------------------------------------------------------------
  Method                  Endpoint                       Description
  ----------------------- ------------------------------ -----------------------
  `POST`                  `/shorten`                     Create a shortened URL
                                                         mapping

  `GET`                   `/shorten/<shortcode>`         Retrieve a mapping by
                                                         short code

  `PUT`                   `/shorten/<shortcode>`         Update the destination
                                                         URL for a short code

  `DELETE`                `/shorten/<shortcode>`         Delete a mapping

  `GET`                   `/shorten/<shortcode>/stats`   Retrieve mapping
                                                         information and
                                                         statistics
  ------------------------------------------------------------------------------

### Create a short URL

**Request**

``` http
POST /shorten
Content-Type: application/json
```

``` json
{
  "url": "https://www.example.com/some/long/path"
}
```

The API processes the submitted URL and attempts to store a short-code
mapping in MySQL.

**Example success response**

``` json
{
  "message": "Success, entry with short code aB12x has been added!"
}
```

The short code shown is illustrative; the application generates the
actual code.

### Retrieve a mapping

``` http
GET /shorten/<shortcode>
```

Replace `<shortcode>` with the code to look up. A successful request
returns the stored record as JSON.

### Update a mapping

**Request**

``` http
PUT /shorten/<shortcode>
Content-Type: application/json
```

``` json
{
  "url": "https://www.example.com/new-destination"
}
```

The API passes the supplied destination URL to the database update logic
for the specified short code.

### Delete a mapping

``` http
DELETE /shorten/<shortcode>
```

Deletes the record associated with the supplied short code.

### Retrieve statistics

``` http
GET /shorten/<shortcode>/stats
```

Returns the record and statistics provided by the database retrieval
logic, including the access-count information if maintained by the
database layer.

Refer to `REST_API.py`, `parse_URL.py`, and `db.py` for the precise
response formats and database behavior.

## How It Works

1.  The frontend sends a URL to the Flask API.
2.  `REST_API.py` receives the request and passes URL processing to
    `parse_URL.py`.
3.  The URL-processing logic generates a short code.
4.  `db.py` handles database operations and stores or retrieves the
    mapping.
5.  The API returns a JSON response to the frontend.

The current API exposes endpoints for managing and looking up short
codes. A public redirect route at the root of the domain (for example,
`/<shortcode>`) is not currently defined in `REST_API.py`.

## Troubleshooting and Notes

-   Confirm MySQL is running and reachable with the credentials in
    `.env`.
-   Confirm the database and table schema match the SQL operations in
    `db.py`.
-   Ensure the frontend origin matches the CORS allowlist in
    `REST_API.py`.
-   Check the Flask terminal for backend errors when a request fails.
-   API responses use different status codes depending on the endpoint
    and outcome; clients should handle unsuccessful responses.
-   Do not expose the development server directly to the public internet
    without reviewing authentication, access controls, input handling,
    logging, and deployment configuration.

## Potential Improvements

-   Add a database schema or migration script so the table can be
    created consistently.
-   Add automated tests for API endpoints, URL validation, and database
    operations.
-   Improve validation for missing or malformed JSON fields.
-   Enforce short-code uniqueness with a database constraint.
-   Add a dedicated redirect endpoint for visiting shortened links.
-   Document access-count behavior and the exact statistics response.
-   Add production deployment configuration and security settings.

## License

Add a `LICENSE` file if you intend to specify how others may use,
modify, or distribute this project.
