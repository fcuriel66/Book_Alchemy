from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Author object/model representing an author in the database.

    Attributes:
        id (int): Primary key for the author. Primary key integer
        and auto-incrementing.
        name (str): Name of the author.
        birth_date (str): Birth date of the author in 'YYYY-MM-DD' format.
        date_of_death (str): Date of death of the author in 'YYYY-MM-DD' format.
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String,nullable=False)
    birth_date = db.Column(db.String,nullable=True)
    date_of_death = db.Column(db.String,nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Author instance for debugging
        purposes.
        """
        return f"Author(id = {self.id}, name = {self.name})"


    def __str__(self):
        """
        Returns a 'friendly' string representation of an Author instance.
        """
        return f"{self.id}. {self.name} ({self.birth_date} - {self.date_of_death})"


class Book(db.Model):
    """
    Book model: a book in the database.

    Attributes:
          id (int): Primary key for the book.
          isbn (str): ISBN of the book, should be unique.
          title (str): Title of the book.
          publication_year (int): Year the book was published.
          author_id (int): Foreign key referencing the Author of the book.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    cover_url = db.Column(db.String, nullable=True)

    author = db.relationship('Author', backref='books', lazy=True) #########

    def __repr__(self):
        """
        Returns a representation of the Book instance.
        """
        return (f"Book(id = {self.id}, isbn = {self.isbn}, title = {self.title}, "
                f"publication_year = {self.publication_year}")

    def __str__(self):
        """
        Returns a user-friendly string representation of the Book instance.
        """
        return f"{self.id}. {self.title} ({self.publication_year})"


