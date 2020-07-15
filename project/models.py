from project import db

class DocumentSample(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    doc_class = db.Column(db.String(80), nullable=False)
    doc_name = db.Column(db.String(80), nullable=False)
    doc_content = db.Column(db.LargeBinary)

    def __init__(self,doc_class,doc_name,doc_content):
        self.doc_class = doc_class
        self.doc_name = doc_name
        self.doc_content = doc_content

    def __repr__(self):
        return f"The document type is {self.doc_class} and the name of the doc is {self.doc_name}"
