from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask import request

from src.db.database import db
from src.db.models import BookModel,UserModel,IssueBookModel

from src.schema.schema import InputBookSchema,OutputBookSchema,UpdateBookSchema

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError



blp = Blueprint("books","book",description = "operation on books")

# Http methods for all the books WITH ROUTE:-/BOOKS
@blp.route("/books")
class Books(MethodView):
    # lets write get method to get all books from database.
    def get(self):
        # writing query to get all books
        try:
            books = BookModel.query.all()
            
            # return the books with status and status code
            
            return {"status":"success","data":OutputBookSchema(many=True).dump(books)},200
        except SQLAlchemyError as e:
            return abort (404,"error found while fetching the books from database.")
        
    
    # lets write post method to add book to database
    @blp.arguments(InputBookSchema)
    @blp.response(201,OutputBookSchema)
    def post(self,book_data):
        try:
            # we will be adding the new book to database.
            # lets check first book with same name is present in database or not.
            
            exiting_book = BookModel.query.filter(BookModel.book_name == book_data["book_name"] and BookModel.book_author == book_data["book_author"]).first()
            
            if exiting_book:
                return abort(404,"book with same name and same author already exist.")
                
                
            book_details = BookModel(
                book_name = book_data["book_name"],
                book_author = book_data["book_auhtor"],
                book_purchase_date = datetime.strptime(book_data["book_purchase_date"],"%Y-%m-%d"),
                book_status = "Free"
            )
            
            db.session.add(book_details)
            db.session.commit()
            db.session.refresh(book_details)
            
            return book_details,201 # returning the output.
        except:
            db.session.rollback()
        
        
# now lets write HTTP methods to get book by there id.
@blp.route("/book/<int:book_id>")
class Book(MethodView):
    # lets get book by its id.(HTTP GET Method.)
    def get(self,book_id):
        # query to get book by its id
        book = BookModel.query.filter(BookModel.id == book_id).first()
        
        if not book:
            return abort  (404,f"book with id {book_id} not found.")
        
        return {
            "status":"success",
            "data":OutputBookSchema().dump(book)
        },200
    
    
    """
    Http Method to update already present data in database by put method.
    """
    @blp.response(201,OutputBookSchema)
    @blp.arguments(UpdateBookSchema)
    def put(self,book_id,book_data):
        # we will first check if book with id is present in database or not
        try:
            book_by_id = BookModel.query.filter(BookModel.id == book_id).first()
            
            # if book by id is not found then return error.
            if not book_by_id:
                return abort(404,f"book with id {book_id} is not found.")
            
            # we need to see if book is occupied or not from issuemodel.
            book_status_data = IssueBookModel.query.filter(IssueBookModel.book_name == book_by_id.book_name).first()
            
            if not book_by_id:
                return abort(404,f"book with id {book_id} is not found.")
            
            if book_data["book_name"]:
                book_by_id.book_name = book_data["book_name"]
            
            if book_data["book_author"]:
                book_by_id.book_auhtor = book_data["book_author"]
                
            if book_data["book_purchase_date"]:
                book_by_id.book_purchase_date = datetime.strptime(book_data["book_purchase_date"],"%Y-%m-%d")
                
            if book_status_data:
                book_by_id.book_status = "Occupied"
                
            # now we have repplaced the data from old data to new data.
            
            db.session.add(book_by_id)
            db.session.commit()
            
            return book_by_id,201
        except SQLAlchemyError as e:
            db.session.rollback()
            
        
    """
    HTTP Method to delete the Book from database by its ID.
    """
    def delete(self,book_id):
        # query to get book its id
        book_by_id = BookModel.query.filter(BookModel.id == book_id).first()
        
        db.session.delete(book_by_id)
        db.session.commit()
        
        return {
            "status":"success",
            "message":f"book with id {book_id} has been deleted."
        },201
        
        
# lets write search API for getting book by its name.
@blp.route("/search")
class SearchBook(MethodView):
    # we will get  required/searched books by HTTP GET method
    def get(self):
        # lets get search_query from request(website)
        search_query = request.args.get('query')
        
        # now lets serch and get books according to search query
        search_books = BookModel.query.filter(BookModel.book_name.ilike(f"%{search_query}%")).all()
        
        return {
            "status":"success",
            "message":"here are your searched books by your name.",
            "data":OutputBookSchema(many = True).dump(search_books)
        },200
        

    
# lets get books by ther status
@blp.route("/books/status")
class BookStatus(MethodView):
    # HTTP Get query to get all occupied books or free books
    def get(self,book_status):
        # query database to get books from database
        books_by_status = BookModel.query.filter(BookModel.book_status == book_status).all()
        
        return {
            "status":"success",
            "message":"here are all books that are occupied",
            "data":OutputBookSchema(many=True).dump(books_by_status)
        },200
        
        
        
        
        
        
        
    