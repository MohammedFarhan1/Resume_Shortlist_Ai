from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdfplumber
from groq import Groq

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Add a test route to verify the server is running
@app.route('/', methods=['GET'])
def test():
    return jsonify({"status": "success", "message": "Server is running!"})

# Initialize Groq client with direct API key
client = Groq(
    api_key="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"
)

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
    return text.strip()

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        print("📌 Request received.")  

        if 'file' not in request.files:
            print("❌ No file provided in request.")  
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        
        # Validate file size (10MB limit)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > 10 * 1024 * 1024:
            return jsonify({"error": "File size too large. Please upload a file smaller than 10MB"}), 400

        # Save file to temporary location
        os.makedirs("./uploads", exist_ok=True)
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)
        print(f"📂 File saved at {file_path}")  

        # Extract text from PDF
        pdf_content = extract_text_from_pdf(file_path)
        if not pdf_content:
            print("❌ PDF extraction failed. No text found.")  
            return jsonify({"error": "PDF extraction failed. No text found in the document."}), 500

        print("📄 Extracted PDF Content:", pdf_content[:500])  

        # Process with Groq API
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the best and most helpful AI assistant. I will provide a PDF file, "
                        "and your task is to remove all personal details such as names, email addresses, "
                        "phone numbers, social media links, and other identifying information. Ensure that "
                        "the remaining content, including sentences and words, is returned in the exact same "
                        "order and format as the original file, without altering its structure or layout."
                    )
                },
                {
                    "role": "user",
                    "content": f"Here is the PDF content:\n{pdf_content}"
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0
        )

        # Extract cleaned text from API response
        cleaned_text = response.choices[0].message.content
        
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify({"cleaned_text": cleaned_text})

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        # Clean up temporary file in case of error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='127.0.0.1', port=5000, debug=True)
