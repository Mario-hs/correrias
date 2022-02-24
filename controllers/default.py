from flask import Flask, jsonify, request
from flask import redirect, render_template, request, url_for
from app import app, db

from app.models.db import Station, session
from app.models.forms import LoginForm, RegisterForm


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            print(form.username.data)
            print(form.password.data)
            return redirect(url_for('home'))
        except Exception as ex:
            return print(ex)
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

@app.route("/", methods=["GET", "POST"])
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/view-all")
def view():
    return "<h1>View All</h1>"


@app.route("/register-update")
def registerUpdate():
    return "<h1>Register Update</h1>"


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