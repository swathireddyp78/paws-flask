from flask import request, flash, jsonify
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Student, Course, Section, Enroll
from flask_api import status
from datetime import datetime

def hash_password(password):
    return generate_password_hash(password)

def check_password(password,password_hash):
    return check_password_hash(password,password_hash)

@app.route('/studentslist_perdept',methods=['POST'])        
def studentslist_perdept():     
    try:
        return_data = []
        studentslist = Student.query.filter(Student.majorDept == request.json['dept']).all()
        if studentslist is not None:
            for application in studentslist:
                application_data = {}
                application_data['sid'] = application[0]
                application_data['fname'] = application[1]
                application_data['lname'] = application[2]
                return_data.append(application_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get applications'})

@app.route('/login',methods=['POST'])
def login():
    try:
        student = Student.query.filter_by(email = request.json['email']).first()
        if student is None or not check_password(student.password,request.json['password']):
            return jsonify({'status': status.HTTP_401_UNAUTHORIZED,'message':'Invalid Credentials'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Login successful','sid':student.sid})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to login'})

@app.route('/paws_registration',methods=['POST'])        
def paws_registration():     
    try:
        for data in request.json:
            studentslist = Student.query.filter(Student.email == data['email']).first()
            if studentslist is None:
                password = hash_password(data['fname']+data['lname'])
                student = Student(
                    email=data['email'],
                    fname=data['fname'],
                    lname=data['lname'],
                    password=password,
                    address1 = data['address1'],
                    address2 = data['address2'],
                    city = data['city'],
                    state = data['state'],
                    zip = int(data['zip']),
                    sType = data['sType'],
                    majorDept = data['majorDept'],
                    gradAssistant = 'N'
                    )
                db.session.add(student)
                db.session.commit()
        return jsonify({'status': status.HTTP_200_OK,'message':'Registered Successfully'})
    except Exception as e:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)}) 

@app.route('/get_all_courses',methods=['POST'])
def get_all_courses():
    try:
        term = request.json['term']
        course_details = db.session.query(Course,Section).filter(Course.cno == Section.course_cpcrn).filter(Section.term == term).all()
        return_data = []
        for course in course_details:
            course_data={}
            course_data['crn'] = course.Section.crn
            course_data['cprefix'] = course.Section.cprefix
            course_data['cno'] = course.Course.cno
            course_data['ctitle'] = course.Course.ctitle
            course_data['chours'] = course.Course.chours
            course_data['days'] = course.Section.days
            course_data['starttime'] = course.Section.starttime
            course_data['endtime'] = course.Section.endtime
            course_data['room'] = course.Section.room
            course_data['cap'] = course.Section.cap
            course_data['instructor'] = course.Section.instructor
            return_data.append(course_data)
        return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except:
        return jsonify({status:status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get courses'})

@app.route('/modify_enrollment',methods=['POST'])
def modify_enrollment():
    try:
        student = Student.query.filter_by(sid = request.json['sid']).first()
        term = request.json['term']
        
        if student is not None:
            Enroll.query.filter_by(sid = student.sid).filter_by(term = term).delete()
            for course in request.json['courses']:
                section = Section.query.filter_by(crn = course['crn']).first()
                enroll = Enroll(
                    sid=student.sid,
                    term=term,
                    year=2019,
                    crn=course['crn'],
                    grade = '',
                    student_sid = student.sid,
                    section_tyc = section.crn
                    )
                db.session.add(enroll)
                db.session.commit()
                
            return jsonify({'status':status.HTTP_200_OK,'message':'Enrollment saved successfully!'})
        return jsonify({'status':status.HTTP_404_NOT_FOUND,'message':'Student record not found!'})
    except:
        return jsonify({status:status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get courses'})

@app.route('/<studentID>/get_schedule')
def get_schedule(studentID):
    try:
        student = Student.query.filter_by(sid = studentID).first()
        if student is not None:
            enrollments = db.session.query(Enroll,Section).filter(Section.crn == Enroll.crn).filter(Enroll.sid == student.sid).all()
            return_data = []
            for enroll in enrollments:
                course = Course.query.filter_by(cno = enroll.Section.cno).first()
                print(course)
                enroll_data={}
                enroll_data['crn'] = enroll.Enroll.crn
                enroll_data['term'] = enroll.Enroll.term
                enroll_data['grade'] = enroll.Enroll.grade
                enroll_data['year'] = enroll.Enroll.year
                enroll_data['days'] = enroll.Section.days
                enroll_data['cprefix'] = enroll.Section.cprefix
                enroll_data['ctitle'] = course.ctitle
                enroll_data['starttime'] = enroll.Section.starttime
                enroll_data['endtime'] = enroll.Section.endtime
                enroll_data['room'] = enroll.Section.room
                enroll_data['instructor'] = enroll.Section.instructor
                return_data.append(enroll_data)
        return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except:
        return jsonify({status:status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get courses'})    


           
@app.route('/get_courses',methods=['POST'])        
def get_courses():     
    try:
        req_course = request.json['course']
        return_data = []
        courses = db.session.query(Course).filter(Course.cprefix == req_course).add_columns(Course.cprefix,Course.cno,Course.ctitle,Course.chours).all()
        if courses is not None:
            for course_temp in courses:
                course_data = {}
                course_data['cprefix'] = course_temp[1]
                course_data['cno'] = course_temp[2]
                course_data['ctitle'] = course_temp[3]
                course_data['chours'] = course_temp[4]
                return_data.append(course_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})

@app.route('/get_enroll',methods=['POST'])        
def get_enroll():     
    try:
        dept = request.json['department']
        return_data = []
        enrolls = db.session.query(Student,Enroll).filter(Student.sid == Enroll.sid).filter(Student.majorDept == dept).add_columns(Enroll.sid,Enroll.term,Enroll.year,Enroll.crn).all()
        if enrolls is not None:
            for enroll_temp in enrolls:
                enroll_data = {}
                enroll_data['sid'] = enroll_temp[2]
                enroll_data['term'] = enroll_temp[3]
                enroll_data['year'] = enroll_temp[4]
                enroll_data['crn'] = enroll_temp[5]
                return_data.append(enroll_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})

@app.route('/get_students',methods=['POST'])        
def get_students():     
    try:
        dept = request.json['majorDept']
        return_data = []
        students = db.session.query(Student).filter(Student.majorDept == dept).add_columns(Student.sid,Student.email,Student.fname,Student.lname).all()
        if students is not None:
            for student_temp in students:
                student_data = {}
                student_data['sid'] = student_temp[1]
                student_data['email'] = student_temp[2]
                student_data['fname'] = student_temp[3]
                student_data['lname'] = student_temp[4]
                return_data.append(student_data)
                print(return_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})

@app.route('/update_grade',methods=['PUT'])
def update_grade():
    try:
        enroll = Enroll.query.filter_by(sid = request.json['sid'],term = request.json['term'],year = request.json['year'], crn = request.json['crn']).first()
        if enroll is not None:
            enroll.grade = request.json['grade']
            
            db.session.add(enroll)
            db.session.commit()

            return jsonify({'status': status.HTTP_201_CREATED,'message':'Grade updated successfully'})
        else:
            return jsonify({'status':status.HTTP_200_OK,'message':'Application not found'})
    except Exception as e:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to change status'})