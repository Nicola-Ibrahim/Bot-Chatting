from src.api.startup import APIStartup

from .modules.utils import initialize_modules


def create_and_run_api():
    """Creates and runs the Flask application."""
    APIStartup().start()


def main():
    """Main entry point: Initializes DI and runs the app."""
    initialize_modules()
    create_and_run_api()


if __name__ == "__main__":
    main()
