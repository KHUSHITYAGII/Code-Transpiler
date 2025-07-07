from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://code-transpilerrr.netlify.app"])  # ✅ correct origin

@app.route("/")
def home():
    return "Flask backend is running!"

def python_to_cpp(code):
    lines = code.strip().split('\n')
    cpp_lines = ["// C++ code converted from Python:"]

    for line in lines:
        line = line.strip()

        if line.startswith("print("):
            content = line[6:-1]
            cpp_lines.append(f"std::cout << {content} << std::endl;")

        elif "input(" in line:
            var = line.split("=")[0].strip()
            cpp_lines.append(f"std::string {var};")
            cpp_lines.append(f"std::cin >> {var};")

        elif "=" in line:
            var, val = line.split("=")
            cpp_lines.append(f"int {var.strip()} = {val.strip()};")

        elif line.startswith("if "):
            condition = line[3:-1].strip()
            cpp_lines.append(f"if ({condition}) {{")

        elif line.startswith("elif "):
            condition = line[5:-1].strip()
            cpp_lines.append(f"}} else if ({condition}) {{")

        elif line.startswith("else"):
            cpp_lines.append("} else {")

        elif line.startswith("for "):
            cpp_lines.append("// for-loops not yet implemented")

        elif line == "":
            cpp_lines.append("")

        else:
            cpp_lines.append(f"// {line}")

    cpp_lines.append("}")
    return "\n".join(cpp_lines)

def python_to_java(code):
    lines = code.strip().split('\n')
    java_lines = ["// Java code converted from Python:", "public class Main {", "  public static void main(String[] args) {"]

    for line in lines:
        line = line.strip()

        if "=" in line and "input" not in line:
            var, val = line.split("=")
            java_lines.append(f"    int {var.strip()} = {val.strip()};")

        elif line.startswith("print("):
            content = line[6:-1]
            java_lines.append(f"    System.out.println({content});")

        elif "input(" in line:
            var = line.split("=")[0].strip()
            java_lines.append("    Scanner scanner = new Scanner(System.in);")
            java_lines.append(f"    String {var} = scanner.nextLine();")

        elif line.startswith("if "):
            condition = line[3:-1].strip()
            java_lines.append(f"    if ({condition}) {{")

        elif line.startswith("elif "):
            condition = line[5:-1].strip()
            java_lines.append(f"    }} else if ({condition}) {{")

        elif line.startswith("else"):
            java_lines.append("    } else {")

        elif line.startswith("for "):
            java_lines.append("    // for-loops not yet implemented")

        elif line == "":
            java_lines.append("")

        else:
            java_lines.append(f"    // {line}")

    java_lines.append("  }")
    java_lines.append("}")
    return "\n".join(java_lines)

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
