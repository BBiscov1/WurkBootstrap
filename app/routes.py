from flask import *
from app import myapp, db, mail
from app.form import *
from app.database import *
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from app.servicedesc import services as dictofservices
import random
from random import randint
import string
import json
import os
from werkzeug.utils import secure_filename


def getInfo(username):
    select = "SELECT * from users where username = '" + str(username) + "'"
    cursor.execute(select)
    records = cursor.fetchall()
    return records


def getService(tos):
    select = "SELECT description from services where name = '" + str(tos) + "'"
    cursor.execute(select)
    records = cursor.fetchall()
    return records


def sendemail(bid):
    booking = Booking.query.filter_by(bookingid=bid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bid).first()
    client = Client.query.filter_by(bookingid=bid).first()

    msg = Message("Your booking has been made!",
                  sender='wurkservices@gmail.com', recipients=[client.email], bcc=["bookings@wurkservices.com"])
    msg.body = "a new booking has been made"
    msg.html = render_template('emailtemplate.html', name=client.name, service=booking.typeofbooking, month=bookingtime.month, day=bookingtime.day, time=bookingtime.starttime, email=client.email, pnum=client.phonenumber, address=client.address + " " +
                               client.city + " " + client.state, comment=booking.comments)
    mail.send(msg)


def returnMonth(day):
    if day == '01':
        return 'January'
    if day == '02':
        return 'Feburary'
    if day == '03':
        return 'March'
    if day == '04':
        return 'April'
    if day == '05':
        return 'May'
    if day == '06':
        return 'June'
    if day == '07':
        return 'July'
    if day == '08':
        return 'August'
    if day == '09':
        return 'September'
    if day == '10':
        return 'October'
    if day == '11':
        return 'November'
    if day == '12':
        return 'December'


@myapp.route("/")
def index():
    return render_template("index.html", pagetitle="Wurk Services")


@myapp.route("/login", methods=['GET', 'POST'])
def login():
    error = request.args.get('uErr')
    form = loginform()
    return render_template("login.html", uErr=error, pagetitle="Login", form = form)

@myapp.route("/loginhandler", methods=['POST'])
def loginhandler():
    username = request.form['username']
    password = request.form['password']
    try:
        remember = request.form['remember']
    except:
        remember = False
    u = User.query.filter_by(username=username).first()
    if not u:
        flash("Error")
        return redirect(url_for("login", uErr=True))
    if u.password == password:
        login_user(u, remember=remember)
        if u.username == 'admin':
                return redirect(url_for("admin"))
        if u.username == 'wurker':
                return redirect(url_for('wurker'))
        return redirect(url_for("useraccount", username = username))
    else:
        flash("Error")
        return redirect(url_for("login", uErr=True))

@myapp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
@myapp.route("/admin", methods=['GET'])
@login_required
def admin():
    if current_user.username != 'admin':
        return redirect(url_for("useraccount"))
    booking = Booking.query.all()
    bookingtime = BookingTime.query.all()
    client = Client.query.all()
    u = db.session.query(Booking,BookingTime,Client).filter(Booking.bookingid == BookingTime.bookingid).filter(BookingTime.bookingid == Client.bookingid).all() 
    popup = request.args.get('popup')
    return render_template('adminpage.html', lst=u, popup = popup)

@myapp.route("/deletebooking/<bookingid>")
def deletebooking(bookingid):
    booking = Booking.query.filter_by(bookingid=bookingid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bookingid).first()
    client = Client.query.filter_by(bookingid=bookingid).first()
    print(booking, bookingtime, client)
    db.session.delete(booking)
    db.session.delete(bookingtime)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for("admin",popup = True))

@myapp.route("/wurker", methods=['GET'])
@login_required
def wurker():
    if current_user.isemployee == 0:
        return redirect(url_for('useraccount'))
    popup = request.args.get('popup')
    error = request.args.get('error')
    u = BookedDays.query.all()
    return render_template('tableData.html', lst=u, popup=popup, error=error)
    
