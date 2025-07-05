from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def python_to_cpp(code):
    # Replace input statements
    code = code.replace("input(", "std::cin >> ")
    
    # Replace print statements
    code = code.replace("print(", "std::cout << ").replace(")", " << std::endl;")
    # Replace if statements
    code = code.replace("if ", "if (").replace(":", ") {")
    code = code.replace("else:", "} else {")
    code = code.replace("elif ", "} else if (").replace(":", ") {")
    
    # Replace for loops
    code = code.replace("for ", "for (").replace(" in range(", "; ")
    code = code.replace("):", ") {")
    
    # Add closing braces for blocks
    code += "\n}"  # Ensure all blocks are closed properly
    
    # Fix common issues with curly braces and semicolons
    code = code.replace("<< std) {) {", "<< std::endl;")  # Fix misplaced braces
    code = code.replace("std) {) {", "std::")  # Fix std:: prefix
    code = code.replace("<< std::endl;endl;", "<< std::endl;")  # Remove redundant endl;
    
    return code

def python_to_java(code):
    # Replace print statements
    code = code.replace("print(", "System.out.println(").replace(")", ");")
    
    # Replace input statements
    code = code.replace("input(", "Scanner scanner = new Scanner(System.in); String ")
    code = code.replace(" = input()", " = scanner.nextLine();")
    
    # Replace if statements
    code = code.replace("if ", "if (").replace(":", ") {")
    code = code.replace("else:", "} else {")
    code = code.replace("elif ", "} else if (").replace(":", ") {")
    
    # Replace for loops
    code = code.replace("for ", "for (int ").replace(" in range(", "; ")
    code = code.replace("):", ") {")
    
    # Add closing braces for blocks
    code += "\n}"  # Ensure all blocks are closed properly
    
    # Fix common issues with curly braces and semicolons
    code = code.replace("<< std) {) {", ");")  # Fix misplaced braces
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
            return jsonify({"convertedCode": converted_code})
        elif source_lang == "python" and target_lang == "java":
            converted_code = python_to_java(code)
            return jsonify({"convertedCode": converted_code})
        else:
            return jsonify({"error": "Unsupported language conversion"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)