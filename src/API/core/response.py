from fastapi.responses import JSONResponse


class APIResponse:
    @staticmethod
    def success(data: dict = None, message: str = "Success"):
        return JSONResponse(content={"message": message, "data": data}, status_code=200)

    @staticmethod
    def error(message: str, status_code: int = 400):
        return JSONResponse(content={"message": message}, status_code=status_code)
