from api.api import app
from fastapi import FastAPI

from api.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)

__all__ = ["app"]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)