from fastapi import FastAPI
from inference import predict_price, batch_predict
from schemas import HousePredictionRequest, PredictionResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize FastAPI app with metadata
app = FastAPI(
    title="House Price Prediction API",
    description="An API for predicting house prices based on various features.",
    version="1.0.0",
    contact={
        "name": "Jay Narayan",
        "email": "jaynarayan94@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Create and apply Prometheus instrumentation exactly once
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize and instrument Prometheus metrics
instrumentator = Instrumentator()
instrumentator.instrument(app)
instrumentator.expose(app)

# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy", "model_loaded": True}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: HousePredictionRequest):
    return predict_price(request)

# Batch prediction endpoint
@app.post("/batch-predict", response_model=list)
async def batch_predict_endpoint(requests: list[HousePredictionRequest]):
    return batch_predict(requests)
