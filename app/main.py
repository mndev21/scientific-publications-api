from fastapi import FastAPI
from app.api.queries import router as queries_router
from app.api.search import router as search_router

app = FastAPI(title="Scientific Publications API")

# Подключаем роутеры
app.include_router(queries_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {"status": "ok"}
