from google.cloud import firestore
from google.cloud import container_v1
from flask import Request

db = firestore.Client()
container_client = container_v1.ClusterManagerClient()

def nightlyScale(request: Request):
    # read flag from Firestore
    doc = db.collection("settings").document("scaling").get()
    data = doc.to_dict() or {}

    override = data.get("override", False)
    if override:
        return "Skipped due to override", 200

    # GKE identifiers (replace values)
    project_id = "PROJECT_ID"
    location = "asia-south1-a"
    cluster_name = "mycluster"
    node_pool_id = "default-pool"

    # name format required by GKE API
    parent = f"projects/{project_id}/locations/{location}/clusters/{cluster_name}"

    request_obj = container_v1.SetNodePoolSizeRequest(
        name=f"{parent}/nodePools/{node_pool_id}",
        node_count=1
    )

    # perform scaling
    container_client.set_node_pool_size(request=request_obj)

    return "Scaled down using GKE API", 200
