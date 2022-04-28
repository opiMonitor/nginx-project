import random
import json
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields, marshal_with


class ReverseProxied(object):
    def __init__(self, app, script_name):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.script_name
        return self.app(environ, start_response)


app = Flask(__name__)
api = Api(app)
app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/flask')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@postgres:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# klasa xxModels(db.Model) to klasa odwzorowujące strukturę naszej bazy danych. każda klasa będzie stwoją własną tabela w bazie danych.
# np klasa HostModels(db.Model) to klasa przechowująca dane na temat hostów. Jeśli chcemy wykorzystać istniejącą już tabelę w bazie
# danych, to tworzymy takie same kolumny jak w istniejącej. czyli jeśli w bazie danych pierwsza kolumna nazywa się 'id' to tworzymy zmienną
# id = db.Column(db.Integer, primary_key=True) itd.
class HostsModels(db.Model):
    __tablename__ = 'host'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.UnicodeText())
    ip = db.Column(db.UnicodeText())
    date = db.Column(db.DateTime())

    def __init__(self, host, ip, id, date):
        self.host = host
        self.ip = ip
        self.id = id
        self.date = date

    def __repr__(self):
        return f"Object HostsModels - NAME:{self.host}; IP: {self.ip}; LP: {self.id}"


class UrlModels(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.UnicodeText())

    def __init__(self, id, url):
        self.id = id
        self.url = url

    def __repr__(self):
        return f"Object UrlModels - URL: {self.url}; ID: {self.id}"


# API
resource_fields = {
    'id': fields.Integer,
    'host': fields.String,
    'ip': fields.String,
    'date': fields.String,
}
url_fields = {
    'id': fields.Integer,
    'url': fields.String,
}


class HostList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        data = HostsModels.query.all()
        return data


class UrlList(Resource):
    @marshal_with(url_fields)
    def get(self):
        data = UrlModels.query.all()
        return data


api.add_resource(HostList, "/list")
api.add_resource(UrlList, "/urls")


@app.route('/')
def get_temperature():

    data = HostsModels.query.all()

    # gdzie hosts to zmienna w template a data to zmienna tutaj
    return render_template('home.html', hosts=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
