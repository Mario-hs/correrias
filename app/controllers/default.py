from flask import Flask, jsonify, request
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import app, db

from app.models.db import Station, Package, Transaction, session
from app.models.forms import LoginForm, RegisterForm, PackageRegisterForm


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
    # if request.method == 'POST':
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
        package = session.query(Transaction).filter(Transaction.destiny_id == current_user.id)

        for p in package:
            station_dest = session.query(Station).filter(Station.id == p.destiny_id).all()
            station_ori = session.query(Station).filter(Station.id == p.source_id).all()

            for o in station_ori:
                # orig_id = o.id
                orig_name = o.name

                for d in station_dest:
                    # dest_id = d.id
                    dest_name = d.name

            lista_package.append(
                {
                    "id": p.id,
                    "source_id":p.source_id,
                    "destiny_id":p.destiny_id,
                    "status_transaction":p.status_transaction,
                    "orig": orig_name,
                    "dest": dest_name,
                }
            )

    # current_user pega o usuário logado
    if current_user.is_authenticated:
        print(current_user.id)
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


    # elif request.method == "POST" and form.validate():
    elif request.method == "POST":
       
        print('ENTREI')
        print(current_user.id)
        print(form.weight.data)
        print(form.cpf.data)
        print(form.name.data)
        print()
        # pack = request.json
        # session.add(
            # Transaction(
            #     package_id= pack["package_id"],
            #     destiny_id= pack["destiny_id"],
            #     source_id= pack["source_id"],
            #     status_transaction = pack["status_transaction"],
            # ),
            # Package(
            #     weight = pack["weight"],
            #     sender_cpf = pack["sender_cpf"],
            #     sender_name = pack["sender_name"]
            # )

        #     Transaction(
        #         # package_id= form.id.data,
        #         package_id= 1,
        #         destiny_id= 1,
        #         source_id= current_user.id,
        #         status_transaction = False,
        #     ),
        #     Package(
        #         weight = form.weight.data,
        #         sender_cpf = form.cpf.data,
        #         sender_name = form.name.data
        #     )
        # )
        # session.commit()
        # print(Transaction)
        # print(Package)
        # return url_for('order'), 200
        

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
        package = session.query(Transaction).filter(Transaction.source_id == current_user.id)

        for p in package:
            station_dest = session.query(Station).filter(Station.id == p.destiny_id).all()
            station_ori = session.query(Station).filter(Station.id == p.source_id).all()

            for o in station_ori:
                # orig_id = o.id
                orig_name = o.name

                for d in station_dest:
                    # dest_id = d.id
                    dest_name = d.name

            lista_package.append(
                {
                    "id": p.id,
                    "source_id":p.source_id,
                    "destiny_id":p.destiny_id,
                    "status_transaction":p.status_transaction,
                    "orig": orig_name,
                    "dest": dest_name,
                }
            )
        for l in lista_package:
            print()
            # print(l['orig'])
            print(l)
            print()
    return render_template('package.html', lista_package = lista_package)