from flask import abort                                         #abort when anything goes wrong
from models import db, Document                                 #database tools
from classifiers import classify_document                       #classification tool
from extractors import extract_text_from_image, extract_text_from_pdf, extract_text_from_docx               #extracting text
from file_type import detect_file_type
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'                            #storing data in documents.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                        #unnecessary modifications not tracked
db.init_app(app)                                                                            #connecting database to web 
app.secret_key = 'secret_key'  

#uploading document path
UPLOAD_FOLDER = 'static/documents'                                                           #stores the uploaded document in 'documents' folder 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)                                                   #creates database/ folders if not present

#admin dashboard
@app.route('/admin')
def admin_dashboard():
    #counts of each file type resume/invoice/medical/others
    #using GROUP_BY query
    doc_counts_query = (
        db.session.query(Document.doc_type, db.func.count(Document.id))
        .group_by(Document.doc_type)
        .all()
    )
    #dictionary list storage of file type & counts
    doc_counts = {doc_type: count for doc_type, count in doc_counts_query}
    total_docs = sum(doc_counts.values())

    search_query = request.args.get("q", "").strip()                                        #search the item
    category = request.args.get("category", "").strip()                                     #search by category selected in filter by user
    

    documents_query = Document.query

    if search_query:
        documents_query = documents_query.filter(Document.filename.ilike(f"%{search_query}%"))

    if category and category.lower() != "all":
        documents_query = documents_query.filter(Document.doc_type == category)

    documents = documents_query.order_by(Document.upload_time.desc()).all()

    return render_template(
        'admin.html',
        documents=documents,
        total_docs=total_docs,
        doc_counts=doc_counts,
        search_query=search_query,
        category=category
    )
#homepage route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    #when no file selected
    if 'file' not in request.files:
        flash('No file part in the request.')
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)                                               #saves file in temporary path
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(temp_path)

    file_type = detect_file_type(temp_path)                                                 #detects the file type (words/pdf/image)

    #extracting text from files using different functions
    if "image" in file_type:
        extracted_text = extract_text_from_image(temp_path)
    elif "pdf" in file_type:
        extracted_text = extract_text_from_pdf(temp_path)
    elif "wordprocessingml" in file_type:
        extracted_text = extract_text_from_docx(temp_path)
    else:
        flash("Unsupported file type.")
        os.remove(temp_path)
        return redirect(url_for('home'))

    doc_type = classify_document(extracted_text)                                            #classifies documents into different folders (invoice/resume/medical/others)

    category_folder = os.path.join(app.config['UPLOAD_FOLDER'], doc_type.lower())           #creates folders for respective files
    os.makedirs(category_folder, exist_ok=True)

    ext = os.path.splitext(filename)[1]                                                     #gets file extension from filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')                                     #converts current time to string
    base_filename = os.path.splitext(filename)[0]                                           #gets filename without the extension
    unique_filename = f"{base_filename}_{timestamp}{ext}"                                   #base filename + '_' + current time + extension = unique filename

    final_path = os.path.join(category_folder, unique_filename)                             #moves the file from temporary path to final folder
    os.rename(temp_path, final_path)

    db_file_path = final_path.replace('static/', '')

    new_doc = Document(
        filename=unique_filename,
        file_path=db_file_path,
        doc_type=doc_type,
        extracted_text=extracted_text
    )
    db.session.add(new_doc)
    db.session.commit()

    flash(f'File uploaded successfully as {unique_filename} and classified as {doc_type}')
    return redirect(url_for('home'))

@app.route('/documents')
def view_documents():
    # Search parameters
    search_query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    documents_query = Document.query

    if search_query:
        documents_query = documents_qugiery.filter(Document.filename.ilike(f"%{search_query}%"))

    if category and category.lower() != "all":
        documents_query = documents_query.filter(Document.doc_type == category)

    documents = documents_query.order_by(Document.upload_time.desc()).all()

    return render_template(
        'documents.html',
        documents=documents,
        search_query=search_query,
        category=category
    )

@app.route('/delete/<int:doc_id>', methods=['POST'])
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)

    file_path = os.path.join('static', doc.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted successfully.')
    return redirect(url_for('view_documents'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
