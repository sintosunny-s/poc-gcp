from google.cloud import firestore
from flask import Request, jsonify
import datetime

db = firestore.Client()

def toggleScaling(request: Request):
    path = request.path.lower()  # /enable, /disable, /status

    # status → return current Firestore flag
    if "status" in path:
        doc = db.collection("settings").document("scaling").get()
        return jsonify(doc.to_dict()), 200

    # disable = override = True
    override = "disable" in path

    db.collection("settings").document("scaling").set({
        "override": override,
        "updated_by": "developer",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

    msg = "DISABLED" if override else "ENABLED"
    return f"Nightly scaling is now {msg}", 200
