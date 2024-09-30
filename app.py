from flask import Flask, render_template, request, jsonify
import pickle
import os
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from birth_chart import generate_birth_chart

app = Flask(__name__)

def load_vector_store(vector_path):
    try:
        with open(vector_path, "rb") as f:
            vector_store = pickle.load(f)
        return vector_store
    except FileNotFoundError:
        raise Exception(f"Vector store not found at {vector_path}")
    except Exception as e:
        raise Exception(f"Error loading vector store: {str(e)}")

def create_llm_chain():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ API Key is missing")

    llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert astrologer. Given the astrological context from the user's birth chart, planetary effects and related documents, provide a personalized and insightful astrological response to their query.
        
        Birth Chart Details: 
        {birth_chart}
        
        Planetary Effects:
        {effects}
        
        Relevant Astrological Literature Context:
        {context}
        
        Based on the above, respond to the following user query in detail:
        User Query: {input}
        """
    )
    return llm, prompt

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/astrological_insights', methods=['GET', 'POST'])
def astrological_insights():
    if request.method == 'POST':
        user_data = {
            'name': request.form['name'],
            'dob': request.form['dob'],
            'time_of_birth': request.form['time_of_birth'],
            'place_of_birth': request.form['place_of_birth'],
            'gender': request.form['gender'],
            'query': request.form['query']
        }

        try:
            birth_chart, effects = generate_birth_chart(user_data)

            vector_path = "vector_embedding.pkl"

            vectors = load_vector_store(vector_path)

            llm, prompt = create_llm_chain()
            document_chain = create_stuff_documents_chain(llm, prompt)
            retriever = vectors.as_retriever()
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            relevant_documents = retriever.get_relevant_documents(user_data['query'])
            context = " ".join([doc.page_content for doc in relevant_documents])

            user_prompt = {
                "birth_chart": birth_chart,
                "effects": effects,
                "context": context,
                "input": user_data['query']
            }

            response = retrieval_chain.invoke(user_prompt)

            detailed_answer = response.get('answer', 'No astrological insights available at this time.').replace("**", "")

            return jsonify({
                'answer': detailed_answer,
                'birth_chart': birth_chart,
                'effects': effects
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
