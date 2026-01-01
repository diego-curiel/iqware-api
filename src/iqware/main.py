from fastapi import FastAPI


app = FastAPI(title="IQWare", version="2025.1.0", root_path="/")

api = FastAPI(title="IQWare API", version="1", root_path="/api/v1")

app.mount("/api/v1", api)
