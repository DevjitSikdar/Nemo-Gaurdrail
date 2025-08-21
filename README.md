# Project Name
NeMo Guardrails + FastAPI + ChatGroq


## Description

This project is a Python application that utilizes FastAPI for its API and Nemo Guardrails for conversational AI functionalities. It includes a chat interface and various guardrails to ensure safe and relevant interactions.

## Setup

To set up the development environment, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Intern
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: If `requirements.txt` does not exist, you may need to generate it first using `pip freeze > requirements.txt` after installing necessary packages, or install packages individually.)*

## Running the Application

To run the FastAPI application, use Uvicorn:

```bash
./venv/Scripts/python.exe -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The application will be accessible at `http://localhost:8000`.

## Testing

To run the tests, use pytest:

```bash
pytest
```

## API Endpoints

The application exposes the following API endpoints:

*   `/chat`: Main endpoint for conversational interactions.
*   *(Add more specific API endpoints here as they are developed)*

## Guardrail Functionalities

This project incorporates Nemo Guardrails to enforce various policies and behaviors, including:

*   **Topic Filtering:** Prevents discussions on predefined sensitive or out-of-scope topics.
*   **Toxicity Filtering:** Detects and mitigates toxic or harmful language.
*   **Citation Enforcement:** Ensures that responses are grounded in provided knowledge bases and cite sources appropriately.
*   **Length Control:** Manages the length of generated responses.
*   *(Add more specific guardrail functionalities here as they are implemented)*