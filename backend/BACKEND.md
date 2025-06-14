# Backend Setup

## Environment Variables

Create a `.env` file in the root of the backend directory (`backend/.env`).

Add the following environment variables:

```
SECRET_KEY='a-dummy-secret-key-for-development'
```

## Database Setup

Run the migrations to set up the database schema:

```bash
python manage.py migrate
```

## Superuser Creation

To access the Django admin, you need to create a superuser. Run the following command:

```bash
python manage.py createsuperuser
```

You will be prompted to enter a username, email, and password. You can use the following for local development:

-   **Username:** admin
-   **Email:** admin@example.com
-   **Password:** (choose a secure password)

**Note:** The superuser credentials are not stored in the `.env` file. They are stored securely in the project's database. The `.env` file is used for configuration variables like the `SECRET_KEY`.
