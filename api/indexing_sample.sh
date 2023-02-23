! curl --header "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  --request POST \
  --data '{"description":"We use Vision API to detect logos but run into an error","id":"5000"}' \
  https://ticket-similarity-api-xgdxnb6fdq-uc.a.run.app/insert