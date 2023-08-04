# Silt Server

The back-end server for the 'Songs I'm Listening To' web app.

# Run locally

1. Add the top level path to the `PYTHONPATH` to enable absolute imports:
    ```shell
    export PYTHONPATH='.'
    ```

# To Do

- [X] Create project structure
- [X] Create get endpoint
- [X] Restructure project to FastAPI structure
- [ ] Refactor postgress url in .env
- [X] Create post endpoint
    - [X] add endpoint
    - [X] add security
    - [X] prevent / make obvious id field is not required (pk, auto-incremented)
- [X] Extract server and host and port to config / .env
- [ ] Add password hashing
- [ ] Add pagination to get
- [ ] Add docker
- [ ] Add fields to song for note, genre, artwork image
- [ ] Add unit tests
- [ ] Add endpoint tests?
- [ ] Change auth to JWT
- [ ] Add migration support (alembic?)