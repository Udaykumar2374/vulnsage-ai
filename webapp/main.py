import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAISS vector index
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("vectorstore_index", embeddings, allow_dangerous_deserialization=True)

# Setup Retriever + LLM
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# JSON POST route for React
@app.post("/query")
async def ask_query(query: str = Form(...)):
    try:
        result = qa_chain.invoke({"query": query})
        answer = result["result"]
        sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        return JSONResponse(content={"answer": answer, "sources": sources})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename

        # Save uploaded file
        save_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(contents)

        # Optionally: trigger re-indexing or analysis here

        return {"message": f"Uploaded {filename} successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
