from fastapi import FastAPI

from app.api.publications import router
app.include_router(router)


app = FastAPI(title="Scientific Publications API")

@app.get("/")
def root():
    return {"status": "ok"}
