from flask import Flask, jsonify, request
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import app
from app.models.db import Station, Package, Transaction, session
from app.models.forms import LoginForm, RegisterForm, PackageRegisterForm


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            user = (session.query(Station).filter(form.name.data == Station.name).first())
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

@app.route("/logout")                
def logout():
    logout_user()
    return redirect(url_for('index'))

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

            return url_for('index'), 200
        except Exception as ex:
            return print(ex)
    return render_template('register.html', form=form)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route("/home", methods=["GET"])
def home():
    if request.method == "GET":
        lista_package = []
        transaction = session.query(Transaction).filter(Transaction.destiny_id == current_user.id)

        for trans in transaction:
            station_dest = session.query(Station).filter(Station.id == trans.destiny_id).all()
            station_ori = session.query(Station).filter(Station.id == trans.source_id).all()
            data_pack = session.query(Package).filter(Package.id_pack == trans.package_id).all()

            for o in station_ori:
                orig_id = o.id
                orig_name = o.name

                for d in station_dest:
                    dest_id = d.id
                    dest_name = d.name

            for p in data_pack:
                idPack = p.id_pack
            lista_package.append(
                {
                    "id": idPack,
                    "source_id": orig_name,
                    "destiny_id": dest_name,
                    "status_transaction": trans.status_transaction,
                    "orig": orig_name,
                    "dest": dest_name,
                }
            )
            
    # current_user pega o usuário logado
    if current_user.is_authenticated:
        return render_template('home.html', lista_package = lista_package)
    else:
        return redirect(url_for('index'))

@app.route("/view-all")
def view():
    return "<h1>View All</h1>"


@app.route("/register-update")
def registerUpdate():
    return "<h1>Register Update</h1>"


@app.route("/order", methods=["GET", "POST", "PUT", "DELETE"])
def order():
    form = PackageRegisterForm(request.form)

    if request.method == "GET":
        stations = (
                    session.query(Station)
                    .filter(Station.id != current_user.id)
                    .all()
                )
        for o in stations:
            print(o.name)
        return render_template('order.html', form=form, stations=stations)


    elif request.method == "POST" and form.validate():
    # elif request.method == "POST":
        select = request.form.get('station')
        pack = request.json
        session.add(
            Package(
                id_pack = form.id_pack.data,
                weight = form.weight.data,
                sender_cpf = form.cpf.data,
                sender_name = form.name.data,
                sender_email = form.email.data
            )
        )
        session.commit()

        session.add(
            Transaction(
                package_id= form.id_pack.data,
                destiny_id= select,
                source_id= current_user.id,
                status_transaction = False,
            )
        )
        session.commit()
        return url_for('order'), 200   
    return render_template('order.html', form=form)


@app.route("/station", methods=["GET", "POST", "PUT", "DELETE"])
def station():
    if request.method == "GET":
        lista_station = []
        
        # session.query(Station).filter(Station.id_station == 1)
        station = session.query(Station.id, Station.name, Station.password, Station.email, Station.cnpj).all()
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

@app.route("/packages", methods=["GET", "POST", "PUT", "DELETE"])
def package():
    if request.method == "GET":
        lista_package = []
        transaction = session.query(Transaction).filter(Transaction.source_id == current_user.id)

        for trans in transaction:
            station_dest = session.query(Station).filter(Station.id == trans.destiny_id).all()
            station_ori = session.query(Station).filter(Station.id == trans.source_id).all()
            data_pack = session.query(Package).filter(Package.id_pack == trans.package_id).all()

            for o in station_ori:
                orig_id = o.id
                orig_name = o.name

                for d in station_dest:
                    dest_id = d.id
                    dest_name = d.name

            for p in data_pack:
                idPack = p.id_pack
            lista_package.append(
                {
                    "id": idPack,
                    "source_id": trans.source_id,
                    "destiny_id": trans.destiny_id,
                    "status_transaction": trans.status_transaction,
                    "orig": orig_name,
                    "dest": dest_name,
                }
            )
    return render_template('package.html', lista_package = lista_package)