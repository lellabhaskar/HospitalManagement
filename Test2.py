from flask import Flask,request,jsonify,render_template
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy

from http import HTTPStatus
import pymysql
app= Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:welcome$1234@localhost/hospitaldatabase"
db=SQLAlchemy(app)
api=Api(app)



class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer(), nullable=False)
    #phone_number = db.Column(db.BigInteger(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    patient_status = db.Column(db.String(200), nullable=False)

    @staticmethod
    def register_patient(name,phone_number,age,bed_type,address,state,city,patient_status):
        new_patient_details=Hospital(name=name,phone_number=phone_number,age=age,bed_type=bed_type,address=address,state=state,city=city,patient_status=patient_status)
        db.session.add(new_patient_details)
        db.session.commit()

    @staticmethod
    def edit_patient(id,age,bed_type,address,state,city,patient_status):
        updatepatient = Hospital.query.filter_by(id=id).first()
        print(updatepatient)
        print(type(updatepatient))

        updatepatient.age=age
        updatepatient.bed_type = bed_type
        updatepatient.address = address
        updatepatient.state = state
        updatepatient.city = city
        updatepatient.patient_status = patient_status

        db.session.commit()

    @staticmethod
    def delete_patient(id):
        delpatient = Hospital.query.filter_by(id=id).delete()
        db.session.commit()
        return delpatient

    @staticmethod
    def getAllPatients():
        data = Hospital.query.all()
        return data

    @staticmethod
    def getpatientid(id):
        data = Hospital.query.filter_by(id=id).first()
        return data

    @staticmethod
    def getAllActivePatients(status):
        data = Hospital.query.filter_by(patient_status=status).all()
        return data


@app.route("/")
def HomePage():
    return render_template("Home.html")


@app.route('/getAllPatients')
def getAllPatientDetials():
    data = Hospital.getAllPatients()
    #print(data)
    return render_template("AllPatients.html",data=data)


@app.route('/GetPatientByIDhtml')
def RedirectionPatientByIDPage():
    return render_template("GetPatientByID.html")


@app.route('/getpatientByID',methods=['POST'])
def getPatientDetailsByID():
    id = request.form["id"]
    print(id)
    data = Hospital.getpatientid(id)
    # print(data)
    # print(data.age)
    # print(data.name)
    return render_template("EachPatientByID.html",patientdetails=data)


@app.route('/EditPatientByIDhtml')
def RedirectionEditPatientByIDPage():
    return render_template("EditPatientByID.html")


@app.route('/editpatientByID', methods=['POST'])
def editPatientDetailsByID():
    id = request.form["id"]
    age = request.form["age"]
    bed_type = request.form["bed_type"]
    address = request.form["address"]
    state   = request.form["state"]
    city = request.form["city"]
    patient_status = request.form["patient_status"]
    print(id,age,bed_type,address,state,city,patient_status)
    Hospital.edit_patient(id,age,bed_type,address,state,city,patient_status)
    return "sucessfully updated the patient details of id {0}".format(id)


if __name__=="__main__":
    app.run()

