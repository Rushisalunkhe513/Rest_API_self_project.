from flask.views import MethodView
from flask_smorest import Blueprint,abort

from src.db.database import db
from src.db.models import BookModel,UserModel,IssueBookModel

from src.schema.schema import InputUserSchema,OutputUserSchema,UpdateUserSchema

from datetime import date
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("Users","user",description = "Operation on users")

# lets get user all users by users route
@blp.route("/users")
class Users(MethodView):
    # lets get all users from dataabse
    def get(self):
        # lets use query to get all users from database
        users = UserModel.query.all()
        
        return {
            "status":"success",
            "message":"here are all users",
            "data":OutputUserSchema(many=True).dump(users)
        },200
        
    
    #HTTP Method to add new user to the database
    @blp.arguments(InputUserSchema) # arguments from input user schema.
    @blp.response(201,OutputUserSchema) # output should be like this.
    def post(self,user_data):
        try:
            # add user to database
            user = UserModel(
                user_name = user_data["user_name"],
                user_mobile_number = user_data["user_mobile_number"],
                user_address = user_data["user_address"]
            ) 
            
            # now lets add user to database.
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            
            return user,201
        except:
            db.session.rollback()
         
         
# now lets add route to get,put and delete user
@blp.route("/user/<int:user_id>")
class User(MethodView):
    # get user by id
    def get(self,user_id):
        # query to get user by its id.
        user = UserModel.query.get_or_404(user_id)
        
        # lets return user by id to clien(frontend)
        return {
            "status":"success",
            "message":f"user with id {user_id}",
            "data":OutputUserSchema(many=True).dump(user)
        },200
        
    #lets update user data by put HTTP Method
    @blp.arguments(UpdateUserSchema)
    @blp.response(201,OutputUserSchema)
    def post(self,user_id,user_data):
        
        # lets check first if user exixt or not.
        user = UserModel.query.filter(UserModel.id == user_id).first()
        
        # if usr with user_id not in database return error
        if not user:
            return abort (404,"user not found")
        
        if user_data:
            user.user_name = user_data["user_name"]
            user.user_address = user_data["user_address"]
            user.user_mobile_number = user_data["user_mobile_number"]
        
        # now we have replaced old data with new one
        # now add newly added data to database.
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        return user,201
    
    
    # HTTP method to delete user by id.
    def delete(self,user_id):
        # query to get user by id from database
        
        user = UserModel.query.get_or_404(user_id)
        
        if not user:
            return abort (404,"user not found.")
        
        db.session.delete(user)
        db.session.commit()
        
        return {
            "status":"success",
            "message":f"user with id {user_id} has been deleted"
        },201