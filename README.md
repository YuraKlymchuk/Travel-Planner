# Travel Planner API

This is a Python-based backend application developed using the FastAPI framework for managing travel projects, tracking locations, and integrating with third-party APIs.

## API Documentation

The application is fully documented adhering to the OpenAPI standards. You can view, interact with, and test the API endpoints using the following methods:

### 1. Interactive Swagger UI (Local Server)
When the application is running locally, the built-in interactive documentation interfaces are accessible at the following URLs:
* **Swagger UI:** http://127.0.0.1:8000/docs (Recommended for real-time endpoint testing)
* **ReDoc:** http://127.0.0.1:8000/redoc

### 2. Static API Documentation File
A pre-generated static API documentation file is included directly in the root directory of this application (`openapi.json`). 
This file contains the complete OpenAPI specification of the endpoints and can be imported into external tools such as Postman, 
Insomnia, or any standard Swagger UI viewer to examine the API structure without running the local server.

---

## Local Setup and Installation

Follow these instructions to deploy and run the application within your local environment.

### Prerequisites
* Python 3.13 or higher
* Docker and Docker Compose (Optional, for containerized deployment)

### Standard Deployment (Using Virtual Environment)
1. Initialize the virtual environment:
   ```bash
   python -m venv .venv
2. Activate the virtual environment:

 - On Windows (PowerShell): .venv\Scripts\activate.ps1
 - On Windows (CMD): .venv\Scripts\activate.bat
 - On macOS / Linux: source .venv/bin/activate

3. Install the required project dependencies:
    ```bash
   pip install -r requirements.txt

4. Start the local development server:
    ```bash
    uvicorn app.main:app --reload

### Containerized Deployment (Using Docker Compose)
1. To initialize and launch the API instance alongside the PostgreSQL database network automatically, 
execute the following orchestration command:
    ```bash
    docker-compose up --build
    