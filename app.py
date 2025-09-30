from idlelib.configdialog import is_int

from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
#from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

# Create the database tables. Ran once and then commented
# with app.app_context():
#    db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
   """
   Handles the addition of a new author. Both GET and POST requests accepted.
       - GET: Renders the form for adding a new author.
       - POST: Processes the form submission, validates the input, and adds the author to the database.
   """
   if request.method == "POST":
      # Gets parameters from the form
      name = request.form.get('name', '').strip()
      birth_date = request.form.get('birth_date', '').strip()
      date_of_death = request.form.get('date_of_death', '').strip()

      # Validates the name field: only non-integer string accepted
      if not name or is_int(name):
         warning_message = "Invalid name. Please fill the form correctly."
         return render_template("add_author.html", warning_message=warning_message)

      # Checks if the author already in db
      existing_author = Author.query.filter_by(name=name, birth_date=birth_date).first()
      print(existing_author)
      if existing_author:
         warning_message = "Author already in database... Please choose a different name."
         return render_template("add_author.html", warning_message=warning_message)

      # Author object creation
      author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

      try:
         db.session.add(author)
         db.session.commit()
         success_message = "Author added successfully!"
         return render_template("add_author.html", success_message=success_message)
      except SQLAlchemyError:
         db.session.rollback()
         warning_message = f"Error adding author to the database!"
         return render_template("add_author.html", warning_message=warning_message)

   # GET method handling
   else:
      return render_template('add_author.html',authors=Author.query.all())




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)