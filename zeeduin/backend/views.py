from flask import Blueprint, render_template, redirect, url_for
from sqlalchemy import text
import zeeduin.models as M
import zeeduin.backend.forms as F
from zeeduin import db


backend_blueprint = Blueprint('backends', __name__, template_folder='./templates/backends')


## Homepage van de backend
@backend_blueprint.route('/backend')
def back_home():
    return render_template('be_home.html')


@backend_blueprint.route('/be_toevoegen/<table>', methods=['GET', 'POST'])
def be_toevoegen(table):
    if table == 'boeking':
        form = F.BeToevoegenBoeking()
        
        dd_data_gast = db.session.execute(db.select(M.Gast)).scalars()
        dd_data_huis = db.session.execute(db.select(M.Huis)).scalars()
        
        form.gast.choices = [gast.email for gast in dd_data_gast]
        form.huis.choices = [huis.naam for huis in dd_data_huis]
        
        if form.validate_on_submit():
            my_boeking = M.Boeking(gast=form.gast.data, huis=form.huis.data, week=form.week.data)
            db.session.add(my_boeking)
            db.session.commit()
            return redirect(url_for('be_overzicht', table=table))
        
        return render_template('be_toevoegen.html', form=form, table=table)
    
    elif table == 'huis':
        form = F.BeToevoegenHuis()
        dd_data_types = db.session.execute(db.select(M.Types)).scalars()
        
        form.huisType.choices = [htype.idType for htype in dd_data_types]
        
        if form.validate_on_submit():
            new_huis = M.Huis(naam=form.naam.data, huistype=form.huisType.data)
            db.session.add(new_huis)
            db.session.commit()
            return redirect(url_for('be_overzicht', table=table))
        
        return render_template('be_toevoegen.html', form=form, table=table)
    
    elif table == 'types':
        form = F.BeToevoegenTypes()
        
        if form.validate_on_submit():
            new_type = M.Types(idType=form.idType.data, capaciteit=form.capaciteit.data, weekprijs=form.weekprijs.data)
            db.session.add(new_type)
            db.session.commit()
            return redirect(url_for('be_overzicht', table=table))
        
        return render_template('be_toevoegen.html', form=form, table=table)
    
    elif table == 'gast':
        form = F.BeToevoegenGast()
        
        if form.validate_on_submit():
            my_gast = M.Gast(email=form.email.data, wachtwoord=form.wachtwoord.data)
            db.session.add(my_gast)
            db.session.commit()
            return redirect(url_for('be_overzicht', table=table))
        
        return render_template('be_toevoegen.html', form=form, table=table)


@backend_blueprint.route('/be_verwijderen/<table>', methods=['GET', 'POST'])
def be_verwijderen(table):
    form = None
    
    sqlstr = text(f'select * from {table}')
    
    table_values = db.session.execute(sqlstr)
    
    if table == 'boeking':
        form = F.BeVerwijderenBoeking()
        
        form.boeking.choices = [boeking.idboeking for boeking in table_values]
        
        if form.validate_on_submit():
            # print(form.boeking.data)
            boeking = db.session.execute(db.select(M.Boeking).filter_by(idboeking=form.boeking.data)).scalar_one()
            db.session.delete(boeking)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='boeking'))
    
    elif table == 'gast':
        form = F.BeVerwijderenGast()
        
        form.gast.choices = [gast.email for gast in table_values]
        
        if form.validate_on_submit():
            my_gast = db.session.execute(db.select(M.Gast).filter_by(email=form.gast.data)).scalar_one()
            db.session.delete(my_gast)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='gast'))
    
    elif table == 'huis':
        form = F.BeVerwijderenHuis()
        
        form.huis.choices = [huis.naam for huis in table_values]
        
        if form.validate_on_submit():
            my_huis = db.session.execute(db.select(M.Huis).filter_by(naam=form.huis.data)).scalar_one()
            db.session.delete(my_huis)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='huis'))
    
    elif table == 'types':
        form = F.BeVerwijderenTypes()
        
        form.types.choices = [types.idType for types in table_values]
        
        if form.validate_on_submit():
            my_type = db.session.execute(db.select(M.Types).filter_by(idType=form.types.data)).scalar_one()
            db.session.delete(my_type)
            db.session.commit()
            return redirect(url_for('be_verwijderen', table='types'))
    
    sqlstr = text(f'select * from {table}')
    
    table_values = db.session.execute(sqlstr)
    
    return render_template('be_verwijderen.html', data=table_values, form=form, table=table)


@backend_blueprint.route('/be_overzicht/<table>')
def be_overzicht(table):
    sqlstr = text(f'select * from {table}')
    
    table_values = db.session.execute(sqlstr)
    
    return render_template('be_overzicht.html', table=table, data=table_values)
