from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/flaskSQL1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(70),unique=True)
    description = db.Column(db.String(100))

    def __init__(self,title,description):
        self.title = title
        self.description = description

with app.app_context():
    db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "title",
            "description"
        )

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route("/tasks",methods=["POST"])
def create_task():
    data = request.get_json()
    title = data["title"]
    description = data["description"]

    newTask = Task(title,description)

    db.session.add(newTask)
    db.session.commit()

    return task_schema.jsonify(newTask)

@app.route("/allTasks",methods=["GET"])
def get_all_task():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    print(result)

    return tasks_schema.jsonify(result)


@app.route("/singleTask",methods=["POST"])
def get_single_task():
    data = request.get_json()
    idTask = data["id"]

    task = Task.query.get(idTask)
    print(task)

    return task_schema.jsonify(task)


@app.route("/editSingleTask/<id>",methods=["PUT"])
def edit_single_task(id):
    data = request.get_json()
    title= data["title"]
    description = data["description"]
    

    task = Task.query.get(id)
    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)


@app.route("/deleteSingleTask/<id>",methods=["DELETE"])
def delete_single_task(id):
    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)


if __name__ == "__main__":
    app.run(debug=True)