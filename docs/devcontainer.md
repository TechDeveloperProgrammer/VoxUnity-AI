# Dev Container

VoxUnity AI+ includes a Dev Container configuration for easy development setup using Visual Studio Code and GitHub Codespaces.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/voxunity-ai.git
    cd voxunity-ai
    ```

2.  **Open in VS Code Dev Containers:**
    - Open VS Code.
    - Click on the green remote indicator in the bottom-left corner of the VS Code window.
    - Select "Reopen in Container" (if you already opened the folder) or "Open Folder in Container..." and select the `voxunity-ai` directory.

    VS Code will build the Docker image and open the project inside the container. All dependencies will be automatically installed.

## GitHub Codespaces

If you are using GitHub Codespaces, the environment will be automatically set up for you when you create a new codespace from this repository.

