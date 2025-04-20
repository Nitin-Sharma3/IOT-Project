from flask import Flask, request, jsonify
import pyotp
import os

app = Flask(__name__)

# Use OTP_SECRET from environment variables
otp_secret = os.environ.get("OTP_SECRET")

@app.route("/")
def index():
    return "✅ OTP Generator Running!"

@app.route("/generate-otp")
def generate_otp():
    if not otp_secret:
        return jsonify({"error": "OTP_SECRET not set"}), 500
    totp = pyotp.TOTP(otp_secret)
    return jsonify({"otp": totp.now()})

@app.route("/validate-otp", methods=["POST"])
def validate_otp():
    if not otp_secret:
        return jsonify({"error": "OTP_SECRET not set"}), 500
    data = request.get_json()
    otp = data.get("otp")
    totp = pyotp.TOTP(otp_secret)
    if totp.verify(otp):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run()
