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


class RegisterPatientDetails(Resource):
    def post(self):
        data=request.get_json()
        print(data)
        Hospital.register_patient(name=data['name'],phone_number=data['phone_number'],age=data['age'],bed_type=data['bed_type'],address=data['address'],state=data['state'],city=data['city'],patient_status=data['patient_status'])
        return "Sucessfully added the new patient details"


class EditPatient(Resource):
    def put(self, id):
        data = request.get_json()
        print(data)
        Hospital.edit_patient(id,data['age'],data['bed_type'],data['address'],data['state'],data['city'],data['patient_status'])
        if data:
            return "sucessfully updated the movie id {0}".format(id)
        else:
            return jsonify({'message': 'ID not found', 'status': HTTPStatus.NOT_FOUND})

class DeletePatient(Resource):
    def delete(self, id):
        delete_patient = Hospital.delete_patient(id)
        print(delete_patient)
        if delete_patient:
            return "sucessfully deleted the movie id {0}".format(id)
        else:
            return jsonify({'message': 'ID not found', 'status': HTTPStatus.NOT_FOUND})


#class AllPatientDetails(Resource):
@app.route('/getpatient')
def get():
    data = Hospital.getAllPatients()
    print(data)
    # patientlst = []
    # for patientdata in data:
    #     dictpatient = {'id': patientdata.id,'name':patientdata.name, 'phone_number': patientdata.phone_number, 'age': patientdata.age, 'bed_type': patientdata.bed_type,'address':patientdata.address,'state':patientdata.state,'city':patientdata.city,'patient_status':patientdata.patient_status}
    #     patientlst.append(dictpatient)
    # #return patientlst
    return render_template("AllPatients.html",data=data)

class GetPatientByID(Resource):
    def get(self, id):
        dicdata = {}
        data = Hospital.getpatientid(id)
        if data:
            #dicdata['id'] = data.id
            dicdata['phone_number'] = data.phone_number
            dicdata['age'] = data.age
            dicdata['bed_type'] = data.bed_type
            dicdata['address'] = data.address
            dicdata['state'] = data.state
            dicdata['city'] = data.city
            dicdata['patient_status'] = data.patient_status

            return jsonify((dicdata), {'status': HTTPStatus.OK})
        else:
            return jsonify({'message': 'ID not found', 'status': HTTPStatus.NOT_FOUND})


class GetAllActivePatients(Resource):
    def get(self, status):
        activepatients = Hospital.getAllActivePatients(status)
        print(activepatients)
        activepatientlst=[]
        for eachpatient in activepatients:
            dictacitvepatient = {'id': eachpatient.id, 'phone_number': eachpatient.phone_number, 'age': eachpatient.age,
                           'bed_type': eachpatient.bed_type, 'address': eachpatient.address, 'state': eachpatient.state,
                           'city': eachpatient.city, 'patient_status': eachpatient.patient_status}
            activepatientlst.append(dictacitvepatient)
        return activepatientlst


# api.add_resource(RegisterPatientDetails,"/Register_patient")
# api.add_resource(EditPatient,"/edit_patient/<int:id>")
# api.add_resource(DeletePatient,"/delete_patient/<int:id>")
# api.add_resource(AllPatientDetails,"/getAllPatients")
# api.add_resource(GetPatientByID,"/getpatient/<int:id>")
# api.add_resource(GetAllActivePatients,"/getAllActivePatients/<string:status>")#status=Active


if __name__=="__main__":
    app.run()



#step 1
# install required packages from Terminal

#step 2
#from Python Console
#from hospital import db
#db.create_all()

#step 3
# go to postman using post    http://127.0.0.1:5000/Register_patient
#input body
# {
#     "name" :"prasham",
#     "phone_number" :9790815622,
#     "age" :34,
#     "bed_type" : "General Ward",
#     "address" : "BTM Layout",
#     "state" : "Karnataka",
#     "city" : "Banagalore",
#     "patient_status" : "Active"
# }

#step 4
# go to postman using put    http://127.0.0.1:5000/edit_patient/2
# {
#     "age" :28,
#     "bed_type" : "Single",
#     "address" : "BTM Layout",
#     "state" : "TamilNadu",
#     "city" : "Chennai",
#     "patient_status" : "discharged"
# }

#step 5
#go to postman using delete http://127.0.0.1:5000/delete_patient/2

#step 6
#go to postman using get http://127.0.0.1:5000/getAllPatients

#step 7
#go to postman using get http://127.0.0.1:5000/getpatient/2
#go to postman using get http://127.0.0.1:5000/getpatient/100
#output
# {
#     "message": "ID not found",
#     "status": 404
# }

#step 8
#go to postman using get http://127.0.0.1:5000/getAllActivePatients/Active