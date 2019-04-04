from app import db
from datetime import datetime

class Student(db.Model):
    sid = db.Column(db.Integer,db.Sequence('student_sid_seq'),db.CheckConstraint('sid > 999 and sid<10000'),unique=True)
    email = db.Column(db.String(40),primary_key=True)
    password = db.Column(db.String(128),nullable=False)
    fname = db.Column(db.String(20),nullable=False)
    lname = db.Column(db.String(20),nullable=False)
    address1 = db.Column(db.String(40))
    address2 = db.Column(db.String(40))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    zip = db.Column(db.Integer)
    sType = db.Column(db.String(5),db.CheckConstraint('sType in (MS,phD,UGRAD)'))
    majorDept = db.Column(db.String(4),db.CheckConstraint('majorDept in (CSC,MATH,POLS,HIST)'))
    gradAssistant = db.Column(db.String(1),db.CheckConstraint('gradAssistant in (Y,N)'))
    student = db.relationship('Enroll',backref='student',lazy='dynamic')

    def __repr__(self):
        return '<Student {}>'.format(self.email)

class Course(db.Model):
    cprefix = db.Column(db.String(40))
    cno = db.Column(db.Integer,primary_key=True)
    ctitle = db.Column(db.String(50))
    chours = db.Column(db.Integer)
    courses = db.relationship('Section',backref='course',lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.cno)        

class Section(db.Model):
    term = db.Column(db.String(2),db.CheckConstraint('term in (FA,SP,SU)'))
    year = db.Column(db.Integer)
    crn = db.Column(db.Integer,primary_key=True)
    cprefix = db.Column(db.String(4))
    cno = db.Column(db.Integer)
    section = db.Column(db.Integer)
    days = db.Column(db.String(6))
    starttime = db.Column(db.String(5))
    endtime = db.Column(db.String(5))
    room = db.Column(db.String(10))
    cap = db.Column(db.Integer)
    instructor = db.Column(db.String(30))
    auth = db.Column(db.String(1),db.CheckConstraint('auth in (Y,N)'))
    course_cpcrn = db.Column(db.Integer,db.ForeignKey('course.cno'))
    section = db.relationship('Enroll',backref='section',lazy='dynamic')

    def __repr__(self):
        return '<Section {}>'.format(self.crn)


class Enroll(db.Model):
    eid = db.Column(db.Integer,db.Sequence('enroll_eid_seq'),db.CheckConstraint('eid > 999 and eid<10000'),primary_key=True)
    sid = db.Column(db.Integer)
    term = db.Column(db.String(2),db.CheckConstraint('term in (FA,SP,SU)'))
    year = db.Column(db.Integer)
    crn = db.Column(db.Integer)
    grade = db.Column(db.String(2),db.CheckConstraint('grade in (A,B,C,D,F,I,IP,S,U)'))
    student_sid = db.Column(db.Integer,db.ForeignKey('student.sid'))
    section_tyc = db.Column(db.Integer,db.ForeignKey('section.crn'))

    def __repr__(self):
        return '<Enroll {}>'.format(self.sid)