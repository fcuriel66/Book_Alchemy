from idlelib.configdialog import is_int
from datetime import datetime
from flask import Flask, render_template, request
import os
import requests
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

def fetch_book_api(isbn):
   """
   Fetches book details, including the cover image URL and description, using the Google Books API.
   Args:
       isbn (str): The ISBN of the book to fetch details for.
   Returns:
       string: Containing cover_url (str or None) which is the
        URL of the book's cover image if available, otherwise None.
   """
   if not isbn or not isbn.isdigit() or len(isbn) not in (10, 13):
      print(f"Invalid ISBN provided: {isbn}")
      return None

   api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

   try:
      response = requests.get(api_url, timeout=25)
      response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
   except requests.exceptions.Timeout:
      print(f"Request timed out while fetching details for ISBN: {isbn}")
      return None
   except requests.exceptions.ConnectionError:
      print(f"Connection error while fetching details for ISBN: {isbn}")
      return None
   except requests.exceptions.HTTPError as e:
      print(f"HTTP error occurred: {e}")
      return None
   except requests.exceptions.RequestException as e:
      print(f"An error occurred while fetching details for ISBN: {isbn}. Error: {e}")
      return None

   try:
      data = response.json()
   except ValueError:
      print(f"Error in JSON response for ISBN: {isbn}")
      return None

   if "items" not in data or not data["items"]:
      print(f"No book found for ISBN: {isbn}")
      return None

   try:
      volume_info = data["items"][0]["volumeInfo"]
      cover_url = volume_info.get("imageLinks", {}).get("thumbnail", None)
      #description = volume_info.get("description", None)
      return cover_url, #description
   except KeyError:
      print(f"Unexpected data structure in API response for ISBN: {isbn}")
      return None


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


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
   """
   Handles the addition of a new book. Both GET and POST requests accepted.
       - GET: Renders the form for adding a new book.
       - POST: Processes the form submission, validates the input, and adds the book to the database.
   """
   if request.method == "POST":
      isbn = request.form.get('isbn', '').strip()
      title = request.form.get('title', '').strip()
      publication_year = request.form.get('publication_year', '').strip()
      author_id = request.form.get('author_id')
      cover_url = request.form.get('cover_url', '').strip()

      # Title validation: it must not be empty and should contain letters
      if not title or not any(char.isalpha() for char in title):
         warning_message = "Invalid book title. Please enter a valid book title."
         return render_template("add_book.html",
                                authors=Author.query.all(),
                                warning_message=warning_message)

      # ISBN validation: It should contain only digits and be 10 or 13 digits long
      if not isbn.isdigit() or len(isbn) not in [10, 13]:
         warning_message = "Invalid ISBN. It should be 10 or 13 digits."
         return render_template("add_book.html",
                                authors=Author.query.all(),
                                warning_message=warning_message)

      # Validate publication year: It should be a valid year
      current_year = datetime.now().year
      if publication_year:
         if not publication_year.isdigit() or not (1455 <= int(publication_year) <= current_year):
            warning_message = (f"Invalid publication year. Must be between 1455"
                               f" (first published book) and {current_year}.")
            return render_template("add_book.html",
                                   authors=Author.query.all(),
                                   warning_message=warning_message)

      # Check if the book already exists
      existing_book = Book.query.filter_by(isbn=isbn).first()
      if existing_book:
         warning_message = "Book already exists in the library collection"
         return render_template("add_book.html",
                                authors=Author.query.all(),
                                warning_message=warning_message)

      book = Book(
         author_id=author_id,
         isbn=isbn,
         title=title,
         publication_year=int(publication_year) if publication_year else None,
         cover_url=cover_url
      )

      try:
         db.session.add(book)
         db.session.commit()
         success_message = "Book added successfully!"
         return render_template("add_book.html",
                                authors=Author.query.all(),
                                success_message=success_message)
      except SQLAlchemyError:
         db.session.rollback()
         warning_message = f"Error adding the book!"
         return render_template("add_book.html",
                                authors=Author.query.all(),
                                warning_message=warning_message)

   else:
      return render_template("add_book.html", authors=Author.query.all())


@app.route('/', methods=['GET'])
def home_page():
   """
       Displays a homepage with the books in the database listed.
       The books can be sorted by author or title. A search function
        can filter books by title.
       Returns:
           - Rendered homepage with books, sorted and/or filtered based on the user's input.
       """
   sort = request.args.get('sort', 'author')
   search = request.args.get('search') or ""
   message = request.args.get('message')

   if search:
      books = db.session.query(Book, Author).join(Author) \
         .filter(Book.title.like(f"%{search}%")) \
         .order_by(Book.title).all()
      if not books:
         return render_template("home.html", books=[], search=search,
                                message="No books in database matched your search.")
   else:
      if sort == 'author':
         books = db.session.query(Book, Author).join(Author).order_by(Author.name).all()
      elif sort == 'title':
         books = db.session.query(Book, Author).join(Author).order_by(Book.title).all()
      else:
         books = db.session.query(Book, Author).join(Author).order_by(Author.name).all()

   books_with_cover = []
   for book, author in books:
      #cover_url, _ = fetch_book_api(book.isbn)
      cover_url = fetch_book_api(book.isbn)
      books_with_cover.append((book, author, cover_url))

   return render_template("home.html", books=books_with_cover,
                          sort=sort, search=search, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)