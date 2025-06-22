# Backend/main.py (updates)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from Backend.utils.database import connect_to_mongo, client
from Backend.routes.user_routes import router as user_router
from Backend.routes.product_routes import router as product_router
from Backend.routes.review_routes import router as review_router
from Backend.routes.admin_routes import router as admin_router
from Backend.routes.auth_routes import router as auth_router
from Backend.utils.scheduler import start_scheduler, shutdown_scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

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
app.include_router(auth_router)

# Mount static files (assets)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../Frontend/assets")), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../Frontend/templates"))

@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def serve_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def serve_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/products/", response_class=HTMLResponse)
def serve_products_page(request: Request):
    return templates.TemplateResponse("productDetails.html", {"request": request})

@app.get("/seller/dashboard", response_class=HTMLResponse)
def serve_seller_dashboard(request: Request):
    return templates.TemplateResponse("seller_dashboard.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def serve_admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/product/{product_id}", response_class=HTMLResponse)
def serve_product_detail(request: Request, product_id: str):
    return templates.TemplateResponse("product_detail.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Backend.main:app", reload=True)

