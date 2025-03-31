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

2. **Install Project Dependencies:**
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

3. **Install Dependencies:**
   Ensure you have Python and `uv` installed. Then, installing the decencies will be automatically by `uv` when running the application

4. **Apply Database Migrations:**
   Run the following command to apply database migrations:

   ```bash
   alembic upgrade head
   ```

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

4. **Run Tests:**
   To ensure everything is set up correctly, run the tests using:

   ```bash
   pytest
   ```

5. **Run the Application with Docker (Optional):**
   If you prefer to use Docker, you can build and run the application using the provided `Dockerfile`:

   ```bash
   docker build -t bot-chat-system .
   docker run -p 8000:8000 --env-file .env bot-chat-system
   ```
