import razorpay
import json
import hmac
import hashlib
import requests


RAZORPAY_KEY_ID = 'rzp_test_QHr92YLrM32wuq'
RAZORPAY_SECRET = "ydDdWNCyrrvwn7GvVwdZ9jWK"
WEBHOOK_SECRET = "my_secret_123456@#$%"



# ✅ Initialize Razorpay Client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))

# ✅ Sample Webhook Data (Modify as needed)
payload = {
    "event": "payment.captured",
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_29QQoUBi66xm2f",
                "order_id": "order_9A33XWu170gUtm",
                "amount": 5000
            }
        }
    }
}

# ✅ Convert payload to JSON string
payload_json = json.dumps(payload, separators=(",", ":"))

# ✅ Generate Signature using Webhook Secret
signature = hmac.new(WEBHOOK_SECRET.encode(), payload_json.encode(), hashlib.sha256).hexdigest()

# ✅ Send Webhook POST Request
response = requests.post(
    "https://af2b-2402-a00-404-ca4f-e098-507b-d058-8b2b.ngrok-free.app/payment/razorpay/webhook/",  # Replace with your actual webhook URL
    headers={
        "Content-Type": "application/json",
        "X-Razorpay-Signature": signature
    },
    data=payload_json
)

# ✅ Print Response
print("Webhook Response:", response.status_code, response.text)