@myapp.route("/register")
def register():
    form = registerform()
    return render_template("register.html", form = form)

@myapp.route("/register1Handler", methods = ["POST"])
def register1Handler():
    session['fname'] = request.form['firstname']
    session['lname'] = request.form['lastname']
    return redirect(url_for("register2"))

@myapp.route("/register2", methods = ['GET'])
def register2():
    error = request.args.get('err')
    form = registerform()
    return render_template("register2.html", err=error, form=form)

@myapp.route("/register2Handler", methods = ["POST"])
def register2Handler():
    session['uname'] = request.form['username']
    session['pword'] = request.form['password']
    u = User.query.filter_by(username=session['uname']).first()
    if u:
        return redirect(url_for("register2",err = True)) 
    return redirect(url_for("register3"))

@myapp.route("/register3")
def register3():
    form = registerform()
    return render_template("register3.html", form=form)


@myapp.route("/register3Handler", methods=['POST'])
def register3Handler():
    fname = session['fname']
    lname = session['lname']
    username = session['uname'].lower()
    password = session['pword']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    id = randint(1000000,9999999)
    u = User(id = id, username=username, password=password, isemployee = 0, bio = '')
    db.session.add(u)
    pi = PersonalInfo(id = id, email=email, phonenumber=phonenumber, city=city, state=state, address=address, person = id,firstname = fname, lastname=lname)
    db.session.add(pi)
    db.session.commit()
    return redirect(url_for("registered"))


@myapp.route("/registered")
def registered():
    return render_template('registered.html')


@myapp.route("/useraccount", methods=['GET'])
@login_required
def useraccount():
    if current_user.username == 'wurker':
        return redirect(url_for('wurker'))
    if current_user.isemployee == 1:
        return redirect(url_for('WP'))
    hasMeeting = request.args.get('hasMeeting')
    hasError = request.args.get('hasError')
    month = request.args.get('month')
    day = request.args.get('day')
    TOB = request.args.get('TOB')
    start = request.args.get('start')
    cu = current_user
    print(cu.id)
    u = User.query.filter_by(id=cu.id).all()
    info = PersonalInfo.query.filter_by(id=cu.id).first()
    print(info)
    form = loginform()
    try:
        name = info.firstname
    except:
        name = 'Unknown'
    return render_template('useraccount.html', hasError= hasError, month=month, day=day,TOB=TOB,start=start,hasMeeting = hasMeeting, uname=name, fTime=True,form=form, pagetitle="My Account")
   

#Wurk in progess 
@myapp.route("/adminhandler", methods=['post'])
def adminhandler():
    FN = request.form['FN']
    LN = request.form['LN']
    TOT = request.form['TOT']
    TID = ''.join([random.choice(string.ascii_letters + string.digits)
                   for n in range(7)])
    insert1 = "INSERT INTO teacher VALUES ('"+str(TID) + \
        "','"+str(FN)+"','"+str(LN)+"','"+str(TOT)+"')"
    cursor.execute(insert1)
    conn.commit()
    return render_template('adminpage.html')


@myapp.route("/CheckBooking", methods=['post'])
def checkbooking():
    bid = request.form['bid']
    booking = Booking.query.filter_by(bookingid=bid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bid).first()
    client = Client.query.filter_by(bookingid=bid).first()
    if booking is not None:
        return redirect(url_for('useraccount', hasMeeting=True, meetingID=bid, month = bookingtime.month, day = bookingtime.day, start = bookingtime.starttime, TOB = booking.typeofbooking))
    else:
        return redirect(url_for('useraccount', hasError=True))

@myapp.route("/services")
def services():
    return render_template('services.html', pagetitle='services')


