from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/health-check")
def health_check():
    return {"status": "ok"}
