from fastapi import FastAPI
from app.api.router import router
from app.settings import settings
from app.db.connection import engine
from app.db.models import ServicePassword

app = FastAPI(title=settings.APP_NAME)
app.include_router(router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(ServicePassword.metadata.create_all)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
