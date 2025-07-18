import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ updated import
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# === Step 0: Load environment variables ===
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# === Step 1: Load or Create Vectorstore ===
VECTORSTORE_PATH = "vectorstore_index"

if os.path.exists(VECTORSTORE_PATH):
    print("🔁 Loading existing FAISS index...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
else:
    print("📚 Loading documents and building vectorstore...")
    data_dir = "./knowledge_base"
    docs = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(data_dir, filename))
            docs.extend(loader.load())

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)
    print("✅ FAISS index saved to:", VECTORSTORE_PATH)

# === Step 2: Set up LLM + RetrievalQA ===
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

# === Step 3: Interactive CLI ===
print("\n💬 Ask your cybersecurity questions! (type 'exit' to quit)\n")
while True:
    query = input("🧠 Your question: ")
    if query.lower().strip() in ["exit", "quit"]:
        print("👋 Exiting. Stay secure!")
        break

    result = qa_chain.invoke({"query": query})
    print("\n📌 Answer:\n" + result["result"])

    print("\n📚 Source Documents:")
    for doc in result["source_documents"]:
        print("-", doc.metadata.get("source", "Unknown"))
    print("\n" + "-" * 60 + "\n")
