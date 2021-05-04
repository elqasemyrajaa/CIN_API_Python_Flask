from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Isnit ma
ma = Marshmallow(app)

# CIN /class Model


class Cin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(200))
    cin = db.Column(db.String(100))
    lieu_naissance = db.Column(db.String(100))
    adress = db.Column(db.String(200))
    date_naissance = db.Column(db.String(100))

    def __init__(self, nom, prenom, cin, lieu_naissance, adress, date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.cin = cin
        self.lieu_naissance = lieu_naissance
        self.adress = adress
        self.date_naissance = date_naissance

# product schema


class CinSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nom', 'prenom', 'cin',
                  'lieu_naissance', 'adress', 'date_naissance')


# Init Schema
cin_schema = CinSchema()
cins_schema = CinSchema(many=True)


# /************************************/
# create CIn  (Post)
@app.route('/add', methods=['POST'])
def add_cin():
    nom = request.json['nom']
    prenom = request.json['prenom']
    cin = request.json['cin']
    lieu_naissance = request.json['lieu_naissance']
    adress = request.json['adress']
    date_naissance = request.json['date_naissance']
    new_cin = Cin(nom, prenom, cin, lieu_naissance, adress, date_naissance)
    db.session.add(new_cin)
    db.session.commit()
    return cin_schema.jsonify(new_cin)

# /************************************/
# fetch all cin


@app.route('/cin', methods=['GET'])
def get_cins():
    all_cins = Cin.query.all()
    result = cins_schema.dump(all_cins)
    return jsonify(result)
# /************************************/
# fetch One  cin


@app.route('/cin/<id>', methods=['GET'])
def get_cin(id):
    cin = Cin.query.get(id)
    return cin_schema.jsonify(cin)


# /************************************/
# Update cin  (Put)
@app.route('/update/<id>', methods=['PUT'])
def update_cin(id):
    cine = Cin.query.get(id)
    nom = request.json['nom']
    prenom = request.json['prenom']
    cin = request.json['cin']
    lieu_naissance = request.json['lieu_naissance']
    adress = request.json['adress']
    date_naissance = request.json['date_naissance']

    cine.nom = nom
    cine.prenom = prenom
    cine.cin = cin
    cine.lieu_naissance = lieu_naissance
    cine.adress = adress
    cine.date_naissance = date_naissance
    db.session.commit()
    return cin_schema.jsonify(cine)
# **************************************************
# Delete  cins


@app.route('/delete/<id>', methods=['DELETE'])
def delete_cin(id):
    cin = Cin.query.get(id)
    db.session.delete(cin)
    db.session.commit()
    return cin_schema.jsonify(cin)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
