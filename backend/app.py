from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# ✅ Allow only your Netlify frontend for better security
CORS(app, origins=["https://code-transpilerr.netlify.app"])

@app.route("/")  # For Render check
def home():
    return "Flask backend is running!"

# --- Code Conversion Logic ---
def python_to_cpp(code):
    code = code.replace("input(", "std::cin >> ")
    code = code.replace("print(", "std::cout << ").replace(")", " << std::endl;")
    code = code.replace("if ", "if (").replace(":", ") {")
    code = code.replace("else:", "} else {")
    code = code.replace("elif ", "} else if (").replace(":", ") {")
    code = code.replace("for ", "for (").replace(" in range(", "; ")
    code = code.replace("):", ") {")
    code += "\n}"
    code = code.replace("<< std) {) {", "<< std::endl;")
    code = code.replace("std) {) {", "std::")
    code = code.replace("<< std::endl;endl;", "<< std::endl;")
    return code

def python_to_java(code):
    code = code.replace("print(", "System.out.println(").replace(")", ");")
    code = code.replace("input(", "Scanner scanner = new Scanner(System.in); String ")
    code = code.replace(" = input()", " = scanner.nextLine();")
    code = code.replace("if ", "if (").replace(":", ") {")
    code = code.replace("else:", "} else {")
    code = code.replace("elif ", "} else if (").replace(":", ") {")
    code = code.replace("for ", "for (int ").replace(" in range(", "; ")
    code = code.replace("):", ") {")
    code += "\n}"
    code = code.replace("<< std) {) {", ");")
    return code

# ✅ Updated to match frontend keys and return correct JSON format
@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    code = data.get("code")
    source_lang = data.get("source_lang")  # match frontend (snake_case)
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
