# CRM Application Setup

This document outlines the steps to set up and run the Celery task for generating weekly CRM reports.

## Prerequisites

- Python 3.8+
- Redis server
- Django project dependencies

## Setup Instructions

1.  **Install Redis**

    Install Redis on your system:

    - **Ubuntu/Debian:**
      ```bash
      sudo apt-get install redis-server
      ```
    - **macOS:**
      ```bash
      brew install redis
      ```
    - **Windows:** Download and install Redis from [https://redis.io/download](https://redis.io/download)

    Start the Redis server (it runs on port 6379 by default):

    ```bash
    redis-server
    ```

2.  **Install Dependencies**

    Run the following command to install all required Python packages, including `celery` and `django-celery-beat`:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations**

    Apply database migrations:

    ```bash
    python manage.py migrate
    ```

4.  **Start Celery Worker**

    In a new terminal, start the Celery worker to process tasks:

    ```bash
    celery -A crm worker -l info
    ```

5.  **Start Celery Beat**

    In another terminal, start the Celery Beat scheduler for the weekly report task:

    ```bash
    celery -A crm beat -l info
    ```

6.  **Verify Logs**

    Check `/tmp/crm_report_log.txt` for weekly CRM reports, which are logged every Monday at 6:00 AM.

    The log format is:

    ```
    YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
    ```

## Notes

- Ensure the Redis server is running before starting the Celery services.
- The GraphQL endpoint (`http://localhost:8000/graphql`) must be available for the task to query data.
- The Celery task assumes the GraphQL schema includes `totalCustomers`, `totalOrders`, and `totalRevenue` fields.
