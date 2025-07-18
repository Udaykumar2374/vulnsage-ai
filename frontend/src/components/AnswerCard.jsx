function AnswerCard({ answer }) {
  return (
    <div className="mt-6 bg-gray-50 p-6 rounded-xl border border-gray-200 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-700 mb-2">📌 Answer</h2>
      <p className="text-gray-800 whitespace-pre-line">{answer.result}</p>

      {answer.source_documents?.length > 0 && (
        <>
          <h3 className="mt-4 font-medium text-sm text-gray-500">📚 Source Documents</h3>
          <ul className="list-disc list-inside text-sm text-gray-600 mt-1">
            {answer.source_documents.map((doc, i) => (
              <li key={i}>{doc.metadata?.source || 'Unknown source'}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default AnswerCard;
