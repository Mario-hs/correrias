from flask import Flask, jsonify, request
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import app
from app.models.db import Station, Package, Transaction, session
from app.models.forms import LoginForm, RegisterForm, PackageRegisterForm, UpdateRegisterPack
# current_user pega o usuário logado


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
                    name=form.name.data,
                    password = form.password.data,
                    email=form.email.data,
                    cnpj=form.cnpj.data
                )
            )
            session.commit()

            return redirect(url_for('index'))
        except Exception as ex:
            return print(ex)
    return render_template('register.html', form=form)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))


@app.route("/home", methods=["GET", "PUT", "POST"])
def home():
    if current_user.is_authenticated:
        form = UpdateRegisterPack(request.form)
        if request.method == "POST":
            pack_confirmed = form.id.data
            session.query(Transaction).filter(Transaction.package_id == pack_confirmed).update({"status_transaction": 1})
            session.commit()
            return render_template('home.html', lista_package = lista_package, form = form)

        if request.method == "GET":
            lista_package = []
            transaction = session.query(Transaction).filter(Transaction.destiny_id == current_user.id)

            for trans in transaction:
                if trans.status_transaction != 1:
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
                
            return render_template('home.html', lista_package = lista_package, form = form)
        
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

    if current_user.is_authenticated:
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
                    status_transaction = 0,
                )
            )
            session.commit()
            return redirect(url_for('order'))
        return render_template('order.html', form=form)
    else:
        return redirect(url_for('index'))


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
    if current_user.is_authenticated:
        if request.method == "GET":
            lista_package_source = []
            lista_package_destiny = []
            source_transaction = session.query(Transaction).filter(Transaction.source_id == current_user.id)
            destiny_transaction = session.query(Transaction).filter(Transaction.destiny_id == current_user.id)

            for trans in source_transaction:
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
                lista_package_source.append(
                    {
                        "id": idPack,
                        "source_id": trans.source_id,
                        "destiny_id": trans.destiny_id,
                        "status_transaction": trans.status_transaction,
                        "orig": orig_name,
                        "dest": dest_name,
                    }
                )
            for trans in destiny_transaction:
                if trans.status_transaction == 1:
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
                    lista_package_destiny.append(
                        {
                            "id": idPack,
                            "source_id": trans.source_id,
                            "destiny_id": trans.destiny_id,
                            "status_transaction": trans.status_transaction,
                            "orig": orig_name,
                            "dest": dest_name,
                        }
                    )
        return render_template('package.html', lista_package_source = lista_package_source, lista_package_destiny = lista_package_destiny)
    else:
        return redirect(url_for('index'))