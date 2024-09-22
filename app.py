from flask import Flask, request, jsonify
import base64
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/bfhl', methods=['GET', 'POST'])
def bfhl():
    if request.method == 'GET':
        # Hardcoded response for GET request
        return jsonify({"operation_code": 1}), 200

    elif request.method == 'POST':
        data = request.json
        if not data or "data" not in data:
            return jsonify({"is_success": False, "error": "Invalid input"}), 400

        # Extract user details (hardcoded for this example)
        user_id = "krishna-venkatesan-14_04_2004"
        email = "kg5300@srmist.edu.in"
        roll_number = "RA2111043010028"

        # Separate numbers and alphabets
        numbers = []
        alphabets = []
        highest_lowercase_alphabet = []

        for item in data["data"]:
            if item.isdigit():
                numbers.append(item)
            elif item.isalpha():
                alphabets.append(item)
                # Check for lowercase alphabets
                if item.islower():
                    highest_lowercase_alphabet.append(item)

        # Find the highest lowercase alphabet
        highest_lowercase_alphabet = [max(highest_lowercase_alphabet)] if highest_lowercase_alphabet else []

        # File handling
        file_valid = False
        file_mime_type = None
        file_size_kb = None
        if "file_b64" in data:
            try:
                # Decode the base64 file
                file_data = base64.b64decode(data["file_b64"])
                file_size_kb = len(file_data) / 1024  # Convert to KB

                # Example to derive MIME type based on file header (optional, could be improved)
                file_mime_type = "application/octet-stream"
                if data["file_b64"].startswith("/9j/"):  # Simple check for JPEG
                    file_mime_type = "image/jpeg"
                elif data["file_b64"].startswith("iVBOR"):  # Check for PNG
                    file_mime_type = "image/png"

                file_valid = True
            except Exception as e:
                print("File decoding error:", e)
                file_valid = False

        # Create response
        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_lowercase_alphabet,
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": round(file_size_kb, 2) if file_size_kb else None
        }

        return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
