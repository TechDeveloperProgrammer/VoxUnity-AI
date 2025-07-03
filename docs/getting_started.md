# Getting Started with VoxUnity AI+

This section will guide you through the initial setup and basic usage of VoxUnity AI+.

## Installation

Follow the detailed instructions in the [README.md](../README.md) file to install the project. This includes setting up your Python environment, installing system dependencies, and configuring the `.env` file.

### Key Dependencies and External Services

VoxUnity AI+ leverages several powerful tools and services. While some are integrated directly, others might require manual installation or configuration for full functionality:

*   **OBS Studio:** A free and open-source software for video recording and live streaming. Essential for `mod-voice` and `mod-streaming` for real-time audio/video manipulation and overlays. [Download OBS Studio](https://obsproject.com/)
*   **AudioRelay:** An application that turns your phone into a wireless microphone or speaker. Useful for `mod-voice` (sending processed audio to phone) and `mod-mobile` (using phone as microphone input). [Download AudioRelay](https://audiorelay.net/)
*   **Tesseract OCR:** An open-source optical character recognition engine. Crucial for `mod-activism`'s anti-doxing features to extract text from images. [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)
*   **PyPI:** The Python Package Index, where all Python dependencies are sourced. We ensure our `requirements.txt` and `setup.py` reference the latest stable versions with safe version ranges.
*   **DockerHub:** A cloud-based repository service for Docker images. Our project is set up for Docker builds, and a future goal is to publish official images here.

## Running the Application

Once installed and your virtual environment is activated (or using Docker), you can run the different components of VoxUnity AI+:

### CLI (Command Line Interface)

The CLI provides a powerful way to interact with VoxUnity AI+ modules directly from your terminal. It's built with `Click` for a robust and extensible experience.

```bash
voxunity cli --help
# Example: Start voice modulation with a robot preset
voxunity cli voice start --preset robot
# Example: Anonymize a file
voxunity cli activism anonymize --file /path/to/sensitive_document.pdf
```

### GUI (Graphical User Interface)

The GUI offers an accessible and intuitive way to manage VoxUnity AI+ features. It's built with `PyQt5` and includes a role-based access system.

```bash
voxunity gui
```

Upon launching, you'll be presented with a login screen. You can register a new user (for demo purposes) or log in with existing credentials. Your role will determine which modules are visible and accessible.

### API (REST/WebSocket)

VoxUnity AI+ exposes a local RESTful API with WebSocket capabilities, built with `Flask` and documented using `Flasgger` (OpenAPI/Swagger UI).

```bash
voxunity api
```

Once the API server is running, you can access its interactive documentation (Swagger UI) in your web browser at `http://127.0.0.1:5000/apidocs/` (or the port configured in your `.env` file).

#### API Authentication

Most API endpoints require JWT (JSON Web Token) authentication. Follow these steps to interact with the authenticated endpoints:

1.  **Login:** Send a POST request to the `/login` endpoint with your `username` and `password` to obtain an `access_token`.
    *   **Example Request (using `curl`):**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://127.0.0.1:5000/login
        ```
    *   **Example Response:**
        ```json
        {
          "access_token": "eyJ...",
          "token_type": "bearer"
        }
        ```

2.  **Include Token in Requests:** For subsequent authenticated requests, include the `access_token` in the `Authorization` header as a `Bearer` token.
    *   **Example Request (using `curl` for `/status` endpoint):**
        ```bash
        curl -X GET -H "Authorization: Bearer eyJ..." http://127.0.0.1:5000/status
        ```

## Next Steps

Explore the individual module documentation for more specific usage examples and configuration details.