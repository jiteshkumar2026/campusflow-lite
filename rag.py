import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from llm import get_llm

PROMPT = ChatPromptTemplate.from_template(
    """You are a college assistant. Answer ONLY using the context below.
If the answer is not in the context, say "I couldn't find this in the uploaded documents."
Mention the document name and page when relevant.

Context:
{context}

Question: {question}
Answer:"""
)

CONDENSE_PROMPT = ChatPromptTemplate.from_template(
    """Given the chat history and a follow-up question, rewrite the follow-up
as a standalone question that includes any needed context from the history.
If it is already standalone, return it unchanged. Output ONLY the question.

Chat history:
{history}

Follow-up question: {question}
Standalone question:"""
)

class RAGStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        self.db = None
        self.chain = PROMPT | get_llm()
        self.condense = CONDENSE_PROMPT | get_llm(temperature=0)

    def add_pdf(self, file, filename):
        """file = path or Streamlit UploadedFile. Returns number of chunks added."""
        tmp_path = None
        if hasattr(file, "getvalue"):                 # Streamlit upload
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(file.getvalue())
                tmp_path = tmp.name
            path = tmp_path
        else:
            path = file
        try:
            pages = PyPDFLoader(path).load()
        finally:
            if tmp_path:
                os.remove(tmp_path)

        for p in pages:
            p.metadata["source"] = filename
            p.metadata["page"] = p.metadata.get("page", 0) + 1   # make it 1-based

        chunks = [c for c in self.splitter.split_documents(pages) if c.page_content.strip()]
        if not chunks:
            return 0          # likely a scanned PDF with no text layer
        if self.db is None:
            self.db = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.db.add_documents(chunks)
        return len(chunks)

    def answer(self, question, history=None, k=4):
        """history = list of (question, answer) tuples, oldest first."""
        if self.db is None:
            return {"answer": "Please upload a PDF first.", "sources": []}

        standalone = question
        if history:
            hist_text = "\n".join(
                f"User: {q}\nAssistant: {a[:400]}" for q, a in history[-3:]
            )
            try:
                standalone = self.condense.invoke(
                    {"history": hist_text, "question": question}
                ).content.strip() or question
            except Exception:
                standalone = question      # fall back to the raw question

        docs = self.db.similarity_search(standalone, k=k)
        context = "\n\n".join(
            f"[{d.metadata['source']}, page {d.metadata['page']}]\n{d.page_content}"
            for d in docs
        )
        reply = self.chain.invoke({"context": context, "question": standalone})
        return {
            "answer": reply.content,
            "sources": [{"source": d.metadata["source"], "page": d.metadata["page"]} for d in docs],
            "searched_for": standalone,
        }
    def reset(self):
        self.db = None

    # Day 3: persist the index so students don't re-upload every time
    def save(self, folder="faiss_index"):
        if self.db:
            self.db.save_local(folder)

    def load(self, folder="faiss_index"):
        if os.path.isdir(folder):
            self.db = FAISS.load_local(folder, self.embeddings, allow_dangerous_deserialization=True)