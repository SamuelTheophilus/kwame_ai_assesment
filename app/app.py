from flask import Flask, request, jsonify
from indexing import index_name
from model import model
from retrieval import retrieve_passages
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
        passages = retrieve_passages(index_name, question, top_k = 3, model = model)

        # Return the passages as JSON response
        return jsonify({'passages': passages}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, port=4000)