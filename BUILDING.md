## 📄 **Running the Application**

Please refer to the detailed instructions in the [Setup and Run Guide](docs/SETUP_AND_RUN.md) for full steps on building and running the application.

---

### **Content of `docs/SETUP_AND_RUN.md`**

# 🚀 **Setup and Run Guide**

## **Installing the Environment**

1. **Install `uv` Package Manager**
   The application uses the `uv` package manager for dependency management. Follow the steps below to install `uv`:

   - **Linux/MacOS:**
      Download the installer from [uv.sh](https://docs.astral.sh/uv/getting-started/installation/) and follow the installation instructions.

      or alternatively:

     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - **Windows:**
     Download the installer from [uv.sh](https://docs.astral.sh/uv/getting-started/installation/) and follow the installation instructions.

1. **Install Project Dependencies:**
   After installing `uv`, run the following command in the root directory of the project to install all dependencies:

    ```bash
    uv install
    ```

## **Setting Up the Environment**

1. **Create a `.env` File:**
   Use the template `.env.example` provided in the repository to create a `.env` file. Ensure you fill in the necessary environment variables such as:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - Other configuration values.

2. **Verify the Environment Variables:**
   Double-check that all required variables are set correctly before proceeding.

## **Running the Application**

1. **Start the FastAPI Server:**
   Use the following command to start the server:

   ```bash
   fastapi run src/shared/presentation/web/fastapi/main.py --reload
    ```

2. Access the API Documentation:
   Once the server is running, you can access the Swagger UI for API documentation and testing at:
    <http://127.0.0.1:8000/docs>

3. Optional - Check the Redoc API Docs:
    You can also access the alternative documentation at:
    <http://127.0.0.1:8000/redoc>
