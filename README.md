# CodeCraftHub

A beginner-friendly REST API for developers to track courses they want to learn. Built with Python and Flask, with no database required — all data is stored in a simple JSON file.

> If you are learning REST APIs for the first time, you are in the right place. This project is intentionally small and readable so that every line makes sense before you move on to bigger frameworks.

---

## Table of Contents

1. [What Is CodeCraftHub?](#what-is-codecrafthub)
2. [Features](#features)
3. [What You Will Learn](#what-you-will-learn)
4. [Project Structure](#project-structure)
5. [Requirements](#requirements)
6. [Installation](#installation)
7. [Running the Application](#running-the-application)
8. [API Endpoints](#api-endpoints)
9. [Request and Response Examples](#request-and-response-examples)
10. [Testing the API](#testing-the-api)
11. [How the JSON File Works](#how-the-json-file-works)
12. [Troubleshooting](#troubleshooting)
13. [Glossary for Beginners](#glossary-for-beginners)

---

## What Is CodeCraftHub?

CodeCraftHub is a course tracker API. You can use it to keep a personal list of developer courses — what you want to learn, what you are currently working on, and what you have already finished.

There is no login screen, no database to set up, and no frontend to build. You interact with it entirely through HTTP requests, which makes it a perfect project for understanding how REST APIs work in practice.

---

## Features

- Add new courses with a name, description, target completion date, and status
- View all your courses at once, or filter by status
- Look up any single course by its ID
- Update any field on a course, including marking it complete
- Delete courses you no longer need
- Automatic JSON file creation on first run — nothing to set up manually
- Clear error messages when something goes wrong, so you always know what to fix

---

## What You Will Learn

By working through this project, you will understand:

- How Flask handles incoming HTTP requests and sends back responses
- What REST means and why the four HTTP methods (GET, POST, PUT, DELETE) map to four actions (Read, Create, Update, Delete)
- How to read and write data to a JSON file as a lightweight alternative to a database
- What HTTP status codes mean and why returning the right one matters (200 vs 201 vs 404 vs 400)
- How to validate user input before saving it
- How to test an API from the command line using `curl`

---

## Project Structure

```
CodeCraftHub/
│
├── app.py              ← The entire application lives here.
│                         All five API routes, two file helper functions,
│                         and input validation are written in this one file.
│                         Intentionally kept in one place for beginners.
│
├── data/
│   └── courses.json    ← Your data file. Created automatically the first
│                         time you start the app. Open it any time to see
│                         exactly what the API is storing.
│
├── requirements.txt    ← Lists the one Python package this project needs:
│                         Flask. Run `pip install -r requirements.txt`
│                         to install it.
│
└── README.md           ← This file.
```

### Why everything is in one file

Real Flask projects split code across many files (routes, models, helpers, etc.). That structure is correct for large apps but confusing when you are just starting out. One file means you can read the whole application top to bottom without jumping around. Once you understand how it works, splitting it up will make more sense.

---

## Requirements

Before you begin, make sure you have:

| Requirement | Minimum version | How to check |
|---|---|---|
| Python | 3.8 or higher | `python --version` |
| pip | Comes with Python | `pip --version` |

You do not need to install anything else before starting. Flask is the only dependency, and the installation steps below handle it.

---

## Installation

Follow these steps exactly. Each one builds on the last.

### Step 1 — Download or clone the project

If you have Git installed:
```bash
git clone https://github.com/your-username/CodeCraftHub.git
cd CodeCraftHub
```

If you do not have Git, download the ZIP file from GitHub, unzip it, and open a terminal inside the project folder.

### Step 2 — Create a virtual environment

A virtual environment keeps this project's dependencies separate from everything else on your computer. This is good practice and avoids conflicts with other Python projects.

**On macOS or Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

You will know the virtual environment is active when you see `(venv)` at the start of your terminal prompt, like this:
```
(venv) C:\Projects\CodeCraftHub>
```

### Step 3 — Install Flask

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs Flask. You should see output ending with:
```
Successfully installed flask-x.x.x ...
```

### Step 4 — Verify the installation

```bash
python -c "import flask; print(flask.__version__)"
```

If a version number prints (e.g. `3.0.2`), Flask is installed correctly.

---

## Running the Application

```bash
python app.py
```

You should see:
```
🚀 CodeCraftHub API is running at http://127.0.0.1:5000
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

The server is now live. Open a second terminal window and use it to send requests. Keep this first terminal open — it is your server, and it shows a log of every request that comes in.

### What `debug=True` means

The app runs with `debug=True`, which does two things:

1. The server restarts automatically every time you save `app.py`, so you do not have to stop and restart it manually while developing.
2. If the code crashes, Flask shows a detailed error page instead of a generic one.

**Important:** Never use `debug=True` when deploying an app to the internet. It is only for local development.

### Stopping the server

Press `Ctrl + C` in the terminal where the server is running.

---

## API Endpoints

A quick-reference table of every endpoint.

| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/api/courses` | Add a new course |
| `GET` | `/api/courses` | Get all courses (optional status filter) |
| `GET` | `/api/courses/<id>` | Get one course by its ID |
| `PUT` | `/api/courses/<id>` | Update one or more fields of a course |
| `DELETE` | `/api/courses/<id>` | Delete a course permanently |

### Course fields

Every course has these six fields:

| Field | Type | Set by | Description |
|---|---|---|---|
| `id` | Integer | Auto-generated | Unique identifier, starts at 1 and increments |
| `name` | String | You | The name of the course |
| `description` | String | You | A short description of what it covers |
| `target_date` | String | You | When you want to finish it (`YYYY-MM-DD` format) |
| `status` | String | You | One of: `Not Started`, `In Progress`, `Completed` |
| `created_at` | String | Auto-generated | UTC timestamp of when the course was added |

---

## Request and Response Examples

### POST /api/courses — Add a course

**Request body:**
```json
{
  "name": "Flask for Beginners",
  "description": "Learn Flask routing, templates, and REST API basics",
  "target_date": "2026-09-01",
  "status": "Not Started"
}
```

**Successful response (HTTP 201):**
```json
{
  "message": "Course created successfully.",
  "course": {
    "id": 1,
    "name": "Flask for Beginners",
    "description": "Learn Flask routing, templates, and REST API basics",
    "target_date": "2026-09-01",
    "status": "Not Started",
    "created_at": "2026-06-12T10:00:00Z"
  }
}
```

---

### GET /api/courses — Get all courses

**Optional query parameter:** `?status=In Progress`

**Successful response (HTTP 200):**
```json
{
  "total": 2,
  "courses": [
    {
      "id": 1,
      "name": "Flask for Beginners",
      "status": "Not Started",
      ...
    },
    {
      "id": 2,
      "name": "React Fundamentals",
      "status": "In Progress",
      ...
    }
  ]
}
```

---

### GET /api/courses/1 — Get one course

**Successful response (HTTP 200):**
```json
{
  "course": {
    "id": 1,
    "name": "Flask for Beginners",
    "description": "Learn Flask routing, templates, and REST API basics",
    "target_date": "2026-09-01",
    "status": "Not Started",
    "created_at": "2026-06-12T10:00:00Z"
  }
}
```

**Course not found (HTTP 404):**
```json
{
  "error": "Course with ID 99 not found."
}
```

---

### PUT /api/courses/1 — Update a course

You only need to send the fields you want to change. Everything else stays the same.

**Request body (partial update):**
```json
{
  "status": "In Progress"
}
```

**Successful response (HTTP 200):**
```json
{
  "message": "Course updated successfully.",
  "course": {
    "id": 1,
    "name": "Flask for Beginners",
    "status": "In Progress",
    ...
  }
}
```

---

### DELETE /api/courses/1 — Delete a course

No request body needed.

**Successful response (HTTP 200):**
```json
{
  "message": "Course 'Flask for Beginners' deleted successfully.",
  "course": { ... }
}
```

---

## Testing the API

### Option A — curl (command line, no install needed)

`curl` comes pre-installed on macOS, Linux, and Windows 10+. Open a terminal and paste any of the commands below.

**Add a course:**
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask for Beginners",
    "description": "Learn Flask routing, templates, and REST API basics",
    "target_date": "2026-09-01",
    "status": "Not Started"
  }'
```

**Get all courses:**
```bash
curl http://127.0.0.1:5000/api/courses
```

**Filter by status:**
```bash
curl "http://127.0.0.1:5000/api/courses?status=In%20Progress"
```

**Get one course:**
```bash
curl http://127.0.0.1:5000/api/courses/1
```

**Update a course:**
```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'
```

**Delete a course:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

---

### Option B — Postman (visual interface, recommended for beginners)

Postman gives you a graphical interface so you do not have to memorize `curl` syntax.

1. Download Postman from [postman.com](https://www.postman.com/downloads/) and install it
2. Click **New Request**
3. Choose the HTTP method from the dropdown (GET, POST, PUT, DELETE)
4. Enter the URL: `http://127.0.0.1:5000/api/courses`
5. For POST and PUT requests, click the **Body** tab, select **raw**, and choose **JSON** from the dropdown, then paste your JSON payload
6. Click **Send**

---

### Option C — Thunder Client (inside VS Code)

If you use VS Code, Thunder Client is a lightweight alternative to Postman that lives right inside your editor.

1. Open the Extensions panel in VS Code (`Ctrl+Shift+X`)
2. Search for **Thunder Client** and install it
3. Click the thunder bolt icon in the left sidebar
4. Use it the same way as Postman

---

### Understanding what to look for

When you send a request, check two things:

1. **The HTTP status code** — shown in Postman/Thunder Client, or use `curl -i` to see it in the terminal. A `2xx` code means success. A `4xx` code means your request had a problem. A `5xx` code means the server had a problem.

2. **The response body** — the JSON the API sends back. If something went wrong, the `error` or `errors` field tells you exactly what.

---

## How the JSON File Works

When the API starts for the first time, it creates `data/courses.json` automatically:

```json
{
  "courses": [],
  "next_id": 1
}
```

After you add a course, open the file and you will see:

```json
{
  "courses": [
    {
      "id": 1,
      "name": "Flask for Beginners",
      "description": "Learn Flask routing, templates, and REST API basics",
      "target_date": "2026-09-01",
      "status": "Not Started",
      "created_at": "2026-06-12T10:00:00Z"
    }
  ],
  "next_id": 2
}
```

The `next_id` counter ensures IDs always go up, even if you delete courses. If you delete course 3 and then add a new course, it will get ID 4 — not 3. This avoids confusion when working with IDs.

> **Tip:** Watching `courses.json` change in VS Code as you test is one of the best ways to understand what the API is doing behind the scenes.

---

## Troubleshooting

### "Address already in use" error on startup

Another process (possibly a previous Flask instance you forgot to stop) is using port 5000.

**Fix on macOS/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

**Fix on Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Then run `python app.py` again.

---

### "ModuleNotFoundError: No module named 'flask'"

Flask is not installed in your current environment.

**Fix:** Make sure your virtual environment is active (you should see `(venv)` in your terminal), then run:
```bash
pip install -r requirements.txt
```

---

### curl returns "Failed to connect" or "Connection refused"

The Flask server is not running, or you have the wrong port.

**Fix:** Check that the server is still running in your other terminal. If it stopped, restart it with `python app.py`. Make sure the URL in your curl command is `http://127.0.0.1:5000` and not `https://`.

---

### POST request returns "Request body must be JSON"

You are sending data without telling the API what format it is in.

**Fix:** Make sure you include the header `-H "Content-Type: application/json"` in your curl command. Without it, Flask does not know how to read the body.

---

### `courses.json` has wrong or test data in it

You want to start fresh.

**Fix:** Delete `courses.json` and restart the server. The file will be recreated empty automatically.

```bash
rm data/courses.json   # macOS / Linux
del data\courses.json  # Windows
```

---

### Status filter returns empty results

You may have a spacing or casing issue in the query parameter.

**Fix:** Status values are case-sensitive and must match exactly:
- `Not Started` (capital N and S)
- `In Progress` (capital I and P)
- `Completed` (capital C)

In curl, spaces must be encoded as `%20`:
```bash
curl "http://127.0.0.1:5000/api/courses?status=Not%20Started"
```

In Postman and Thunder Client, you can type spaces directly.

---

### On Windows, PowerShell curl does not work like the examples

Windows PowerShell has its own `curl` command that behaves differently from the real one. Use `curl.exe` instead:

```bash
curl.exe -X POST http://127.0.0.1:5000/api/courses `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Flask for Beginners\",\"description\":\"REST basics\",\"target_date\":\"2026-09-01\",\"status\":\"Not Started\"}'
```

Or switch to using Postman or Thunder Client, which avoids command-line quoting issues entirely.

---

## Glossary for Beginners

| Term | What it means in plain English |
|---|---|
| **API** | A set of rules for how two programs talk to each other. Here, your terminal talks to Flask. |
| **REST** | A style of building APIs using standard HTTP methods. Not a library — a set of conventions. |
| **Endpoint** | A specific URL the API listens on, like `/api/courses`. Each one does a different thing. |
| **HTTP method** | The verb that tells the server what action you want: GET (read), POST (create), PUT (update), DELETE (remove). |
| **JSON** | A text format for storing and sending data. Looks like a Python dictionary. |
| **HTTP status code** | A number the server adds to every response. 200 = OK, 201 = created, 400 = bad request, 404 = not found. |
| **Request body** | The JSON data you send along with a POST or PUT request. |
| **Response body** | The JSON data the server sends back to you. |
| **Virtual environment** | An isolated Python installation just for this project, so its dependencies don't clash with other projects. |
| **`curl`** | A command-line tool for sending HTTP requests. Ships with most operating systems. |
| **`debug=True`** | A Flask setting that makes development easier. Auto-reloads the server when you edit code. Never use in production. |
| **CRUD** | Create, Read, Update, Delete — the four basic operations of any data-driven app. |
| **Query parameter** | Extra information added to a URL after a `?`, like `?status=Completed`. Used for filtering. |g