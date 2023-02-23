import uvicorn
from fastapi import Request, FastAPI
from google.cloud import aiplatform_v1
from google.cloud import aiplatform
import os
import datetime


aiplatform.init(
    project=os.environ.get("PROJECT"),
    location=os.environ.get("REGION")
)

endpoint = aiplatform.Endpoint(os.environ.get("ENDPOINT"))

index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=os.environ.get("INDEX_RESOURCE_NAME"))

index_client = aiplatform_v1.IndexServiceClient(
    client_options=dict(api_endpoint="{}-aiplatform.googleapis.com".format(os.environ.get("PROJECT")))
)

app = FastAPI()

@app.post('/query')
async def query (request: Request):
    body = await request.json()
    description = body['description']

    start_time = datetime.datetime.now()
    embeddings = endpoint.predict(instances=[{"text": ticket_description}])
    end_time = datetime.datetime.now()

    time_diff = (end_time - start_time)
    latency_embedding = time_diff.total_seconds() * 1000
    print(f'latency embedding {latency_embedding}')

    start_time = datetime.datetime.now()
    matches = index_endpoint.match(
      deployed_index_id=os.environ.get("DEPLOYED_INDEX_ID"),
      queries=[embeddings.predictions[0]],
      num_neighbors=10
    )
    end_time = datetime.datetime.now()

    time_diff = (end_time - start_time)
    latency_matching = time_diff.total_seconds() * 1000
    print(f'latency matching {latency_matching}')

    formated_response = []
    for match in matches[0]:
      formated_response.append({"id": match.id, "similarity": match.distance})

    return formated_response

@app.post('/insert')
async def insert(request: Request):
    body = await request.json()

    ticket_description = body['description']
    ticket_id = body['id']

    embeddings = endpoint.predict(instances=[{"text": ticket_description}])

    insert_datapoints_payload = aiplatform_v1.IndexDatapoint(
      datapoint_id=ticket_id,
      feature_vector=embeddings[0][0]
    )

    upsert_request = aiplatform_v1.UpsertDatapointsRequest(
      index=os.environ.get("INDEX_RESOURCE_NAME"), datapoints=[insert_datapoints_payload]
    )

    index_client.upsert_datapoints(request=upsert_request)

    return "done"


if __name__ == "__main__":
    uvicorn.run(app, debug=True)