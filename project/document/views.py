from flask import Blueprint,render_template,redirect,url_for,request,flash
from project import db
from project.models import DocumentSample
import os
from werkzeug.utils import secure_filename
from project import app
from project.document.cosine_similarity import correlation_plot,setup_base_csa,check_new_doc
from project.document.word_cloud import word_frequency_analysis
import glob


# Registering Blueprints
doc_blueprint = Blueprint('document',__name__,template_folder='templates/document')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@doc_blueprint.route('/upload_document',methods=['GET', 'POST'])
def upload_file():
    upload_folder = app.config['UPLOAD_FOLDER']
    base_csa_correlation,feature_names = setup_base_csa(upload_folder)
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


            new_file_correlation = check_new_doc(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            base_csa_correlation = round(base_csa_correlation,2)
            new_file_correlation = round(new_file_correlation,2)
            return render_template('success.html',filename=filename,text_content=text_first_page,
                                   base_csa_correlation=base_csa_correlation,new_file_correlation=new_file_correlation)

    return render_template('index.html')

@doc_blueprint.route('/upload_folder',methods=['GET', 'POST'])
def upload_folder():
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        # if user does not select file, browser also
        # submit an empty part without filename
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        word_frequency_analysis(app.config['UPLOAD_FOLDER'])
        return render_template('folder.html' ,url='/static/images/word_freq.png' )

    return render_template('upload_folder.html')

@doc_blueprint.route('/delete_folder',methods=['GET', 'POST'])
def delete_folder():
    #Deleting all uploads
    file_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*.txt"))
    for f in file_list:
        os.remove(f)

    img_list = glob.glob(os.path.join("D:/flask/upload/project/static/images/","*"))
    for f in img_list:
        os.remove(f)


    return render_template('delete_confirmation.html')


if __name__ == '__main__':
    app.run()
