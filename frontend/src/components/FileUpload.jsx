import { useState } from "react";

import axios from "axios";

function FileUpload() {
  const [fileInfo, setFileInfo] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData);
      setFileInfo(res.data);
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  return (
    <div className="p-4 border rounded-xl shadow-md bg-white max-w-xl mx-auto">
      <h2 className="text-lg font-bold mb-2">📄 Upload Vulnerability Report</h2>
      <input
        type="file"
        accept=".txt"
        onChange={handleUpload}
        className="mb-4"
      />
      {fileInfo && (
        <div className="text-sm mt-2">
          <p><strong>Name:</strong> {fileInfo.filename}</p>
          <p><strong>Size:</strong> {fileInfo.size} bytes</p>
          <p><strong>Preview:</strong></p>
          <pre className="bg-gray-100 p-2 rounded">{fileInfo.preview}</pre>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
