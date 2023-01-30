from flask import render_template, redirect, url_for
from model import db, app, Huis, Boeking, Gast, Types
from forms import reserverenWeek, BoekenForm, BeToevoegenBoeking, BeToevoegenHuis, BeToevoegenTypes, BeToevoegenGast, BeVerwijderenBoeking, \
    BeVerwijderenGast, BeVerwijderenHuis, BeVerwijderenTypes
from sqlalchemy import text

# MySQL variation

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'Hanze12345'
# app.config['MYSQL_DB'] = 'zeeenduin'

app.config['SECRET_KEY'] = 'mijnsecretkey'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/overzicht')
def huisjes():
    alle_huisjes = Huis.query.all()
    print(*alle_huisjes, sep='\n')
    
    return render_template('overzicht_huisjes.html', huisjes=alle_huisjes)


@app.route('/boeken/<huistype>', methods=['GET', 'POST'])
def boeken(huistype):
    form = reserverenWeek()
    imgsrc = ''
    omschrijving = ''
    
    if form.validate_on_submit():
        week = form.week.data
        return redirect(url_for('boeken_2', huistype=huistype, week=week))
    
    if huistype == 'duinhaas':
        imgsrc = '/static/bun_4pax.jpg'
        txtfile = open("static/Duinhaas.txt", 'r')
        omschrijving = txtfile.read()
    elif huistype == 'flierefluiter':
        imgsrc = '/static/bun_6pax.jpg'
        txtfile = open("static/Flierefluiter.txt", 'r')
        omschrijving = txtfile.read()
    elif huistype == 'zeepaardje':
        imgsrc = '/static/bun_8pax.jpg'
        txtfile = open("static/Zeepaardje.txt", 'r')
        omschrijving = txtfile.read()
    
    return render_template('boeken.html', huistype=huistype, form=form, imgsrc=imgsrc, omschrijving=omschrijving)


@app.route('/boeken_2/<huistype>/<week>', methods=['POST', 'GET'])
def boeken_2(huistype, week):
    # vrije_huisjes = db.session.execute("""select * from boeking""") #TODO cleanup
    
    vrije_huisjes = db.session.execute(text("select huis.naam from huis where huis.huistype = :huistype and huis.naam NOT "
                                       "IN (select huis from boeking where boeking.week = :week);"),
                                       {'huistype': huistype, 'week': week})
    
    form = BoekenForm()
    form.huis.choices = [huis[0] for huis in vrije_huisjes]
    
    if form.validate_on_submit():
        
        exist_gast = db.session.execute(text('SELECT EXISTS(SELECT * FROM gast WHERE email= :email)'), {'email': form.gast.data})
        my_check = [item[0] for item in exist_gast]
        if my_check == [0]:
            new_gast = Gast(email=form.gast.data, wachtwoord=form.wachtwoord.data)
            db.session.add(new_gast)
            # db.session.commit()
            
        # TODO check wachtwoord on exisiting gast!
        new_boeking = Boeking(gast=form.gast.data, huis=form.huis.data, week=int(week))
        print(type(new_boeking), new_boeking)
        db.session.add(new_boeking)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('boeken_beschikbaarheid.html', form=form, huis=vrije_huisjes, huistype=huistype, week=week)


@app.route('/backend')
def back_home():
    return render_template('be_home.html')


@app.route('/be_toevoegen/<table>', methods=['GET', 'POST'])
def be_toevoegen(table):                    # TODO: add to database, check for doubles
    if table == 'boeking':
        form = BeToevoegenBoeking()
       
        dd_data_gast = db.session.execute(text('SELECT email FROM gast'))
        dd_data_huis = db.session.execute(text('SELECT naam FROM huis'))
        
        form.gast.choices = [gast.email for gast in dd_data_gast]
        form.huis.choices = [huis.naam for huis in dd_data_huis]
        
        if form.validate_on_submit():
            return redirect(url_for('be_overzicht', table=table))

            # TODO database connection and update
        return render_template('be_toevoegen.html', form=form, table=table)
        
    elif table == 'huis':
        form = BeToevoegenHuis()
        dd_data_types = db.session.execute(text('SELECT idType FROM types'))
        
        form.huisType.choices = [htype.idType for htype in dd_data_types]
        
        if form.validate_on_submit():
            return redirect(url_for('be_overzicht', table=table))

            # TODO database connection and update
        return render_template('be_toevoegen.html', form=form, table=table)
        
    elif table == 'types':
        form = BeToevoegenTypes()
        
        if form.validate_on_submit():
            db.session.execute(text('insert into types values (:idType, :capaciteit, :weekprijs)'), {'idType': form.idType.data,
                                                                                               'capaciteit': form.capaciteit.data,
                                                                                               'weekprijs': form.weekprijs.data})
            db.session.commit()
            
            return redirect(url_for('be_overzicht', table=table))
        
        return render_template('be_toevoegen.html', form=form, table=table)
    elif table == 'gast':           # TODO: gast als laatste
        form = BeToevoegenGast()
                                    # TODO database connection and update
        return render_template('be_toevoegen.html', form=form, table=table)
    
    
@app.route('/be_verwijderen/<table>', methods=['GET', 'POST'])
def be_verwijderen(table):
    
    form = None
    
    sqlstr = text(f'select * from {table}')
    
    table_values = db.session.execute(sqlstr)
    
    if table == 'boeking':
        form = BeVerwijderenBoeking()
        
        form.boeking.choices = [boeking.idboeking for boeking in table_values]
        
        if form.validate_on_submit():
            # print(form.boeking.data)
            boeking = db.session.execute(db.select(Boeking).filter_by(idboeking=form.boeking.data)).scalar_one()
            db.session.delete(boeking)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='boeking'))
    
    elif table == 'gast':
        form = BeVerwijderenGast()
        
        form.gast.choices = [gast.email for gast in table_values]
        
        if form.validate_on_submit():
            
            my_gast = db.session.execute(db.select(Gast).filter_by(email=form.gast.data)).scalar_one()
            db.session.delete(my_gast)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='gast'))
    
    elif table == 'huis':
        form = BeVerwijderenHuis()
        
        form.huis.choices = [huis.naam for huis in table_values]
        
        if form.validate_on_submit():
            
            my_huis = db.session.execute(db.select(Huis).filter_by(naam=form.huis.data)).scalar_one()
            db.session.delete(my_huis)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='huis'))
    
    elif table == 'types':
        form = BeVerwijderenTypes()
        
        form.types.choices = [types.idType for types in table_values]
        
        if form.validate_on_submit():
            
            my_type = db.session.execute(db.select(Types).filter_by(idType=form.types.data)).scalar_one()
            db.session.delete(my_type)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='types'))
        
    sqlstr = text(f'select * from {table}')

    table_values = db.session.execute(sqlstr)
    
    return render_template('be_verwijderen.html', data=table_values, form=form, table=table)
    
    
@app.route('/be_overzicht/<table>')
def be_overzicht(table):
    
    sqlstr = text(f'select * from {table}')
    
    table_values = db.session.execute(sqlstr)
    
    return render_template('be_overzicht.html', data=table_values)


if __name__ == '__main__':
    app.run()
