from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db = SQLAlchemy(app)


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Todo - {self.id}"

    def cast(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at
        }


@app.route("/", methods=["GET"])
def indexRoute():
    tasks = Todo.query.order_by(Todo.created_at).all()
    # return render_template("index.html", tasks=tasks)

    tasksJson = [task.cast() for task in tasks]
    return jsonify(tasksJson)


@app.route("/add", methods=["POST"])
def addTask():
    content = request.form["content"]
    newTask = Todo(content=content)

    try:
        db.session.add(newTask)
        db.session.commit()

        return redirect("/")
    except:
        return "Error - 500"


@app.route("/delete/<int:id>", methods=["GET"])
def deleteTask(id):
    taskToDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()

        return redirect("/")
    except:
        return "Error - 500"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def updateTask(id):
    taskToUpdate = Todo.query.get_or_404(id)

    if request.method == "GET":
        return render_template("update.html", task=taskToUpdate)
    else:
        updatedContent = request.form["content"]
        taskToUpdate.content = updatedContent

        try:
            db.session.commit()

            return redirect("/")
        except:
            return "Error - 500"


if __name__ == "__main__":
    app.run(debug=True)
