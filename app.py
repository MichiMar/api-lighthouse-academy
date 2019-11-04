from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE-URL"] = "postgres://fwxorwkioztovh:8174d7631ed494e7a733e29c1c119529287a13a40c735f8796931001c8c7f68a@ec2-174-129-252-226.compute-1.amazonaws.com:5432/d2tn72tnu61a0v"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Topic(db.Model):
    __tablename__="topics"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))

    def __init__(self, title, description):
        self.title = title
        self.description = description

class TopicSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description")

topic_schema = TopicSchema()
topics_schema = TopicsSchema(many=True)

@app.route("/topics", methods=["GET"])
def get_topics():
    all_topics = Topic.query.all()
    result = topics_schema.dump(all_topics)
    return jsonify(result)

@app.route("/topic", methods=["POST"])
def add_topics():
    title = request.json["title"]
    description = request.json["description"]

    new_topic = Topic(title, description)
    db.session.add(new_topic)
    db.session.commit()

    created_topic = Topic.query.get(new_topic.id)
    return todo_schema.jsonify(created_topic)

@app.route("/topic/<id>", method=["PUT"])
def update_topic(id):
    topic = Topic.query.get(id)

    topic.title = request.json("title")
    topic.description = request.json("description")

    db.session.commit()
    return topic_schema.jsonify(topic)

@app.route("/topic/<id>", methods=["DELETE"])
def delete_topic():
    topic = Topic.query.get(id)

    db.session.delete(topic)
    db.session.commit()

    return "REACORD DELETED"

if __name__ == "__main__":
    app.debug = True
    app.run()

    response
    
