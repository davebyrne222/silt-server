# Silt Server

The back-end server for the 'Songs I'm Listening To' web app.

# Configuration

SiltServer requires a number of settings to assist in configuring the PostgresDB and Uvicorn server. These
settings should be configured in a file entitled `.env` located in the SiltServer root directory. The following snippet
displays the required variables. Please note, only those with `<>` brackets in the setting require any changes.

```.dotenv
PYTHONPATH=/app/SiltServer:${PYTHONPATH}
POSTGRES_USER="dave"
POSTGRES_PASSWORD="tidussloan"
POSTGRES_DB="silt-docker"
DATABASE_URL='postgresql://dave:tidussloan@db/silt-docker'
SERVER_ADDR_HOST="0.0.0.0"
SERVER_ADDR_PORT="8081"
SERVER_RELOAD="True"
```

- `PYTHONPATH`: This enables the absolute imports used within SiltServer. No changes required unless the dockerfile is
  changed
- `POSTGRES_USER` \*: The username for the PostgresDB
- `POSTGRES_PASSWORD`
- POSTGRES_DB="silt-docker"
- DATABASE_URL='postgresql://dave:tidussloan@db/silt-docker'
- SERVER_ADDR_HOST="0.0.0.0"
- SERVER_ADDR_PORT="8081"
- SERVER_RELOAD="True"

[!NOTE]
\*: If running locally, this should be set to the username set when
  creating the PostgresDB. If running with Docker, this can be any username you wish

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

This will run the server on at the host IP and port specified in the `.env` file (see ??). The docs
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