# Backend/main.py (updates)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from Backend.utils.database import connect_to_mongo, client
from Backend.routes.user_routes import router as user_router
from Backend.routes.product_routes import router as product_router
from Backend.routes.review_routes import router as review_router
from Backend.routes.admin_routes import router as admin_router
from Backend.utils.scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    # start scheduler after DB is connected
    start_scheduler()
    try:
        yield
    finally:
        shutdown_scheduler()
        client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Backend.main:app", reload=True)

