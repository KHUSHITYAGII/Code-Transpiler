import React, { useState } from "react";

function App() {
  const [code, setCode] = useState("");
  const [sourceLang, setSourceLang] = useState("python");
  const [targetLang, setTargetLang] = useState("cpp");
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");

  const handleConvert = async () => {
    if (!code.trim()) {
      setError("Please enter valid code.");
      return;
    }
    try {
      setError(""); // Clear previous errors
      const response = await fetch("http://127.0.0.1:5000/api/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, sourceLang, targetLang }),
      });
      const data = await response.json();
      if (response.ok) {
        setOutput(data.convertedCode);
      } else {
        setError(data.error || "An error occurred during conversion.");
      }
    } catch (err) {
      setError("Failed to connect to the server.");
    }
  };

  return (
    <div className="container">
      <h1>Bidirectional Code Converter</h1>

      {/* Input Section */}
      <textarea
        placeholder="Enter your code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      {/* Language Selection */}
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: "10px" }}>
        <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
          <option value="python">Python</option>
          <option value="cpp">C++</option>
          <option value="java">Java</option>
        </select>
        <span>➡️</span>
        <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
          <option value="cpp">C++</option>
          <option value="java">Java</option>
          <option value="python">Python</option>
        </select>
      </div>

      {/* Convert Button */}
      <button onClick={handleConvert}>Convert</button>

      {/* Error Notification */}
      {error && <p className="error">{error}</p>}

      {/* Output Section */}
      <div className="output">
        <strong>Converted Code:</strong>
        <pre>{output || "Your converted code will appear here."}</pre>
      </div>
    </div>
  );
}

export default App;
