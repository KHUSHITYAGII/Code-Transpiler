from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")  # ✅ This route is required for sanity check on Render
def home():
    return "Flask backend is running!"

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

@app.route("/api/convert", methods=["POST"])
def convert():
    data = request.json
    code = data.get("code")
    source_lang = data.get("sourceLang")
    target_lang = data.get("targetLang")

    try:
        if source_lang == "python" and target_lang == "cpp":
            converted_code = python_to_cpp(code)
        elif source_lang == "python" and target_lang == "java":
            converted_code = python_to_java(code)
        else:
            return jsonify({"error": "Unsupported language conversion"}), 400

        return jsonify({"convertedCode": converted_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
