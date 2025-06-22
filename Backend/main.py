from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from Backend.utils.database import connect_to_mongo,client
from Backend.routes import user_routes, product_routes
from Backend.routes import review_routes
from Backend.routes import admin_routes
@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    try:
        yield
    finally:
        client.close()

        
app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(user_routes.router)

# Product endpoints: /products/add, /products/my?seller_id=...
app.include_router(product_routes.router)

app.include_router(review_routes.router)
app.include_router(admin_routes.router)

if __name__ == "__main__":
    import uvicorn; uvicorn.run("Backend.main:app", reload=True)




