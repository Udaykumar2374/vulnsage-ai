import { useState } from "react";
import FileUpload from "./components/FileUpload";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnswer(null);
    setSources([]);

    try {
      const formData = new FormData();
      formData.append("query", query);

      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (res.ok) {
        setAnswer(data.answer);
        setSources(data.sources);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Could not reach backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-10">
      <div className="max-w-2xl mx-auto space-y-6">
        {/* 🧠 Title */}
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-2">🧠 VulnSage AI Assistant</h1>
          <p className="text-gray-600 text-sm">Upload reports or ask questions below</p>
        </div>

        {/* 📄 File Upload */}
        <FileUpload />

        {/* 💬 Query Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow p-6 space-y-4">
          <textarea
            className="w-full border border-gray-300 rounded-md p-3 resize-none focus:outline-none focus:ring focus:ring-blue-400"
            rows="4"
            placeholder="Ask something about your docs..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
          ></textarea>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>

        {/* 🔴 Error Message */}
        {error && (
          <div className="text-red-600 text-sm text-center">{error}</div>
        )}

        {/* ✅ Answer Display */}
        {answer && (
          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-2">Answer:</h2>
            <p className="text-gray-800">{answer}</p>

            {sources.length > 0 && (
              <div className="mt-4 text-sm text-gray-500">
                <span className="font-medium">Sources:</span>
                <ul className="list-disc list-inside">
                  {sources.map((src, idx) => (
                    <li key={idx}>{src}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
