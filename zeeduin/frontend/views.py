from flask import Blueprint, render_template, redirect, url_for
from sqlalchemy import text
from zeeduin.frontend.forms import BoekenForm, reserverenWeek
from zeeduin import db
from zeeduin.models import Boeking, Gast, Types, Huis


frontend_blueprint = Blueprint('frontends', __name__, template_folder='./templates/frontends')


@frontend_blueprint.route('/info')
def info():
    return render_template('info.html')


@frontend_blueprint.route('/overzicht')
def huisjes():
    stmt = db.session.execute(db.select(Huis, Types).join_from(Huis, Types, Huis.huistype == Types.idType))
    
    return render_template('overzicht_huisjes.html', huisjes=stmt)


### 2 stappen van de boeking wizzard
@frontend_blueprint.route('/boeken/<huistype>', methods=['GET', 'POST'])
def boeken(huistype):
    form = reserverenWeek()
    imgsrc = ''
    omschrijving = ''
    
    if form.validate_on_submit():
        week = form.week.data
        return redirect(url_for('frontends.boeken_2', huistype=huistype, week=week))
    
    if huistype.lower() == 'duinhaas':
        imgsrc = '/static/bun_4pax.jpg'
        # I surrender..
        omschrijving = "Dit de Duinhaas tekst, met meer informatie over het huis, de verdiepingen, de uitrusting, slaapplaatsen en slaapkamers etc etc Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquam distinctio eveniet expedita facere, facilis harum illo, illum, iure laborum laudantium nemo non placeat quae reiciendis temporibus vel velit voluptas voluptatibus?"
    elif huistype.lower() == 'flierefluiter':
        imgsrc = '/static/bun_6pax.jpg'
        omschrijving = "Dit de Flierefluiter tekst, met meer informatie over het huis, de verdiepingen, de uitrusting, slaapplaatsen en slaapkamers etc etc Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquam distinctio eveniet expedita facere, facilis harum illo, illum, iure laborum laudantium nemo non placeat quae reiciendis temporibus vel velit voluptas voluptatibus?"
    elif huistype.lower() == 'zeepaardje':
        imgsrc = '/static/bun_8pax.jpg'
        omschrijving = 'Dit de Duinhaas tekst, met meer informatie over het huis, de verdiepingen, de uitrusting, slaapplaatsen en slaapkamers etc etc Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquam distinctio eveniet expedita facere, facilis harum illo, illum, iure laborum laudantium nemo non placeat quae reiciendis temporibus vel velit voluptas voluptatibus?'
    
    return render_template('boeken.html', huistype=huistype, form=form, imgsrc=imgsrc, omschrijving=omschrijving)


@frontend_blueprint.route('/boeken_2/<huistype>/<week>', methods=['POST', 'GET'])
def boeken_2(huistype, week):
    
    vrije_huisjes = db.session.execute(text("select huis.naam from huis where huis.huistype = :huistype and huis.naam NOT "
                                            "IN (select huis from boeking where boeking.week = :week);"),
                                       {'huistype': huistype, 'week': week})
    # TODO: to be continued: Figure out converting above sql in below syntax...
    
    # vh = db.session.execute(db.select(Huis).filter(~Huis.naam.in_(db.select(Huis.naam).filter(Boeking.huis).where(Boeking.week == week))))
    # print(vh.scalars().all())
    
    form = BoekenForm()
    form.huis.choices = [huis[0] for huis in vrije_huisjes]
    
    if form.validate_on_submit():
        
        exist_gast = db.session.execute(text('SELECT EXISTS(SELECT * FROM gast WHERE email= :email)'), {'email': form.gast.data})
        my_check = [item[0] for item in exist_gast]
        if my_check == [0]:
            new_gast = Gast(email=form.gast.data, wachtwoord=form.wachtwoord.data)
            db.session.add(new_gast)
        
        new_boeking = Boeking(gast=form.gast.data, huis=form.huis.data, week=int(week))
        print(type(new_boeking), new_boeking)
        db.session.add(new_boeking)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('boeken_beschikbaarheid.html', form=form, huis=vrije_huisjes, huistype=huistype, week=week)
