from os import name
from tokenize import String
from flask import Flask, jsonify, request
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_user
from sqlalchemy import null
from app import app, db

from app.models.db import Station, Package, Transaction, session
from app.models.forms import LoginForm, RegisterForm


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
    # if request.method == 'POST':
        try:
            user = (session.query(Station).filter(form.name.data == Station.name).one())
            if user and form.password.data == user.password:
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Invalid Login")
                return render_template('sign-in.html', form=form)

        except Exception as ex:
            return print()
    else:
        return render_template('sign-in.html', form=form)
                


@app.route("/register", methods=["GET", "POST"])
def registerStation():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            session.add(
                Station(
                    name=form.username.data,
                    password = form.password.data,
                    email=form.email.data,
                    cnpj=form.cnpj.data
                )
            )
            session.commit()

            return url_for('dashboard'), 200
        except Exception as ex:
            return print(ex)
    return render_template('register.html', form=form)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route("/home", methods=["GET"])
def home():
    # print(int(load_user(Station.get_id.fget())))
    # print(Station.get_id)
    return render_template('home.html', user=Station.get_id.__get__)

@app.route("/view-all")
def view():
    return "<h1>View All</h1>"


@app.route("/register-update")
def registerUpdate():
    return "<h1>Register Update</h1>"


@app.route("/order", methods=["GET", "POST", "PUT", "DELETE"])
def order():
    if request.method == "GET":
        lista_package = []

        # session.query(Package).filter(Package.id_package == 1)

        package = session.query(Transaction).all()

        for p in package:

            station_dest = session.query(Station).filter(Station.id == p.destiny_id).all()

            station_ori = session.query(Station).filter(Station.id == p.source_id).all()

            lista_package.append(
                {
                    "id": p.id,
                    "source_id":p.source_id,
                    "destiny_id":p.destiny_id,
                    "status_transaction":p.status_transaction,
                }
            )

        for s in station_ori:
            lista_package.append(
                {
                    "orig": s.name,
                }
            )

        for s in station_dest:
            lista_package.append(
                {
                    "dest": s.name,
                }
            )
        return jsonify(lista_package), 200

    elif request.method == "POST":
        pack = request.json
        session.add(
            Transaction(
                package_id= pack["package_id"],
                destiny_id= pack["destiny_id"],
                source_id= pack["source_id"],
                status_transaction = pack["status_transaction"],
            ),
            Package(
                weight = pack["weight"],
                sender_cpf = pack["sender_cpf"],
                sender_name = pack["sender_name"]
            )

        )
        session.commit()
        return "", 200


@app.route("/station", methods=["GET", "POST", "PUT", "DELETE"])
def station():
    if request.method == "GET":
        lista_station = []
        # session.query(Station).filter(Station.id_station == 1)
        station = session.query(Station).all()
        for s in station:
            lista_station.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "password": s.password,
                    "email":s.email,
                    "cnpj":s.cnpj
                }
            )
        return jsonify(lista_station), 200
    elif request.method == "POST":
        station = request.json
        session.add(
            Station(
                name=station["name"],
                password = station["password"],
                email=station["email"],
                cnpj=station["cnpj"]
            )
        )
        session.commit()
        return "", 200