@myapp.route("/services/<TOS>")
def TOS(TOS):
    desc = dictofservices()
    print(desc)
    try:
        meta = desc.serviceDict[TOS + " Meta"]
    except KeyError as e:
        meta = ''
    filedirectory = 'css/img/'+TOS
    if TOS == "Lawn Care":
        return render_template('lawncare.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle='Barrington Landscaping Services | Lawn Care Services | Barrington, Il | Wurk Barrington Services')
    if TOS == 'Junk Removal':
        return render_template('LC.html', baa=True, service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=TOS, meta=meta)
    return render_template('LC.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=TOS, meta=meta)

@myapp.route("/landscaping-services-barrington-il")
def thingthatarchalwanted():
    TOS = 'Lawn Care'
    desc = dictofservices()
    print(desc)
    try:
        meta = desc.serviceDict[TOS + " Meta"]
    except KeyError as e:
        meta = ''
    filedirectory = 'css/img/'+TOS
    return render_template('lawncare.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle='Barrington Landscaping Services | Lawn Care Services | Barrington, Il | Wurk Barrington Services')

@myapp.route("/services/<TOS>/StartBooking")
def TOSBook(TOS):
    session['TOB'] = TOS
    if not current_user.is_anonymous:
        return redirect(url_for("CreateBookingTimeAndDate"))
    form = registerform()
    return render_template('CBpre.html', pagetitle="Start a booking", form=form)


@myapp.route("/BookingSelector")
def BookingSelector():
    form = bookingform()
    return render_template('bookingselect.html', form=form)


@myapp.route("/TOBselector", methods=['POST'])
def BookingSelector2():
    session['TOB'] = request.form['services']
    return redirect(url_for('CreateBookingTimeAndDate'))

@myapp.route("/bookinghandler", methods=['POST'])
def bookinghandler():
    session['name'] = request.form['firstname'] + " " + request.form['lastname']
    session['email'] = request.form['email']
    session['pnum'] = request.form['phonenumber']
    session['address'] = request.form['address']
    session['city'] = request.form['city']
    session['state'] = request.form['state']
    return redirect(url_for('CreateBookingTimeAndDate'))

@myapp.route("/CreateBookingFinal" ,methods=['GET'])
def CreateBookingTimeAndDate():
    form = bookingform()
    BID = ''.join([random.choice(string.ascii_letters + string.digits)
                   for n in range(6)])
    session['bid'] = BID
    error = request.args.get('error')
    return render_template("bookingtimeanddate.html", form = form, currentbooking = session['TOB'], error = error)

@myapp.route("/FinalizeBooking", methods=['POST'])
def FinalizeBooking():
    date = request.form['day']
    time = request.form['time']
    month = returnMonth(date[5:7])
    day = str(int(date[8:10]))
    check = BookedDays.query.filter_by(day=day).first()
    if check:
        return redirect(url_for("CreateBookingTimeAndDate",error = True))
    if not current_user.is_anonymous:
        cu = current_user
        u = User.query.filter_by(id=cu.id).all()
        info = PersonalInfo.query.filter_by(id=cu.id).first()
        name = info.firstname + " " + info.lastname
        session['email'] = info.email
        session['pnum'] = info.phonenumber
        session['address'] = info.address
        session['city'] = info.city
        session['state'] = info.state
    else:
        name = session['name']
    booking = Booking(bookingid=session['bid'], clientname=name, typeofbooking=session['TOB'], comments=request.form['comments'])
    bookingtime = BookingTime(bookingid=session['bid'], month=month, day=day, starttime=request.form['time'])
    client = Client(name = name, email = session['email'], phonenumber = session['pnum'], address = session['address'], city = session['city'], state = session['state'], bookingid = session['bid'])
    
    db.session.add(booking)
    db.session.add(bookingtime)
    db.session.add(client)
    db.session.commit()
    sendemail(session['bid'])
    return redirect(url_for('created'))

@myapp.route("/BookingCreated")
def created():
    return render_template("BookingComplete.html", BID=session['bid'])
    

@myapp.route("/ContactUs")
def CU():
    return render_template("contact.html")


@myapp.route("/MeetTheTeam")
def MTT():
    return render_template("MTT.html")

@myapp.route("/WurkerPage", methods=['GET'])
@login_required
def WP():
    if current_user.isemployee == 0:
        return redirect(url_for('useraccount'))
    popupremove = request.args.get('popupremove')
    error = request.args.get('error')
    u = BookedDays.query.all()
    day = request.args.get('day')
    month = request.args.get('month')
    popup = request.args.get('popup')
    err = request.args.get('err')
    name = request.args.get('name')
    form = wurkerEntry()
    return render_template('wurker.html', user = PersonalInfo.query.filter_by(id= current_user.id).first().firstname, lst = u, popupremove = popupremove, form=form, day=day, month=month, err=err, popup=popup, name=name)

@myapp.route("/deletebookedday/<id>")
@login_required
def deleteslot(id):
    b = BookedDays.query.get(id)
    error=False
    try:
        db.session.delete(b)
        db.session.commit()
    except:
        error = True
    return redirect(url_for('WP', popupremove=True, error=error))
    

@myapp.route("/wurkerhandler", methods=['post'])
def addSceudel():
    w= PersonalInfo.query.filter_by(id=current_user.id).first()
    date = request.form['day']
    time = request.form['time']
    CN = request.form['clientName']
    TOJ = request.form['JobType']
    POTJ = request.form['POTJ']
    print(date)
    month = returnMonth(date[5:7])
    day = int(date[8:10])
    bd = BookedDays(name=w.firstname, day = day, month = month, wid = current_user.username, jobtype = TOJ, peopleonjob = POTJ, clientname = CN, time = time)
    db.session.add(bd)
    db.session.commit()
    print(w.firstname + "has updated their avaliblity")
    return redirect(url_for('WP', day=day, month=month, popup=True, name=w.firstname))

@myapp.route('/sitemap.xml')
def site_map():
    sitemap_template = render_template('sitemap.xml')
    response = make_response(sitemap_template)
    response.headers["Content-Type"] = "application/xml"
    return response





@myapp.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@myapp.route('/<wurker>/profile', methods = ['GET', 'POST'])
def wurkerprofile(wurker):
    form = UploadForm()
    try:
        os.makedirs('app/static/css/img/' + wurker)
    except:
        print('Already exists')
    if request.method == 'POST':
        file = request.files['image']
        try:
            os.makedirs('app/static/css/img/' + wurker)
        except:
            print('Already exists')
        finally:
            filename = secure_filename(file.filename)
            file.save(os.path.join('app/static/css/img/' + wurker, filename))
            p = Post(pic=filename, desc=request.form['description'], poster=current_user.id)
            db.session.add(p)
            db.session.commit()
    try:
        u = User.query.filter_by(username=wurker).first()
        p = PersonalInfo.query.filter_by(id=u.id).first()
        files = Post.query.filter_by(poster = u.id)
        if not current_user.is_anonymous and current_user.isemployee == 1 and current_user.username == wurker:
            myaccount = True
        else:
            myaccount = False
        filelst = os.listdir('app/static/css/img/' + wurker)
        print(filelst)
        return render_template('employeefeed.html', lst = files,username = u.username, form= form, name=p.firstname, bio=u.bio, myaccount = myaccount, title = p.firstname)
    except:
        return redirect(url_for('genericerror'))

@myapp.route('/<wurker>/upload', methods = ['POST'])
def uploadphoto(wurker):
    filename1 = secure_filename(form.image.data.filename)
    print(filename1)
    return redirect(url_for('wurkerprofile'))

#Error Handlers

@myapp.route('/error')
def genericerror():
    return render_template('application-error.html', errormessage ='That page could not be found, please go home and try again!')
    
@myapp.errorhandler(404)
def page_not_found(e):
    return render_template('application-error.html', error = e, errormessage = "That page could not be found, please go home and try again!"), 404

@myapp.errorhandler(500)
def interror(e):
    return render_template('application-error.html', error=e, errormessage = 'Our database is currently undergoing maintance, please try again later!'), 500
