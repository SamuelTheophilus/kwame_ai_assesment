from flask import Flask, request, jsonify, make_response
from indexing import index_name, index_document
from model import model
import docx
from parsing import read_files, divide_passage_into_chunks
from retrieval import retrieve_passages
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import PyPDF2
import traceback

app = Flask(__name__)


@app.get("/")
def home():
    return "Home"


@app.post('/api/question')
def receive_question():
    try:
        data = request.get_json()
        question = data.get('question')
        if not question:
            return jsonify({'error': 'Missing question'}), 400

        # Retrieve relevant passages using your passage retrieval logic
        passages, _, _ = retrieve_passages(index_name, question, top_k=3, model=model)

        # Return the passages as JSON response
        return jsonify({'passages': passages}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.post('/api/upload-document')
def upload_document():
    uploaded_file = request.files["file"]
    print(uploaded_file)
    if uploaded_file.filename == '': return make_response(jsonify({"Error": "No file uploaded"}), 400)

    file_extension = uploaded_file.filename.split(".")[-1].lower()
    if file_extension == "pdf" or file_extension == "docx" or file_extension == "txt":
        text, metadata = extract_text_and_metadata(uploaded_file, file_type=file_extension)
    else:
        return make_response(jsonify({"error": "Unsupported file type"}), 400)

    try: 
        index_document(text, metadata)
        return make_response(jsonify({"Success": "Your File has been successfully indexed"}), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({"Error": "error occured while processing file"}), 500)
    


# Utilities
def extract_text_and_metadata(uploaded_file, file_type: str):
    if file_type == "pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            page = pdf_reader.pages[0]
            text = page.extract_text()
            print(text)
        except Exception as e:
            print(f"Error {e}")
            traceback.print_exc()
            return None, None
        
        metadata = pdf_reader.metadata
        return text, metadata
    
    if file_type == "docx":
        doc = docx.Document(uploaded_file)
        fullText = []
        for paragragh in doc.paragraphs:
            fullText.append(paragragh.text)
        text = '\n'.join(fullText)

        metadata = {}
        prop = doc.core_properties
        for data in dir(prop):
            if not data.startswith('_'):
                metadata[data] = getattr(prop)    
        return text, metadata
    
    if file_type == "txt":
        with open(uploaded_file, 'r', encoding= 'utf-8') as text_file:
            text = text_file.readlines()
        metadata = {} # .txt files contain no metadata.
    
        return text, metadata


if __name__ == "__main__":
    app.run(debug=True, port=4000)
