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
            parts = [p.strip() for p in content.split(",")]
            joined = " << \" \" << ".join(parts)
            cpp_lines.append(f"std::cout << {joined} << std::endl;")

        elif "input(" in line:
            var = line.split("=")[0].strip()
            cpp_lines.append(f"std::string {var};")
            cpp_lines.append(f"std::cin >> {var};")

        elif line.startswith("for ") and "in range(" in line:
            loop_var = line.split("in")[0].replace("for", "").strip()
            range_part = line.split("range(")[1].split(")")[0]
            if "," in range_part:
                parts = [x.strip() for x in range_part.split(",")]
                if len(parts) == 2:
                    start, end = parts
                    cpp_lines.append(f"for (int {loop_var} = {start}; {loop_var} < {end}; {loop_var}++) {{")
                elif len(parts) == 3:
                    start, end, step = parts
                    cpp_lines.append(f"for (int {loop_var} = {start}; {loop_var} < {end}; {loop_var} += {step}) {{")
            else:
                end = range_part.strip()
                cpp_lines.append(f"for (int {loop_var} = 0; {loop_var} < {end}; {loop_var}++) {{")

        elif "=" in line:
            var, val = line.split("=")
            cpp_lines.append(f"int {var.strip()} = {val.strip()};")

        elif line.startswith("if "):
            condition = line[3:].strip().rstrip(":")
            cpp_lines.append(f"if ({condition}) {{")

        elif line.startswith("elif "):
            condition = line[5:].strip().rstrip(":")
            cpp_lines.append(f"}} else if ({condition}) {{")

        elif line.startswith("else"):
            cpp_lines.append("} else {")

        elif line == "":
            cpp_lines.append("")

        else:
            cpp_lines.append(f"// {line}")

    cpp_lines.append("  }")
    cpp_lines.append("}")
    return "\n".join(cpp_lines)

def python_to_java(code):
    lines = code.strip().split('\n')
    java_lines = [
        "// Java code converted from Python:",
        "import java.util.Scanner;",
        "public class Main {",
        "  public static void main(String[] args) {",
        "    Scanner scanner = new Scanner(System.in);"
    ]

    declared_vars = set()

    for line in lines:
        line = line.strip()

        if "input(" in line:
            var = line.split("=")[0].strip()
            if var not in declared_vars:
                java_lines.append(f"    String {var} = scanner.nextLine();")
                declared_vars.add(var)
            else:
                java_lines.append(f"    {var} = scanner.nextLine();")

        elif line.startswith("print("):
            content = line[6:-1].strip()
            parts = [p.strip() for p in content.split(",")]
            joined = " + \" \" + ".join(parts)
            java_lines.append(f"    System.out.println({joined});")

        elif line.startswith("for ") and "in range(" in line:
            loop_var = line.split("in")[0].replace("for", "").strip()
            range_part = line.split("range(")[1].split(")")[0]
            if "," in range_part:
                parts = [x.strip() for x in range_part.split(",")]
                if len(parts) == 2:
                    start, end = parts
                    java_lines.append(f"    for (int {loop_var} = {start}; {loop_var} < {end}; {loop_var}++) {{")
                elif len(parts) == 3:
                    start, end, step = parts
                    java_lines.append(f"    for (int {loop_var} = {start}; {loop_var} < {end}; {loop_var} += {step}) {{")
            else:
                end = range_part.strip()
                java_lines.append(f"    for (int {loop_var} = 0; {loop_var} < {end}; {loop_var}++) {{")

        elif "=" in line:
            var, val = line.split("=")
            var = var.strip()
            val = val.strip()
            if var not in declared_vars:
                java_lines.append(f"    int {var} = {val};")
                declared_vars.add(var)
            else:
                java_lines.append(f"    {var} = {val};")

        elif line.startswith("if "):
            condition = line[3:].strip().rstrip(":")
            java_lines.append(f"    if ({condition}) {{")

        elif line.startswith("elif "):
            condition = line[5:].strip().rstrip(":")
            java_lines.append(f"    }} else if ({condition}) {{")

        elif line.startswith("else"):
            java_lines.append("    } else {")

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
