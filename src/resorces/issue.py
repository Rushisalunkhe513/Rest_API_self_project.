"""
Importing Model for data addition in table.
"""
from src.db.models import IssueBookModel,UserModel,BookModel

"""
Importing db for databse operations like commit,add,delete,roolback and etc.
"""
from src.db.database import db

"""
Importing Schema for data validation for defined Model.
"""
from src.schema.schema import InputIssueSchema,OutputIssueSchema,UpdateIssueSchema

"""
flask_smoresst Blueprint is used to divide large flask application into smaller one by divivding its parts into smaller one
and then combining it togetger to make complete application at app.py/main.py
by doing this we can manage large app easiily , also give routing for each part of application in one place.
"""
from flask_smorest import Blueprint,abort # abort used for quiting method when something is not found.

"""
we are using MethodView here because we will be defining all HTTP method in single class, rather than 
importing single method for each class.it will help us to group all Http methods in single class. 
"""
from flask.views import MethodView 

"""
One of sqlalchemy error type for defining error.
"""
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime,timedelta



# IssueData is name of Blueprint
# Description is documentation for this blueprint, what it does.
blp = Blueprint("IssueData","issues",description = "Operation on Book Issues.")


# lets write class and HTTP methods.
@blp.route("/book_issues") # this @ blp.route is used to give route(address) to access this methods.
class BookIssues(MethodView): # We are defining class with Methodview to define methods lke get,post,put and delete insidee this class
    # @blp.response(200,OutputIssueSchema)
    # this blp.response is decorator which gives us output in status code and serialized data(from data objects to json file) in form OutputIssueSchema
    # this should be used when we are not using {"status":"success","data":OutputIssueSchema(many = True).dump(issues)},200
    def get(self):
        """
        lets get all data from IssueModel table
        """
        issues = IssueBookModel.query.all()    # this is the query whhich will give us all data from table.
        
        # here we are givivng status as success and with status code is 200 for successs and data in schema with many = True says multuple issues will be given.
        return {"status":"success","data":OutputIssueSchema(many = True).dump(issues)},200
    
    
    """
    return {"status":"success","data":OutputIssueSchema(many = True).dump(issues)},200
    we are not using this method for post request because post request always gives us status and status_code to us along with data.
    """
    @blp.response(201,OutputIssueSchema) # output response for tgis post request should be like OutputIssueSchema
    @blp.arguments(InputIssueSchema) # this @blp.arguments is used to get exact type of value and data from user.
    def post(self,issue_data): # issue_data is actually user_give data in form of request.
        """
        lets add new issue to the database, by taking arguments specified in InputIssueSchema
        """
        try:
            # lets check for user_id in Userdata to make sure user exixt
            user = UserModel.query.filter(UserModel.id == issue_data["user_id"]).first() # get first user that matches with id.
            
            # sim,make sure book exitenece by book_id in BookData.
            book = BookModel.query.filter(BookModel.id == issue_data["book_id"]).first()
            
            if not user and not book:
                return abort(409,f"user and book not found")
            
            
            if issue_data["book_issued_frequency"] == "Weekly":
                date_issued_till = datetime.now() + timedelta(days= 7)
            elif issue_data["book_issued_frequency"] == "Monthly":
                date_issued_till = datetime.now() + timedelta(days=30)
            else:
                date_issued_till = datetime.now() + timedelta(days= 90)
            
            issue_details = IssueBookModel(
                book_name = issue_data["book_name"],
                user_name = issue_data["user_name"],
                user_id = issue_data["user_id"],
                book_id = issue_data["book_id"],
                book_issued_frequency = issue_data["book_issued_frequency"],
                issue_from = datetime.now(),
                issue_date_till = date_issued_till
            )
            
            # now lets add data to the table by,
            db.session.add(issue_details)
            # save added data to the table by commit.
            db.session.commit()
            # now lets refresh data
            db.session.refresh(issue_details)
            
            # returning data as per Output schema type and status code as 201.
            return issue_details,201 
        
        except SQLAlchemyError as e:
            # rollback will prevent the data added to the table or database to removed when error is found.
            db.session.rollback()
            
        
        
# lets get,put and delete the data by issue id.
@blp.route("/book_issue/<int:issue_id>") # this is route should be used to access this methods inside this class.
class BookIssuesByID(MethodView):
    """
    get method first
    """ 
    def get(self,issue_id):
        
        # lets get issue_data by id
        issue_data_by_id = IssueBookModel.query.get_or_404(issue_id) # this method will look for object if not found will return 404.
            
        return {"status":"success","data":OutputIssueSchema(many=False).dump(issue_data_by_id)},200
        
    """
    Put method to update the existing data
    """
    # add response and arguments to post and put methods.
    @blp.response(201,OutputIssueSchema)
    @blp.arguments(InputIssueSchema)
    def put(issue_id,issue_details):
        
        try:
            # lets get first issue_data by id
            issue_data = IssueBookModel.query.get(issue_id) # this method will return if object exixt by primary key(automatically) else returns None.
            
            if not issue_data:
                return abort (404,f"issue data with id {issue_id} is not found")
                
            if issue_details["book_issued_frequency"] == "Weekly":
                book_issued_till = datetime.now() + timedelta(days=7)
            elif issue_details["book_issued_frequency"] == "Monthly":
                book_issued_till = datetime.now() + timedelta(days=30)
            else:
                book_issued_till = datetime.now() + timedelta(days=90)
            
            if issue_data:
                issue_data.book_name = issue_details["book_name"]
                issue_data.user_name = issue_details["user_name"]
                issue_data.user_id = issue_details["user_id"]
                issue_data.book_id = issue_details["book_id"]
                issue_data.issue_date = datetime.now()
                issue_data.issue_date_till = book_issued_till
                issue_data.book_issued_frequency = issue_details["book_issued_frequency"]
            
            # now lets add data to the table 
            db.session.add(issue_data)
            db.session.commit()
            db.session.refresh(issue_data)
            
            return issue_data,201
        except SQLAlchemyError as e:
            db.session.rollback()
            
    """
    Http delete Method by id
    """
    def delete(self,issue_id):
        
        # lets get issue_data by id and delete
        issue_data_by_id = IssueBookModel.query.get(issue_id)
        
        if not issue_data_by_id:
            return abort (404,f"issued data by id {issue_id} not found.")
        
        db.session.delete(issue_data_by_id)
        db.session.commit()
        
        return {
            "status":"success",
            "message":f"the issue data by id {issue_id} has been deleted"
            },200
        
#     """
#     get HTTP method for getting books issued by user
#     """

@blp.route("/issued/<int:user_id>")
class UserIssuedBooks(MethodView):
    # get all user issued books by user_id
    def get(self,user_id):
        
        # lets get all user_issued books but first lets get user data
        user_issued_books = IssueBookModel.query.filter(IssueBookModel.user_id == user_id).all()
        
        return {
            "status":"success",
            "data":OutputIssueSchema(many = True).dump(user_issued_books)
        },200
        

            
        
        