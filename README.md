# 


<div align="center">

Real Time Deep Learning Vector Similarity Search

[Architecture](#Architecture) •
[Setup](#Setup) •

</div>

## Architecture

![Architecture](docs/images/architecture.png?raw=true "Architecture")

## Setup

please follow the order 

### 1. Initial one-time setup Vertex AI

#### Create a Vertex AI Endpoint

```
gcloud ai endpoints create \
  --project=sascha-playground-doit \
  --region=us-central1 \
  --display-name=similarity-embedding-fast-api-cuda
```

#### Create the model serving container
Run the deploy.sh inside of the embedding folder

#### Upload the model to the Vertex AI Model registry
````
gcloud ai models upload \
  --container-ports=80 \
  --container-predict-route="/predict" \
  --container-health-route="/health" \
  --region=us-central1 \
  --display-name=similarity-embedding \
  --container-image-uri=gcr.io/sascha-playground-doit/similarity-embedding
````

#### Deploy the model to the Vertex AI Endpoint

CPU
````
gcloud ai endpoints deploy-model 3487883979770560512 \
  --project=sascha-playground-doit \
  --region=us-central1 \
  --model=1355251435326930944 \
  --traffic-split=0=100 \
  --machine-type="n1-standard-2" \
  --display-name=similarity-embedding
````

GPU
````
gcloud ai endpoints deploy-model 3487883979770560512 \
  --project=sascha-playground-doit \
  --region=us-central1 \
  --model=1355251435326930944 \
  --traffic-split=0=100 \
  --machine-type="n1-standard-2" \
  --accelerator count=1,type=nvidia-tesla-t4 \
  --display-name=similarity-embedding
````


### 2. Create backfill data
see [Backfilling](#Backfilling) needed for step 3

### 3. Initial one-time setup Matching Engine
The Matching Engine service requires a one time setup. Creating the streaming index is currently not support via `gcloud` therefore we us a API call as workaround.

#### Create Streaming Index (not yet supported via gcloud, therfore workaround via curl)
```
INPUT_GCS_DIR=gs://similarity-demo/data/
DIMENSIONS=768
DISPLAY_NAME=similarity
PROJECT_ID=sascha-playground-doit
ENDPOINT=us-central1-aiplatform.googleapis.com
REGION=us-central1

curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer `gcloud auth print-access-token`" \
https://${ENDPOINT}/v1/projects/${PROJECT_ID}/locations/${REGION}/indexes \
-d '{
    displayName: "'${DISPLAY_NAME}'",
    description: "'${DISPLAY_NAME}'",
    metadata: {
       contentsDeltaUri: "'${INPUT_GCS_DIR}'",
       config: {
          dimensions: "'${DIMENSIONS}'",
          approximateNeighborsCount: 150,
          distanceMeasureType: "DOT_PRODUCT_DISTANCE",
          algorithmConfig: {
             bruteForceConfig: {}
          }
       },
    },
    indexUpdateMethod: "STREAM_UPDATE"
}'
```

#### Create Endpoint
```
!gcloud ai index-endpoints create \
  --display-name="similarity_endpoint" \
  --network="projects/234439745674/global/networks/matching-engine-vpc-network" \
  --project="sascha-playground-doit" \
  --region="us-central1"
```

#### Deploy Index 
````
!gcloud ai index-endpoints deploy-index "<insert endpoint ID>" \
  --deployed-index-id="similarity_deployed_v2" \
  --display-name="similarity index deployed" \
  --index="<insert index ID>" \
  --project="sascha-playground-doit" \
  --region="us-central1"
````

### 4. API Deployment 

The API has environemnt variables adapt them accordinly.

To deploy the API by running `gcloud build submit --config cloudbuild.yaml` in the corresponding subfolder. 
