from marshmallow import Schema,fields,validate # validate will insure that data given by user should matches specific data.
# validate uses validate.oneOf method to see if user given values is matches to specific data defined in server/backend. 
"""
Marshamallow is library for flask and django framework used for data validation and serializaing and deserailizing data into python datatypes to objects.
"""

# dump_only = dump_only is used to show data in output but that data shoudnt be present in input.
# load only = load only data is used for loading or adding the data to database but should not be used in output.
# required = True(means that this values should must be present during data additon or during in inputing data)

# schema

# schema for books
# Input from user
class InputBookSchema(Schema):
    # we will not be needing Id we will be auto including it in input so use dump_only to it
    id =fields.Int(dump_only = True)
    book_name = fields.Str(required = True)
    book_purchase_date = fields.Str(required = True)
    book_author = fields.Str(required = True)
    book_status = fields.Str(dump_only = True,validate=validate.OneOf(
        [
            "Free",
            "Occupied"
        ]
    ))
    
# schema for updating book data
class UpdateBookSchema(Schema):
    book_name = fields.Str()
    book_purchase_date = fields.Str()
    book_author = fields.Str()
    book_status = fields.Str(validate=validate.OneOf(
        [
            "Free",
            "Occupied"
        ]
    ))
    
# Book Output Schema
class OutputBookSchema(Schema):
    # show in swagger docs or to client side.
    id = fields.Int()
    book_name = fields.Str()
    book_purchase_date = fields.Str()
    book_author = fields.Str()
    book_status = fields.Str()
    


# lets write schema for the user.
# input schema
class InputUserSchema(Schema):
    # lets take id but for dump_only
    id = fields.Int(dump_only = True)
    user_name = fields.Str(required = True)
    user_mobile_number = fields.Str(required = True)
    user_address = fields.Str(required = True)
    
# schema for updating user data
class UpdateUserSchema(Schema):
    user_name = fields.Str()
    user_mobile_number = fields.Str()
    user_address = fields.Str() 

# output user schema
class OutputUserSchema(Schema):
    # lets get user id
    id = fields.Int()
    user_name = fields.Str()
    user_mobile_number = fields.Str()
    user_address = fields.Str()
    


# schema for issue
# inout schema
class InputIssueSchema(Schema):
    # id should be dump only
    id = fields.Int(dump_onlt = True)
    book_name = fields.Str(required = True)
    user_name = fields.Str(required = True)
    book_id = fields.Int(required = True)
    user_id = fields.Int(required = True)
    issue_date = fields.DateTime(dump_only = True)
    issue_date_till = fields.DateTime(dump_only = True)
    book_issued_frequency = fields.Str(required = True,
                                       validate = validate.OneOf(
                                           [
                                               "Weekly",
                                               "Monthly",
                                               "Quarterly"
                                           ]
                                       )
        )
    
# issue schema for put(update) method.
class UpdateIssueSchema(Schema):
    book_name = fields.Str()
    user_name = fields.Str()
    book_id = fields.Int()
    user_id = fields.Int()
    issue_date = fields.DateTime()
    issue_date_till = fields.DateTime()
    book_issued_frequency = fields.Str(validate = validate.OneOf(
        [
            "Weekly",
            "Monthly",
            "Quarterly"
        ]
    ))

# output schema
class OutputIssueSchema(Schema):
    # need all data
    id = fields.Int()
    book_name = fields.Str()
    user_name = fields.Str()
    user_id = fields.Int()
    book_id = fields.Int()
    issue_date = fields.DateTime()
    issue_date_till = fields.DateTime()
    book_issued_frequency = fields.Str()    
    
    