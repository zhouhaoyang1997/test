# coding=utf-8
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
conn = MongoClient('127.0.0.1', 27017)
db = conn.test


@app.route('/')
def show():
    list = db.student.find()
    return render_template("show.html", list=list)


@app.route('/del')
@app.route('/del/<string:stuNo>')
def dele(stuNo=None):
    db.student.remove({"stuNo": stuNo})
    list = db.student.find()
    return render_template("show.html", list=list)


@app.route('/addForm')
def addForm():
    return render_template("add.html")


@app.route('/add', methods=["POST"])
def add():
    stuNo = request.form.get('stuNo')
    sname = request.form.get('sname')
    grade = request.form.get('grade')
    clas = request.form.get('class')
    db.student.insert({"stuNo": stuNo,
                       "sname": sname,
                       "grade": grade,
                       "class": clas})
    list = db.student.find()
    return render_template("show.html", list=list)


@app.route('/updataForm')
@app.route('/updataForm/<string:stuNo>')
def updataForm(stuNo=None):
    list = db.student.find_one({"stuNo": stuNo})
    return render_template("updata.html", list=list)


@app.route('/updata/', methods=["POST"])
@app.route('/updata/<string:updatastuNo>', methods=["POST"])
def updata(updatastuNo=None):
    stuNo = request.form.get('stuNo')
    sname = request.form.get('sname')
    grade = request.form.get('grade')
    clas = request.form.get('class')
    db.student.update({"stuNo": updatastuNo}, {"stuNo": stuNo,
                                               "sname": sname,
                                               "grade": grade,
                                               "class": clas})
    list = db.student.find()
    return render_template("show.html", list=list)


if __name__ == '__main__':
    app.run()
