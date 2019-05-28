from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
import enum
import json

app = Flask(__name__)

# for mysql replace the following with link to database:
# mysql://scott:tiger@localhost/mydatabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/maverick/Desktop/service/test.db'

db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)


model = api.model('Employee', {
    'employee_id': fields.String,
    'country': fields.String,
    'gender': fields.String(enum=['male', 'female']),
    'job_title': fields.String,
    'job_family': fields.String,
    'job_function': fields.String,
    'job_band': fields.String,
    'dept_code': fields.String,
    'dept_name': fields.String,
    'birth_date': fields.DateTime(),
    'service_date': fields.DateTime(),
    'tenure': fields.String,
    'ethnicity': fields.String,
    'diverse': fields.String(enum=['diverse', 'non_diverse']),
    'flsa_status': fields.String(enum=['exempt', 'non_exempt']),
    'employee_type': fields.String,
    'contingent': fields.String(enum=['yes', 'no']),
    'fte': fields.Integer,
    'local_salary': fields.Integer,
    'shift_and_position_allowance': fields.Integer,
    'overtime': fields.Integer,
    'on_call': fields.Integer,
    'bonus': fields.Integer,
    'indemnity_payment': fields.Integer,
    'adjustment': fields.Integer,
    'total_payroll': fields.Integer,
    'company_social_security': fields.Integer,
    'monthly_base_salary': fields.Integer,
    'annual_base_salary': fields.Integer,
    'total_rem': fields.Integer,
    'bonus_mbo': fields.Integer,
    'union_christmas_local_bonus': fields.Integer,
    'annual_total_rem': fields.Integer
})

@api.route('/')
class EmployeeRoot(Resource):
    """Employee API"""
    def get(self):
        return jsonify({"description": "Employee API"})

@api.route('/employee')
class Employee(Resource):
    """create new employee"""
    @api.marshal_with(model)
    def post(self, **kwargs):
        employee_schema = EmployeeModelSchema()
        data = request.json()
        loaded_data = employee_schema.load(data).data
        new_employee = EmployeeModel(loaded_data)
        db.session.add(new_employee)
        db.session.commit()
        return employee_schema.dumps(new_employee), 201

@api.route('/employee/list')
class EmployeeList(Resource):
    """"Returns all employees data"""
    def get(self):
        employees_schema = EmployeeModelSchema(many=True)
        all_employees = EmployeeModel.query.all()
        result = employees_schema.dumps(all_employees)
        return jsonify(result.data)


@api.route('/employee/<int:employee_id>')
class EmployeeByID(Resource):
    """"This API returns single employees details by it's ID"""
    @api.marshal_with(model)
    def get(self, employee_id):
        employee = EmployeeModel.query.get(employee_id)
        if not employee:
            return jsonify({"error": "employee not found"}), 404
        employee_schema = EmployeeModelSchema()
        result = employee_schema.dumps(employee)
        return jsonify(result.data)

@api.route('/empoloyee/update')
class EmployeeUpdate(Resource):
    """Updates single employee data"""
    @api.marshal_with(model)
    def put(self):
        data = request.get_json()
        employee_schema = EmployeeModelSchema()
        employee_data = employee_schema.load(employee_schema).data
        employee = EmployeeModel.query.get(employee_data.employee_id)
        if employee:
            for key, val in employee:
                if val is not None:
                    employee.key = val
                db.session.commit()
            result = employee_schema.dumps(employee_data)
            return jsonify(result.data)
        return {"error": "Employee Not Found"}


class GenderEnum(enum.Enum):
    male = "MALE"
    female = "FEMALE"

class DiversityEnum(enum.Enum):
    diverse = "DIVERSE"
    non_diverse = "NON-DIVERSE"

class FlsaStatusEnum(enum.Enum):
    exempt = "EXEMPT"
    non_exempt = "NON-EXEMPT"

class ContingencyEnum(enum.Enum):
    yes = "YES"
    no = "NO"

class EmployeeModel(db.Model):
    """"Model Class for Database table of employee"""
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True, unique=True)
    country = db.Column(db.String)
    gender = db.Column(db.Enum(GenderEnum)) #male or female
    job_title = db.Column(db.String)
    job_family = db.Column(db.String)
    job_function = db.Column(db.String)
    job_band = db.Column(db.String)
    dept_code = db.Column(db.String)
    dept_name = db.Column(db.String)
    birth_date = db.Column(db.DateTime)
    service_date = db.Column(db.DateTime)
    tenure = db.Column(db.String)
    ethnicity = db.Column(db.String)
    diverse = db.Column(db.Enum(DiversityEnum))
    flsa_status = db.Column(db.Enum(FlsaStatusEnum))
    employee_type = db.Column(db.String)
    contingent = db.Column(db.Enum(ContingencyEnum))
    fte = db.Column(db.Integer)
    local_salary = db.Column(db.Integer)
    shift_and_position_allowance = db.Column(db.Integer)
    overtime = db.Column(db.Integer)
    on_call = db.Column(db.Integer)
    bonus = db.Column(db.Integer)
    indemnity_payment = db.Column(db.Integer)
    adjustment = db.Column(db.Integer)
    total_payroll = db.Column(db.Integer)
    company_social_security = db.Column(db.Integer)
    total_company_payment = db.Column(db.Integer)
    monthly_base_salary = db.Column(db.Integer)
    annual_base_salary = db.Column(db.Integer)
    total_rem = db.Column(db.Integer)
    bonus_mbo = db.Column(db.Integer)
    union_christmas_local_bonus = db.Column(db.Integer)
    annual_total_rem = db.Column(db.Integer)

class EmployeeModelSchema(ma.ModelSchema):
    class Meta:
        model = EmployeeModel

if __name__ ==   '__main__':
    app.run(debug=True)