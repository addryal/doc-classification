from flask import Blueprint,render_template,redirect,url_for,request,flash
from project import db
from project.models import DocumentSample
import os
from werkzeug.utils import secure_filename
from project import app
from project.document.cosine_similarity import check_doc_with_class
from project.document.word_cloud import word_frequency_analysis
from project.document.forms import DocumentUploadForm
import glob


# Registering Blueprints
doc_blueprint = Blueprint('document',__name__,template_folder='templates/document')
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@doc_blueprint.route('/upload_folder',methods=['GET', 'POST'])
def upload_folder():
    form = DocumentUploadForm()
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        name = form.doc_class.data

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

         #Inserting documents into the database
        list_uploads  = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*.txt"))
        for file_path in list_uploads:
            head_tail = os.path.split(file_path)
            with open(file_path, encoding="utf8", errors="ignore") as f_input:
                document_content = f_input.read()
            doc_content_binary = bytes(document_content, 'utf-8')
            doc = DocumentSample(name, head_tail[1], doc_content_binary)
            db.session.add(doc)

        db.session.commit()
        word_frequency_analysis(app.config['UPLOAD_FOLDER'])
        file_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*.txt"))
        for f in file_list:
            os.remove(f)

        return render_template('folder.html' ,url='/static/images/word_freq.png' )

    return render_template('upload_folder.html',form=form)

@doc_blueprint.route('/delete_folder',methods=['GET', 'POST'])
def delete_folder():
    #Deleting all uploads
    file_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*.txt"))
    for f in file_list:
        os.remove(f)

    img_list = glob.glob(os.path.join("D:/flask/upload/project/static/images/","*"))
    for f in img_list:
        os.remove(f)

    full_db = DocumentSample.query.all()
    for obj_value in full_db:
        db.session.delete(obj_value)
    db.session.commit()


    return render_template('delete_confirmation.html')


@doc_blueprint.route('/view_classes',methods=['GET', 'POST'])
def view_classes():
    # Grab a list of puppies from database.
    documents = DocumentSample.query.all()
    return render_template('list.html', documents=documents)



@doc_blueprint.route('/upload_document',methods=['GET', 'POST'])
def upload_file():
    upload_folder = app.config['UPLOAD_FOLDER']
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename),encoding="utf8",errors="ignore") as f_input:
                text_first_page = [next(f_input) for x in range(10)]

            correl_df, correl_class =  check_doc_with_class(upload_folder)
            file_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*.txt"))
            for f in file_list:
                os.remove(f)

            return render_template('success.html',filename=filename,text_content=text_first_page,
                                   correl_class=correl_class)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
