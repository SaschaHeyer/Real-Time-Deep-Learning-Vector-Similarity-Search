! curl --header "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  --request POST \
  --data '{"description":"Hi DoIt team! One of my team members is working on Jupyter notebooks inside of a GPU Vertex AI Workbench instance and for some reason, the VM is not able to save the Jupyter notebook to disk and thus all of the work is getting lost. I have looked through the VMs logs in Logs Explorer, but there are no obvious errors or warnings that would give a hint about why this is happening. Could you please help me come up with a new approach for troubleshooting so I can figure out why Workbench is failing to save this notebook to disk? Kindest regards, Camilla"}' \
  https://ticket-similarity-api-xgdxnb6fdq-uc.a.run.app/query