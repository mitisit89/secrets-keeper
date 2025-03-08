# Secrets Keeper

Secrets Keeper is a secure application for storing and managing passwords. It uses encryption to protect your passwords and provides an API for accessing and managing them.

## Features

- Encrypt and decrypt passwords
- Store and retrieve passwords securely
- Search for passwords by service name
- Create or update passwords

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository:

```sh
git clone https://github.com/yourusername/secrets_keeper.git
cd secrets_keeper
```

2. Build and start the services using Docker Compose:

```sh
docker-compose up --build
```

3. The application will be available at `http://localhost:8000`.

4. Access the API documentation at `http://localhost:8000/docs`.

## Running Tests

To run the tests, use the following command:

```sh
pytest
```
# Secrets Keeper

## Installation and Setup

1. Install [uv](https://github.com/astral-sh/uv):
   ```sh
   pip install uv
   ```

2. Clone the repository:
   ```sh
   git clone https://github.com/mitisit89/secrets_keeper.git
   ```

3. Navigate to the project directory:
   ```sh
   cd secrets_keeper
   ```

4. Create and set up a virtual environment:
   ```sh
   uv venv
   ```

5. Install dependencies:
   ```sh
   uv sync
   ```

6. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```

7. Generate a secret key:
   ```sh
   python gen_secret_key.py
   ```

8. Start FastAPI in development mode:
   ```sh
   fastapi dev
   ```

## Additional Information
- Make sure you have Python 3.8+ installed.
- If you are using Windows, activate the virtual environment with:
  ```sh
  .venv\Scri
## CI/CD

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml`.

## Environment Variables

The following environment variables are used by the application:

- `DATABASE_URL`: The URL of the PostgreSQL database.

