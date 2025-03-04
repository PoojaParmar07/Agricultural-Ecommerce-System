import hmac
import hashlib
import json
import base64

# Webhook secret from Razorpay dashboard
webhook_secret = "settings.RAZORPAY_WEBHOOK_SECRET"

# Sample payload (convert to JSON string without spaces)
payload = {
    "event": "payment.authorized",
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_test",
                "order_id": "order_test",
                "amount": 202500
            }
        }
    }
}
payload_json = json.dumps(payload, separators=(',', ':'))  # Ensure compact JSON

# Generate HMAC SHA256 signature
signature = hmac.new(
    webhook_secret.encode('utf-8'), 
    payload_json.encode('utf-8'), 
    hashlib.sha256
).hexdigest()

print("Generated Signature:", signature)
