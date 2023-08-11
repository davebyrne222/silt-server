# Silt Server

The back-end server for the 'Songs I'm Listening To' web app.

# Configuration

SiltServer requires a number of settings to assist in configuring the PostgresDB and Uvicorn server. These
settings should be configured in a file entitled `.env` located in the SiltServer root directory. The following snippet
displays the required variables. Please note, only those with `<>` brackets in the setting require any changes.

```.dotenv
PYTHONPATH=/app/SiltServer:${PYTHONPATH}
POSTGRES_USER="<username>"
POSTGRES_PASSWORD="<password>"
POSTGRES_DB="<database name>"
DATABASE_URL='postgresql://<username>:<password>@<postgresDB addr>/<database name>'
SERVER_ADDR_HOST="0.0.0.0"
SERVER_ADDR_PORT="8081"
SERVER_RELOAD="False"
```

- `PYTHONPATH`: This enables the absolute imports used within SiltServer. No changes required unless the `WORKING_DIR`
  in the Dockerfile is
  changed
- `POSTGRES_USER` \*: The username for PostgresDB
- `POSTGRES_PASSWORD` \*: The password for PostgresDB
- `POSTGRES_DB` \*: The name of the PostgresDB database
- `DATABASE_URL` \*\*: The PostgresDB database url. This facilitates the connection from FastAPI to Postgres and takes
  the form: `postgresql://<username>:<password>@<postgresDB addr>/<database name>`
- `SERVER_ADDR_HOST`: The desired host IP of the SiltServer. This can typically be set to `0.0.0.0`
- `SERVER_ADDR_PORT`: The desired port of the SiltServer. This can typically be set to `8081`
- `SERVER_RELOAD`: When `True`, the uvicorn server will reload on detected code changes. This should be used for
  development purposes only and otherwise can be set to `False`

> [!NOTE]
> *If running locally, this should be the same value used when
> creating the PostgresDB instance. If running with Docker, this can be the value you wish to use (PostgresDB will be
> created with that value)


> [!NOTE]
> **If running locally, the \<PostgresDB addr\> can be set to `localhost`. If using Docker, it should be set to the
> docker compose service name. Default for SiltServer is 'DB'

# Usage

## Run Locally

1. Install `pipenv`:
   ```shell
   pip install pipenv
   ```

2. Install dependencies:
   ```shell
   pipenv install 
   ```
   This will create a virtual environment and install all dependencies within it

3. Add the top level / root path to the `PYTHONPATH` to enable absolute imports:
    ```shell
    export PYTHONPATH='.'
    ```
   **N.B.**: The working directory should be the SiltServer root dir before running this command

4. Run the uvicorn server:
   ```shell
   pipenv run python SiltServer/main.py
   ```
   This will run the server on at the host IP and port specified in the `.env` file (see ??). The docs
   can be access by navigating to  `http://<ip>:<port>/docs`

## Run Using Docker-Compose

Assuming Docker-Compose is available on your local system, SiltServer can be run using:

```shell
docker-compose up
```

This will run the server on at the host IP and port specified in the `.env` file (see [Configuration](#Configuration)). The docs
can be access by navigating to the `http://<ip>:<port>/docs`

# To Do

- [X] Create project structure
- [X] Create get endpoint
- [X] Restructure project to FastAPI structure
- [X] Create post endpoint
    - [X] add endpoint
    - [X] add security
    - [X] prevent / make obvious id field is not required (pk, auto-incremented)
- [X] Extract server and host and port to config / .env
- [X] Add password hashing
- [ ] Add pagination to get
- [X] Add docker
- [ ] Add fields to song for note, genre, artwork image
- [ ] Add unit tests
- [ ] Add endpoint tests?
- [X] Change auth to JWT
- [ ] Add migration support (alembic?)
- [ ] Add HTTPS support?