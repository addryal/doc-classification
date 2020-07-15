
from project import app,db
from flask import render_template



@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()