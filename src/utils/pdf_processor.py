from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(file_path):
    reader = PdfReader(file_path)
    documents = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            documents.append({
                "source": file_path.name,
                "page": page_number + 1,
                "text": text,
            })
    return documents

def load_all_pdfs(folder_path):
    folder = Path(folder_path)
    all_documents = []

    for pdf_file in folder.glob("*.pdf"):
        print(f"Loading: {pdf_file.name}")
        documents = load_pdf(pdf_file)
        all_documents.extend(documents)

    return all_documents

def create_chunks(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = []
    chunk_id = 0

    for doc in documents:
        split_texts = splitter.split_text(doc["text"])
        for text in split_texts:
            chunks.append({
                "chunk_id": chunk_id,
                "source": doc["source"],
                "page": doc["page"],
                "text": text
            })
            chunk_id += 1

    return chunks