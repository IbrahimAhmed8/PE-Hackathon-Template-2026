import re
from flask import request, jsonify

THREAT_SIGNATURES = [
    re.compile(r"(union\s+select|drop\s+table|insert\s+into|select\s+.*from|delete\s+from|--|#|/\*|\*/)", re.IGNORECASE),
    
    re.compile(r"(<script|<iframe|<object|<embed|<svg|<body|<applet|<meta|<style|<link|<img|<details)", re.IGNORECASE),

    re.compile(r"(on\w+\s*=)", re.IGNORECASE),
    re.compile(r"(javascript:|data:|vbscript:)", re.IGNORECASE),
    
    re.compile(r"(\.\./\.\./|/etc/passwd|/etc/shadow|/bin/sh|/bin/bash|c:\\windows|boot\.ini)", re.IGNORECASE),
    
    re.compile(r"([;&|`$])", re.IGNORECASE)
]

def check_malicious_payloads():
    if request.path == '/health':
        return None
    
    for key, value in list(request.args.items()):
        val_str = str(value)
        for sig in THREAT_SIGNATURES:
            if sig.search(val_str):
                return jsonify({
                    "error": "RASP Alert: Malicious activity detected in query parameters",
                    "attack_type": "Signature Match",
                    "code": 403
                }), 403

    if request.is_json:
        data = request.get_json(silent=True)
        if data and isinstance(data, dict):
            for key, value in data.items():
                val_str = str(value)
                for sig in THREAT_SIGNATURES:
                    if sig.search(val_str):
                        return jsonify({
                            "error": "RASP Alert: Malicious payload detected in JSON body",
                            "attack_type": "Signature Match",
                            "code": 403
                        }), 403
                        
    return None