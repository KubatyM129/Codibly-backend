from fastapi import FastAPI
from .api.routes import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(router, prefix="/api")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)