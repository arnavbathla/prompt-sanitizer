# Prompt Sanitization API

The Prompt Sanitization API provides a simple and secure interface for cleaning prompts that will be sent to Large Language Models (LLMs). It's designed to mitigate various injection attacks by sanitizing inputs to remove potentially dangerous characters and patterns.

## Features

- **Injection Pattern Removal**: Removes specific injection patterns that can manipulate LLMs.
- **Character Sanitization**: Strips out characters that could potentially be used in SQL, command, and XSS injection attacks.
- **Extensible Keywords**: Easily add more keywords that, when detected, will trigger the removal of the following text.
- **Simple Integration**: Designed to be integrated easily with any system that interacts with LLMs.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python 3.8+ and Flask installed on your system to run the application.

### Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repo**

2. **Set Up a Virtual Environment**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install flask
    ```

4. **Start the Application**

    ```sh
    python app.py
    ```

The API will be available on `http://127.0.0.1:5000/`.

## Usage

To sanitize a prompt, send a POST request to `/sanitize` with a JSON payload containing the prompt.

```sh
curl -X POST http://127.0.0.1:5000/sanitize -H "Content-Type: application/json" -d "{\"prompt\":\"Your prompt here\"}"
```

## Customization

To add more keywords for sanitization, update the keywords_to_remove list in app.py.
```sh

keywords_to_remove = ['forget', 'ignore', 'skip', 'omit', ...]

```

## Testing
You can test the API using tools like cURL or Postman by sending POST requests to the /sanitize endpoint.
