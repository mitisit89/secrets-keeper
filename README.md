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
## Running without docker
    1. go to https://github.com/astral-sh/uv and install 
    2. git clone https://github.com/yourusername/secrets_keeper.git
    3. cd secrets_keeper
    4. Setup venv ```sh uv venv```
    5. Sync deps ```sh uv sync```
    6. Activate ```sh venv source .venv/bin/activate```
    7. gen secret key ```sh python  gen_secret_key.py```
    8. fastapi dev
## CI/CD

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml`.

## Environment Variables

The following environment variables are used by the application:

- `DATABASE_URL`: The URL of the PostgreSQL database.
- `SECRET_KEY`: The secret key used for encryption.

