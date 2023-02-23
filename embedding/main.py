import os
from fastapi import Request, FastAPI 

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('../all-mpnet-base-v2')

app = FastAPI()

AIP_HEALTH_ROUTE = os.environ.get('AIP_HEALTH_ROUTE', '/health')
AIP_PREDICT_ROUTE = os.environ.get('AIP_PREDICT_ROUTE', '/predict')

@app.get(AIP_HEALTH_ROUTE, status_code=200)
async def health():
    return {'health': 'ok'}

@app.post(AIP_PREDICT_ROUTE)
async def predict(request: Request):
    body = await request.json()

    instances = body["instances"]
    instances = [x['text'] for x in instances]
    embeddings = model.encode(instances).tolist()

    data = {"predictions": embeddings}

    return data