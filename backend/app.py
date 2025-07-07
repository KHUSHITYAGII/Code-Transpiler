from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://code-transpilerrr.netlify.app"])  # ✅ correct origin

@app.route("/")
def home():
    return "Flask backend is running!"

def python_to_cpp(code):
    return f"// C++ code converted from Python:\n{code}"

def python_to_java(code):
    return f"// Java code converted from Python:\n{code}"

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    code = data.get("code")
    source_lang = data.get("source_lang")
    target_lang = data.get("target_lang")

    try:
        if source_lang == "python" and target_lang == "cpp":
            converted_code = python_to_cpp(code)
        elif source_lang == "python" and target_lang == "java":
            converted_code = python_to_java(code)
        else:
            return jsonify({"error": "Unsupported language conversion"}), 400

        return jsonify({"converted_code": converted_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
