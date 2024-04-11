from src.db.database import db
from datetime import datetime


# lets declare models
# db.model is for declaring that this is table.
# we are not importing datatypes from SQLALchemy because db is SQLALchemy instance and it contains all datatypes required for this model.

    
# table for book
class BookModel(db.Model): # db.Model declares that it is SQLALchemy Model class
    __tablename__ ="books" # name of table is books
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # id is primary_key declared by primary_key constraint,autoincremt means that it will increment automatically 
    book_name = db.Column(db.String,nullable = False) # book name column in Books model with String type data with should not be empty
    book_purchase_date = db.Column(db.DateTime,nullable = True,default = datetime.now()) # book purchase date by library column in Datetime type column and nullable True with default value is datetuime of today.
    book_author = db.Column(db.String,nullable = False) # author of book with String type data and it should not be null.
    book_status = db.Column(db.String,default = 'Free')
    
    issued_book = db.relationship(
        "IssueBookModel",
        back_populates = "book"
    )
    
# table for user with user details.
class UserModel(db.Model):
    __tablename__ ="users"
    
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    user_name = db.Column(db.String,nullable = False)
    user_mobile_number = db.Column(db.String,nullable = False)
    user_address = db.Column(db.String,nullable = False)
    
    issued = db.relationship(
        "IssueBookModel",
        back_populates = "user"
    )
    
# issue table for book
class IssueBookModel(db.Model):
    __tablename__ ="issue_book"
    
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    book_id = db.Column(db.Integer,db.ForeignKey("books.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    book_name = db.Column(db.String,nullable = False)
    user_name = db.Column(db.String,nullable = False)
    book_issued_frequency = db.Column(db.String,nullable = False)
    issue_date = db.Column(db.DateTime,nullable = False)
    issue_date_till = db.Column(db.DateTime,nullable = False)
    
    
    user = db.relationship(
        "UserModel",
        back_populates = "issued"
    )
    
    book = db.relationship(
        "BookModel",
        back_populates = "issued_book"
    )
    