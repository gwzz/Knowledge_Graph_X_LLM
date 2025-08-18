# Knowledge Server

The **Knowledge Server** is a central component of the Knowledge_Graph_X_LLM project. It provides RESTful APIs and backend services for managing, querying, and serving knowledge graph (KG) data to clients and applications. The server is built with Python and is designed for extensibility and integration with other modules in the project.

## Features

- **Knowledge Graph Management**: Create, update, delete, and query entities and relationships in the KG.
- **Chat APIs**: Interact with the KG using natural language queries.
- **Modular Design**: Organized into app modules for chat and knowledge operations.
- **Logging**: Built-in logging for monitoring and debugging.
- **Environment Configuration**: Easily configurable via `.env` files.

## Directory Structure

```
knowledge_server/
├── .env                  # Environment variables (user-specific, not committed)
├── .env.template         # Template for environment configuration
├── configs.py            # Server and application configuration
├── databases.py          # Database connection and ORM setup
├── main.py               # Entry point for starting the server
├── utils.py              # Utility functions
├── app/
│   ├── __init__.py
│   ├── chat/
│   │   ├── __init__.py
│   │   └── chat.py
│   └── knowledge/
│       ├── __init__.py
│       ├── knowledge.py
│       ├── knowledge_crud.py
│       ├── knowledge_models.py
│       └── knowledge_schemas.py
├── log/
│   ├── log.log           # Log files
│   └── log.log.*         # Rotated logs
├── utilities/            # Additional utility scripts
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Navigate to the `knowledge_server` directory:
    ```sh
    cd knowledge_server
    ```

2. Install required Python packages:
    ```sh
    pip install -r ../requirements.txt
    ```

3. Copy the environment template and configure as needed:
    ```sh
    cp .env.template .env
    # Edit .env to set your environment variables (e.g., database URL, secret keys)
    ```

### Running the Server

Start the server with:

```sh
uvicorn main.app --reload
```

The server will start and expose RESTful endpoints for knowledge graph operations and chat.

## API Overview

- **Knowledge APIs**: CRUD operations for entities and relationships.
- **Chat APIs**: Natural language interface to the KG.

For detailed API documentation, see the code in `app/knowledge/` and `app/chat/`.

## Logging

Logs are stored in the `log/` directory. Check `log.log` for runtime information and errors.

## Customization

- Add new endpoints or logic in the `app/` submodules.
- Update configuration in `configs.py` or via the `.env` file.

## License

This module is part of the Knowledge_Graph_X_LLM project and is licensed under the MIT License.

---