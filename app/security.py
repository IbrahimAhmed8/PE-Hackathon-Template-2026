import re
from flask import request, jsonify

THREAT_SIGNATURES = [
    re.compile(r"(union\s+select|drop\s+table|insert\s+into)", re.IGNORECASE),
    re.compile(r"(<script>|javascript:|onerror=)", re.IGNORECASE),
    re.compile(r"(\.\./\.\./|/etc/passwd)", re.IGNORECASE)
]

def check_malicious_payloads():
    for key, value in request.args.items():
        for sig in THREAT_SIGNATURES:
            if sig.search(value):
                return jsonify({"error": "RASP Alert: Malicious query parameter detected", "code": 403}), 403

    if request.is_json:
        data = request.get_json()
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    for sig in THREAT_SIGNATURES:
                        if sig.search(value):
                            return jsonify({"error": "RASP Alert: Malicious JSON payload detected", "code": 403}), 403
    return None
