def log_execution(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Executing {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Executed {func.__name__}")
            return result

        return wrapper

    return decorator
