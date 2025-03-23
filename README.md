# ProkrastiNie: A Simple Task Management Application

ProkrastiNie is a Flask-based web application designed to help users manage their tasks.  It features a simple web interface for creating, viewing, editing, completing, and deleting tasks. It also includes a read-only API for retrieving a user's task list. The project emphasizes simplicity and uses forever API tokens for API access.

**Important Security Note:** This project uses *forever API tokens*, which do *not* expire.  This is suitable for *personal use and testing only*.  For any production environment, you *must* implement expiring tokens and a refresh token mechanism for security.  If a forever token is compromised, an attacker has indefinite access.

## Features

*   **User Authentication:**
    *   User registration and login via a web interface.
    *   Password hashing for security.
    *   "Remember Me" functionality.
*   **Task Management (Web Interface):**
    *   Create new tasks with a title, description, due date, and optional due time.
    *   View a list of all tasks, sorted by due date.
    *   Edit existing tasks (title, description, due date, due time, completion status).
    *   Mark tasks as complete or pending.
    *   Delete tasks.
*   **API (Read-Only):**
    *   Retrieve a list of all tasks for the authenticated user in JSON format.
    *   Uses "forever" API tokens for authentication (see security note above).
    *   Pagination for handling large task lists.
*   **Internationalization (i18n):**
    *   Support for English and Spanish.
    *   Uses Flask-Babel for translations.
* **Styling:**
    * Uses Bootstrap v5 for fast and user friendly UI.
* **Tech Stack:**
      * Python v3.12


## Setup and Installation

1.  **Prerequisites:**

    *   Python 3.8 or higher (3.12 recommended).
    *   pip (Python package installer).

2.  **Clone the Repository:**

    ```bash
    git clone <repository_url>  # Replace with your repository URL
    cd <repository_directory>    # Replace with your project directory
    ```

3.  **Create a Virtual Environment (Highly Recommended):**

    A virtual environment isolates your project's dependencies.

    ```bash
    python3 -m venv venv  # Or python -m venv venv
    ```

4.  **Activate the Virtual Environment:**

    *   **Linux/macOS:**

        ```bash
        source venv/bin/activate
        ```

    *   **Windows (cmd.exe):**

        ```bash
        venv\Scripts\activate
        ```
     * **Windows (Powershell):**

        ```bash
        venv\Scripts\Activate.ps1
        ```

5.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

6.  **Database Setup:**

    *   **Initialize the database:**

        ```bash
        flask db init
        ```

    *   **Create the initial migration:**

        ```bash
         python -m flask db migrate -m "Initial migration"
        ```
         Or with Venv:
        ```bash
         flask db migrate -m "Initial migration"
        ```

    *   **Apply the migration:**

        ```bash
        python -m flask db upgrade
        ```
         Or with Venv:
         ```bash
          flask db upgrade
         ```

7.  **Configure Environment Variables:**

    *   Create a `.flaskenv` file in the root directory of your project. Add the following lines:
         *   `FLASK_APP=prokrastinie.py`  (Tells Flask where your app is)
         * `FLASK_DEBUG=1`
            (Enables debug mode - *remove* this in production!)
         * `SECRET_KEY=your-secret-key` (**Important:** Change `your-secret-key` to a *strong, random* value.  This key is used for security-sensitive operations, such as session management.)  Generate a strong key.
            Example with `secrets` inside `python`:
             ```python
                import secrets
                secrets.token_urlsafe(32)
                'copy this generated value'
              ```
        Example:
        ```
         FLASK_APP=prokrastinie.py
         FLASK_DEBUG=1
         SECRET_KEY=some_very_long_random_string_you_generate
        ```

    *   (Optional, but recommended) Create a `.env` file in your project's root directory.  Add:

        ```
        DATABASE_URL=sqlite:///app.db
        ```

        This sets the database URL to use a local SQLite database (`app.db`).  For other databases (PostgreSQL, MySQL, etc.), you'll need to adjust the `DATABASE_URL` accordingly (and install the appropriate database drivers).

8. **Run The application**
  To run the Application, you need to start the flask server:

flask run

Usage (Web Interface)
Open in Browser: Access the application in your web browser at http://127.0.0.1:5000 (or the address shown in your terminal).

Register: Click the "Register" link to create a new user account.

Log In: Use your registered username and password to log in.

Manage Tasks:

Create new tasks using the form on the main page (/index).

View, edit, complete, and delete tasks from the task list.

Get Your API Token:
After registering and logging in, navigate to /auth/get_token.
Copy your API token.
Keep it secret!

API Usage (Read-Only)
The API allows you to retrieve a list of all tasks for the authenticated user in JSON format.

Endpoint: /api/tasks (GET)

Authentication: You must include your API token in the Authorization header, using the Bearer scheme:

Authorization: Bearer <your_api_token>
Use code with caution.
Examples:

curl (Linux, macOS, Windows with Git Bash/WSL):

curl -H "Authorization: Bearer <your_api_token>" http://127.0.0.1:5000/api/tasks
Use code with caution.
Bash
PowerShell (Windows):

$token = "<your_api_token>"
$baseUrl = "http://127.0.0.1:5000"
$response = Invoke-WebRequest -Uri "$baseUrl/api/tasks" -Headers @{Authorization = "Bearer $token"}
$response.Content | ConvertFrom-Json
Use code with caution.
Powershell
Or (one-liner):

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/tasks" -Headers @{Authorization = "Bearer <your_api_token>"} | ConvertFrom-Json
Use code with caution.
Powershell
Example API Response:

{
  "_links": {
    "next": null,
    "prev": null,
    "self": "/api/tasks?page=1&per_page=25"
  },
  "_meta": {
    "page": 1,
    "per_page": 25,
    "total_items": 2,
    "total_pages": 1
  },
  "items": [
    {
      "completed": false,
      "description": "Task description",
      "due_date": "2025-03-28T00:00:00Z",
      "id": 1,
      "title": "Task Title"
    },
    {
      "completed": true,
      "description": "Another task",
      "due_date": "2025-04-01T12:30:00Z",
      "id": 2,
      "title": "Another Task"
    }

  ]
}


API Response Fields:

_links: Provides links for pagination (if there are multiple pages of tasks). next and prev will be null if there are no more pages. self points to the current page.

_meta: Metadata about the current page and the total task list:

page: The current page number.

per_page: The number of tasks per page.

total_items: The total number of tasks for the user.

total_pages: The total number of pages.

items: An array of task objects. Each task object has the following fields:

id: The unique ID of the task.

title: The title of the task.

description: The description of the task (can be null).

due_date: The due date and time of the task in ISO 8601 format (with a "Z" indicating UTC). Can be null if no due date is set.

completed: A boolean value indicating whether the task is completed (true) or not (false).

Important Notes:
Security: Again, this project uses forever API tokens for simplicity. This is not secure for production use.

Error Handling: The API includes basic error handling (returning JSON responses with appropriate HTTP status codes). More robust error handling could be added.

Pagination: The API supports pagination. You can control the page number and the number of items per page using the page and per_page query parameters (e.g., /api/tasks?page=2&per_page=10). The _links and _meta fields in the response provide information for navigating between pages.
