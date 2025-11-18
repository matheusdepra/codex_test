from fastapi import FastAPI

app = FastAPI(title="FastAPI Sample")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from FastAPI template"}
