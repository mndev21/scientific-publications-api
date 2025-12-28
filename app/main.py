from fastapi import FastAPI

app = FastAPI(title="Scientific Publications API")

@app.get("/")
def root():
    return {"status": "ok"}
