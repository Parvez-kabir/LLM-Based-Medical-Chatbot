import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# -------------------------
# 0. ENVIRONMENT VARIABLES
# -------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyAarZoEBynPWDDjCWR5V1kPMu1BqHVK5uc"
os.environ["PINECONE_API_KEY"] = "pcsk_4PVqUk_GFd8auKDU7qwffoZZvcP2p4DE7CWTS221cYiw6cRjrEoUtNfQcQPQCf1kCLqZuG"
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("❌ GOOGLE_API_KEY missing!")

if PINECONE_API_KEY is None:
    raise ValueError("❌ PINECONE_API_KEY missing!")

# -------------------------
# 1. Embeddings
# -------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------
# 2. Pinecone Setup
# -------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "law-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# -------------------------
# 3. Load Vectorstore
# -------------------------
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# -------------------------
# 4. Gemini Model
# -------------------------
chatmodel = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2
)

# -------------------------
# 5. Prompt Template
# -------------------------
system_prompt = (
    "You are a Law Assistant specialized in the Penal Code and CrPC, "
    
    "\n\n"
    "{context}"
)

from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# -------------------------
# 6. RAG Chain
# -------------------------
question_answer_chain = create_stuff_documents_chain(chatmodel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# -------------------------
# 7. Flask App
# -------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.form.get("user_input")
    if not user_msg:
        return jsonify({"error": "No input provided"}), 400

    # Get answer from RAG chain
    response = rag_chain.invoke({"input": user_msg})
    bot_msg = response.get("answer", "Sorry, I could not answer that.")

    return jsonify({"answer": bot_msg})

if __name__ == "__main__":
    app.run(debug=True)
