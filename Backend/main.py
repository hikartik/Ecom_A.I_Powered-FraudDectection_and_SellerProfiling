from fastapi import FastAPI
from Backend.routes import predict, list_product

app = FastAPI()

# Internal route for Trust & Safety team to get raw predictions
app.include_router(predict.router, prefix="/predict", tags=["Internal Prediction"])

# Seller-facing route: auto-screens new listings in real-time
app.include_router(
    list_product.router,
    prefix="/list_product",
    tags=["Seller Listing"]
)

if __name__ == "__main__":
    import uvicorn
    # Launch the app: reload enables live code updates during development
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)