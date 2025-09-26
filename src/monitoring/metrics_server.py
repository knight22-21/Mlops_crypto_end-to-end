from prometheus_client import make_asgi_app
from fastapi import FastAPI
import uvicorn

app = FastAPI()
# mount metrics at /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
