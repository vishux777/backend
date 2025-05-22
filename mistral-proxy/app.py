from flask import Flask, request, jsonify
   import requests
   import os
   from flask_cors import CORS

   app = Flask(__name__)
   CORS(app, resources={r"/api/mistral": {"origins": ["https://example.com"]}})

   # Mistral API configuration
   MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
   MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

   @app.route("/api/mistral", methods=["POST"])
   def proxy_mistral():
       try:
           # Get the request data from the client
           data = request.get_json()
           if not data:
               return jsonify({"error": "No data provided"}), 400

           # Forward the request to Mistral API
           headers = {
               "Content-Type": "application/json",
               "Authorization": f"Bearer {MISTRAL_API_KEY}"
           }
           response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
           response.raise_for_status()

           # Return Mistral's response to the client
           return jsonify(response.json())
       except requests.exceptions.RequestException as e:
           return jsonify({"error": "API call failed", "details": str(e)}), 500
       except Exception as e:
           return jsonify({"error": "Internal server error", "details": str(e)}), 500

   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
