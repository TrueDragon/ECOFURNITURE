from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, IntegerField, DecimalField, validators
from wtforms.fields import EmailField, DateField
from wtforms.widgets import NumberInput

class CreateUserForm(Form):
    first_name = StringField('Employee Name', [validators.Length(min=1, max=16), validators.DataRequired()])
    last_name = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = SelectField('Membership', [validators.DataRequired()], choices=[('', 'Select'), ('M', 'Manager'), ('E', 'Employee'), ('A', 'Admin')], default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])

class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = SelectField('Membership', [validators.DataRequired()], choices=[('', 'Select'), ('P', 'Professional'), ('F', 'Fellow'), ('S', 'Seniro')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])

class CreateFurnitureForm(Form):
    furniture_type = RadioField('Furniture Type', [validators.DataRequired()], choices=[('Table/Desks', 'Table/Desks'), ('Chairs', 'Chairs'), ('Sofas', 'Sofas'), ('Bed Frames', 'Bed Frames'), ('Wardrobes', 'Wardrobes'), ('Shelves', 'Shelves'), ('Lights', 'Lights')])
    furniture_name = TextAreaField('Furniture Name', [validators.DataRequired()], render_kw={"placeholder": "Product Name"})
    furniture_quantity = IntegerField('Quantity', [validators.NumberRange(min=0, max=10000), validators.DataRequired()], widget=NumberInput())
    furniture_category = SelectField('Furniture Category', [validators.DataRequired()], choices=[('', 'Select'), ('New', 'New'), ('Upcycled', 'Upcycled'), ('Old', 'Old')])
    furniture_status = SelectField('Furniture Status', [validators.DataRequired()], choices=[('', 'Select'), ('For Sale', 'For Sale'), ('Not For Sale', 'Not For Sale')])
    furniture_price = DecimalField('Unit Price ($)',[validators.NumberRange(min=0, max=10000), validators.DataRequired()])
    furniture_remarks= TextAreaField('Remarks', [validators.Optional()], render_kw={"placeholder": "Type remarks here"})

class PaymentForm(Form):
    first_name = StringField('First name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last name', [validators.Length(min=1, max=150), validators.DataRequired()])
    card_no = IntegerField('Card number', [validators.NumberRange(min=16, max=999999999999999999999999), validators.DataRequired()], widget=NumberInput())
    exp = StringField('Expiration date', [validators.Length(min=4, max=5), validators.DataRequired()], render_kw={"placeholder": "MM/YY"})
    cvv = IntegerField('CVV', [validators.NumberRange(min=0, max=10000), validators.DataRequired()], widget=NumberInput())

class DiscountForm(Form):
    code = StringField('Discount code', [validators.Length(min=1, max=150), validators.DataRequired()])
    amount = IntegerField('Discount amount', [validators.NumberRange(min=1, max=150), validators.DataRequired()])

class ReportForm(Form):
    email = StringField('email address registered', [validators.Length(min=1, max=150), validators.DataRequired()])
    issue = RadioField('select one issue from the options below', choices=[('B', 'Bug reporting'), ('I', 'Issue with payment method'), ('A', 'Account details'), ('G', 'General feedback')], default='F')
    remarks = TextAreaField('Please share more about your issues or concerns', [validators.Optional()])

class Transportation_form(Form):
    email = StringField('email address registered', [validators.Length(min=1, max=150), validators.DataRequired()])
    Address = StringField("Address to delivery from",[validators.length(min=1, max=150), validators.DataRequired()])
    phone_No = StringField('phone number', [validators.Length(min=1, max=150), validators.DataRequired()])
    type = RadioField('select the type of furniture to deliver', choices=[('T', 'tables & desk'), ('S', 'Sofa'), ('C', 'Chairs'), ('B', 'Bed frames'), ('W', 'Wardrobes'), ('S', 'Shelving Unites')], default='F')
    date = DateField("Date of delivery", format="%Y-%m-%d")
    Info = TextAreaField("Anything for us to take note of?")

class OrderForm(Form):
    customer_id = StringField('Customer ID required', [validators.Length(min=1, max=150), validators.DataRequired()])
    item_id = StringField('Item ID required', [validators.Length(min=1, max=150), validators.DataRequired()])
    item_quantity = StringField('Item quantity required', [validators.Length(min=1, max=150), validators.DataRequired()])


