# coding=utf-8
from flask import Flask, render_template, request, json, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
conn = MongoClient('127.0.0.1', 27017)
db = conn.Maoyan


@app.route('/')
def show():
    # list = db.movies.find()
    return render_template("show.html")


@app.route('/getMovieList')
def getMovieList():
    list = db.movies.find()

    # print dumps(list)
    return  dumps(list)


#
# @app.route('/del')
# @app.route('/del/<string:stuNo>')
# def dele(stuNo=None):
#     db.student.remove({"stuNo": stuNo})
#     list = db.student.find()
#     return render_template("show.html", list=list)





if __name__ == '__main__':
    app.run()
