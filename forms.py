from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FileField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
email_list = [
    'reigate@moderndemocracy.com',
    'rochford@moderndemocracy.com',
    'rhmaidendheadwindsor@moderndemocracy.cc',
    'southoxfordshire@moderndemocracy.com',
    'threerivers@moderndemocracy.com',
    'brentwood@moderndemocracy.com',
    'colchester@moderndemocracy.com',
    'barking@moderndemocracy.com',
    'newham@moderndemocracy.com',
    'rother@moderndemocracy.com',
    'thurrock@moderndemocracy.com',
    'bath@moderndemocracy.com',
    'chorley@moderndemocracy.com',
    'elmbridge@moderndemocracy.com',
    'southribble@moderndemocracy.com',
    'bracknellforest@moderndemocracy.com',
    'eastbourne@moderndemocracy.com',
    'lewes@moderndemocracy.com',
    'spelthorne@moderndemocracy.com',
    'watford@moderndemocracy.com',
    'arun@moderndemocracy.com',
    'crawley@moderndemocracy.com',
    'gosport@moderndemocracy.com',
    'harrow@moderndemocracy.com',
    'horsham@moderndemocracy.com',
    'hounslow@moderndemocracy.com',
    'midsussex@moderndemocracy.com',
    'wealden@moderndemocracy.com',
    'blaenaugwent@moderndemocracy.com',
    'bridgend@moderndemocracy.com',
    'caerphilly@moderndemocracy.com',
    'cardiff@moderndemocracy.com',
    'carmarthenshire@moderndemocracy.com',
    'merthyr@moderndemocracy.com',
    'monmouthshire@moderndemocracy.com',
    'neath@moderndemocracy.com',
    'swansea@moderndemocracy.com',
    'torfaen@moderndemocracy.com',
    'valeofglamorgan@moderndemocracy.com',
    'bolsover@moderndemocracy.com',
    'peterbourough@moderndemocracy.com',
    'tamworth@moderndemocracy.com',
    'westlancashire@moderndemocracy.com',
    'fenland@moderndemocracy.com',
    'lichfield@moderndemocracy.com'
    "mehdi",
    "test@test,.com",
]



# Create a form to register new users
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a form for scanning existing items asset ID and assign cover to them
class ScanForm(FlaskForm):
    asset_id = StringField("Scan Asset ID", validators=[DataRequired()])
    cover_tag = StringField("Scan Cover TAG", validators=[DataRequired()])
    submit = SubmitField("Save Scan")


# Create a form that assigns iPads to locations
class AssignForm(FlaskForm):
    # location = StringField("Enter Location Email", validators=[DataRequired()])
    # cover_tag = IntegerField("Scan cover Tag ", validators=[DataRequired()])
    # end_number = IntegerField("Enter last iPad Cover tag in the bunch ", validators=[DataRequired()])
    locations = SelectField("Select Location", choices=email_list, validators=[DataRequired()])
    submit = SubmitField("Submit")


# Creates a form to upload the CSV file to record UDID according to Serial Number
class RenameUpdateForm(FlaskForm):
    file = FileField(validators=[FileRequired(), FileAllowed(["csv"], "CSV file only")])
    submit = SubmitField("Upload")


# Creates a form to manually add an ipad to list of devices.
class AddForm(FlaskForm):
    asset_id = StringField("Scan Device Asset ID or enter Manually", validators=[DataRequired()])
    serial_number = StringField("Enter Serial Number", validators=[DataRequired()])
    owner = StringField("Enter Owner of the tablet")
    submit = SubmitField("Add")


# Define a search form using Flask-WTF
class SearchForm(FlaskForm):
    search_query = StringField('Search Query')
    submit = SubmitField('Search')


class ShowDB(FlaskForm):
    submit = SubmitField("Show DB")
    form_type = HiddenField(default="db")


class ExportForm(FlaskForm):
    submit = SubmitField("Export To CSV")
    form_type = HiddenField(default="export")


class ReturnedForm(FlaskForm):
    cover_tag = StringField("Scan Cover Tags",validators=[DataRequired()])
    submit = SubmitField("Save")


class EditForm(FlaskForm):
    asset_id = StringField("Scan Asset ID", validators=[DataRequired()])
    cover_tag = StringField("Scan Cover TAG")
    serial_number = StringField("Serial Number", validators=[DataRequired()])
    location = StringField("Location")
    owner = StringField("Owner")
    submit = SubmitField("Save Edit")


class UploadCSVForm(FlaskForm):
    file = FileField("Upload CSV File", validators=[DataRequired()])
    submit = SubmitField("Upload")

