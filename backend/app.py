from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app, origins=["https://code-transpilerrr.netlify.app"])  # ✅ Match frontend domain

@app.route("/")
def home():
    return "Flask backend is running!"

# --- Python to C++ Conversion Logic ---
def python_to_cpp(code):
    lines = code.split("\n")
    converted_lines = ["// C++ code converted from Python:"]

    for line in lines:
        line = line.strip()

        # Handle variable assignment (e.g., x = 10)
        match = re.match(r"(\w+)\s*=\s*(\d+)", line)
        if match:
            var, value = match.groups()
            converted_lines.append(f"int {var} = {value};")
            continue

        # Handle print statements (e.g., print("value", x))
        if line.startswith("print(") and line.endswith(")"):
            content = line[6:-1]
            parts = [p.strip() for p in content.split(",")]
            cpp_print = 'std::cout << ' + ' << '.join(parts) + ' << std::endl;'
            converted_lines.append(cpp_print)
            continue

        # If line doesn't match, comment it
        converted_lines.append(f"// {line}")

    return "\n".join(converted_lines)

# --- Python to Java Placeholder ---
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
