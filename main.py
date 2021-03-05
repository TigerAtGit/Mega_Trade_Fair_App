from flask import Flask, render_template,request, url_for, redirect, flash
from servicesdb import servicesdb
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"

db = servicesdb()
# db.connect_database()
# db.create_table()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/add_venue',methods=['POST','GET'])
def add_venue():
    if request.method=='POST':
        table = 'Venue'
        city = request.form.get('city')
        address = request.form.get('address')
        country_id = request.form.get('country_id')
        state_id = request.form.get('state_id')
        db.add_record(table, {'City':city, 'Address':address, 'Country_id':country_id,'State_id':state_id})
        return render_template('add_venue.html',text='New venue created!')
    return render_template('add_venue.html')

@app.route('/add_event',methods=['POST','GET'])
def add_event():
    if request.method=='POST':
        table = 'Event'
        name = request.form.get('name')
        booking_date = request.form.get('booking_date')
        event_date = request.form.get('event_date')
        end_date = request.form.get('end_date')
        venue_id = request.form.get('venue_id')
        data = {'Name':name,'BookingStartDate':booking_date,'StartDate':event_date,'EndDate':end_date,'Venue_Id':venue_id}
        db.add_record(table, data)
        return render_template('add_event.html',text='New Event added!')
    return render_template('add_event.html')


@app.route('/add_visitor',methods=['POST','GET'])
def add_visitor():
    if request.method=='POST':
        table = 'Visitor'
       
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        address = request.form.get('address')
        pin = request.form.get('pin')
        phone = request.form.get('phone')
        email = request.form.get('email')
        DOB = request.form.get('DOB')
        gender = request.form.get('gender')
        data = {'FirstName':fname,'LastName':lname,'Address':address,'Pincode':pin,'MobileNo':phone,'EmailId':email,'DateOfBirth':DOB,'Gender':int(gender)}
        db.add_record(table, data)
        return render_template('add_visitor.html',text='New Visitor added!')
    return render_template('add_visitor.html')

@app.route('/add_exhibitor',methods=['POST','GET'])
def add_exhibitor():
    if request.method=='POST':
        table = 'Exhibitor' 
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company_name = request.form.get('company_name')
        company_description = request.form.get('company_description')
        address = request.form.get('address')
        pin = request.form.get('pin')
        industry_id = request.form.get('industry_id')
        country_id = request.form.get('country_id')
        state_id = request.form.get('state_id')
        data = {'ExhibitorName':name,'EmailId':email,'PhoneNo':phone,'CompanyName':company_name,'CompanyDescription':company_description,'Address':address,'Pincode':pin,'Industry_Id':industry_id,'Country_Id':country_id,'State_Id':state_id}
        db.add_record(table, data)
        return render_template('add_exhibitor.html',text='New Exhibitor added!')
    return render_template('add_exhibitor.html')


@app.route('/add_stall',methods=['POST','GET'])
def add_stall():
    if request.method=='POST':
        table = 'Stall'
        
        stall_no = request.form.get('stall_no')
        price = request.form.get('price')
        size = request.form.get('size')
        isbooked = request.form.get('isbooked')
        event_id = request.form.get('event_id')
        data = {'StallNo':stall_no,'Price':price,'StallSize':size,'IsBooked':int(isbooked),'Event_id':event_id}
        db.add_record(table, data)
        return render_template('add_stall.html',text='New Stall added!')
    return render_template('add_stall.html')


@app.route('/consumer_card',methods=['POST','GET'])
def consumer_card():
    if request.method=='POST':
        table = 'MegaConsumerCard' 
        spend = request.form.get('spend')
        spend_date = request.form.get('spend_date')
        payment_mode = request.form.get('payment_mode')
        event_id = request.form.get('event_id')
        booking_id = request.form.get('booking_id')
        visitor_id = request.form.get('visitor_id')
        data = {'Spend':spend,'SpendDate':spend_date,'PaymentMode':payment_mode,'Event_Id':event_id,'Booking_Id':booking_id,'Visitor_Id':visitor_id}
        db.add_record(table, data)
        return render_template('consumer_card.html',text='New Consumer data added!')
    return render_template('consumer_card.html')


@app.route('/add_country',methods=['POST','GET'])
def add_country():
    if request.method=='POST':
        table = 'Country'
        name = request.form.get('name')
        db.add_record(table, {'Country_name':name})
        return render_template('add_country.html',text='New Country added!')
    return render_template('add_country.html')


@app.route('/add_state',methods=['POST','GET'])
def add_state():
    if request.method=='POST':
        table = 'State'
        
        name = request.form.get('name')
        country_id = request.form.get('country_id')
        data = {'State_name':name,'Country_id':country_id}
        db.add_record(table, data)
        return render_template('add_state.html',text='New State added!')
    return render_template('add_state.html')


@app.route('/add_industry',methods=['POST','GET'])
def add_industry():
    if request.method=='POST':
        table = 'Industry'
      
        name = request.form.get('name')
        data = {'Industry_name':name}
        db.add_record(table, data)
        return render_template('add_industry.html',text='New Industry added!')
    return render_template('add_industry.html')


@app.route('/display/<title>')
def display(title):
    record = db.fetch_records(title)
    if title=='Venue':
        return render_template('display_venue.html',record=record)
    elif title=='Event':
        return render_template('display_event.html',record=record)
    elif title=='Stall':
        return render_template('display_stall.html',record=record)
    elif title=='Visitor':
        return render_template('display_visitor.html',record=record)
    elif title =='Exhibitor':
        return render_template('display_exhibitor.html',record=record)
    elif title=='megaconsumercard':
        return render_template('display_consumer_card.html',record=record)
    elif title=='Country':
        return render_template('display_country.html',record=record)
    elif title=='State':
        return render_template('display_state.html',record=record)
    else:
        return render_template('display_industry.html',record=record)


@app.route('/update/<title>/<int:ID>',methods=['GET'])
def update_get(title,ID):

    if title=='Venue':
        return render_template('update_venue.html', ID=ID)
    elif title=='Event':
        return render_template('update_event.html', ID=ID)
    elif title=='Stall':
        return render_template('update_stall.html', ID=ID)
    elif title=='Visitor':
        return render_template('update_visitor.html', ID=ID)
    elif title =='Exhibitor':
        return render_template('update_exhibitor.html', ID=ID)
    elif title=='ConsumerCard':
        return render_template('update_consumer_card.html', ID=ID)
    elif title=='Country':
        return render_template('update_country.html', ID=ID)
    elif title=='State':
        return render_template('update_state.html', ID=ID)
    else:
        return render_template('update_industry.html', ID=ID)

@app.route('/update/<title>',methods=['POST'])
def update(title):
    if title=='Venue':
        table = 'Venue'
        id = request.form.get('Id')
        city = request.form.get('city')
        address = request.form.get('address')
        country_id = request.form.get('country_id')
        state_id = request.form.get('state_id')
        db.update_record(table, id, {'City':city, 'Address':address, 'Country_id':country_id,'State_id':state_id})
        return render_template('update_venue.html',text='Following Venue updated!')
            
    elif title=='Event':
        table = 'Event'
        id = request.form.get('Id')
        name = request.form.get('name')
        booking_date = request.form.get('booking_date')
        event_date = request.form.get('event_date')
        end_date = request.form.get('end_date')
        venue_id = request.form.get('venue_id')
        data = {'Name':name,'BookingStartDate':booking_date,'StartDate':event_date,'EndDate':end_date,'Venue_Id':venue_id}
        db.update_record(table,id, data)
        return render_template('update_event.html',text='Following event updated!')

    elif title=='Stall':
        table = 'Stall'
        id = request.form.get('Id')
        stall_no = request.form.get('stall_no')
        price = request.form.get('price')
        size = request.form.get('size')
        isbooked = request.form.get('isbooked')
        event_id = request.form.get('event_id')
        data = {'StallNo':stall_no,'Price':price,'StallSize':size,'IsBooked':int(isbooked),'Event_id':event_id}
        db.update_record(table,id, data)
        return render_template('update_stall.html',text='Following stall updated!')
        
    elif title=='Visitor':
        table = 'Visitor'
        id = request.form.get('Id')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        address = request.form.get('address')
        pin = request.form.get('pin')
        phone = request.form.get('phone')
        email = request.form.get('email')
        DOB = request.form.get('DOB')
        gender = request.form.get('gender')
        data = {'FirstName':fname,'LastName':lname,'Address':address,'Pincode':pin,'MobileNo':phone,'EmailId':email,'DateOfBirth':DOB,'Gender':int(gender)}
        db.update_record(table,id, data)
        return render_template('update_visitor.html',text='Following visitor details updated!')

    elif title =='Exhibitor':
        table = 'Exhibitor' 
        id = request.form.get('Id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        company_name = request.form.get('company_name')
        company_description = request.form.get('company_description')
        address = request.form.get('address')
        pin = request.form.get('pin')
        industry_id = request.form.get('industry_id')
        country_id = request.form.get('country_id')
        state_id = request.form.get('state_id')
        data = {'Name':name,'EmailId':email,'PhoneNo':phone,'CompanyName':company_name,'CompanyDescription':company_description,'Address':address,'Pincode':pin,'Industry_Id':industry_id,'Country_Id':country_id,'State_Id':state_id}
        db.update_record(table,id, data)
        return render_template('update_exhibitor.html',text='Following Exhibitor details updated!')

    elif title=='ConsumerCard':
        table = 'MegaConsumerCard' 
        id = request.form.get('Id')
        spend = request.form.get('spend')
        spend_date = request.form.get('spend_date')
        payment_mode = request.form.get('payment_mode')
        event_id = request.form.get('event_id')
        booking_id = request.form.get('booking_id')
        visitor_id = request.form.get('visitor_id')
        data = {'Spend':spend,'SpendDate':spend_date,'PaymentMode':payment_mode,'Event_Id':event_id,'Booking_Id':booking_id,'Visitor_Id':visitor_id}
        db.update_record(table,id, data)
        return render_template('update_consumer_card.html',text='Consumer data updated!')
    elif title=='Country':
        table = 'Country'
        id = request.form.get('Id')
        name = request.form.get('name')
        db.update_record(table,id, {'Country_name':name})
        return render_template('update_country.html',text='Country details updated!')

    elif title=='State':
        table = 'State'
        Id = request.form.get('Id')
        name = request.form.get('name')
        country_id = request.form.get('country_id')
        data = {'State_name':name,'Country_id':country_id}
        db.update_record(table,Id, data)
        return render_template('update_state.html',text='State details updated!')

    elif title=='Industry':
        table = 'Industry'
        Id = request.form.get('Id')
        name = request.form.get('name')
        db.update_record(table,Id, {'Industry_name':name})
        return render_template('update_industry.html',text='Industry details updated!')
        
@app.route('/bookings')
def bookings():
    Events = db.fetch_column_data('Event', ['Id','Name'])
    Exhibitors = db.fetch_column_data('Exhibitor', ['Id','Name'])
    Stalls = db.fetch_column_data('stall', ['Id','StallNo','Event_Id'], condition_name='IsBooked', condition_value=0)
    # Events = [(1,'hi',), (2, 'Hello',)]
    # Exhibitors = [(1, 'Parth',), (2, 'Samved',)]
    # Stalls = [(1,)]
    return render_template('bookings.html', Events=Events, Exhibitors=Exhibitors, Stalls=Stalls)

@app.route('/add_booking', methods=['POST'])
def add_booking():
    Event_Id = request.form.get('event')
    Exhibitor_Id = request.form.get('exhibitor')
    Stall_Id = request.form.get('stall')
    TotalAmount = request.form.get('price')
    BookingDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    #print({'BookingDate': BookingDate, 'TotalAmount': TotalAmount, 'Event_Id': Event_Id, 'Exhibitor_Id': Exhibitor_Id})
    db.add_record('Booking', {'BookingDate': BookingDate, 'TotalAmount': TotalAmount, 'Event_Id': Event_Id, 'Exhibitor_Id': Exhibitor_Id})
    Booking_Id = db.get_last_insert_id()
    db.add_record('BookingStallMap', {'Booking_Id': Booking_Id, 'Event_Id': Event_Id, 'Stall_Id': Stall_Id})
    db.update_record('Stall', Id=Stall_Id, updated_data={'IsBooked': 1})
    flash('DONE')
    return redirect('/bookings')    


@app.route('/analytics',methods=['GET','POST'])
def analytics():
    options = db.fetch_column_data('Industry',['Id','Name'])
    if request.method=='POST':
        if request.form.get('analysis') == 'booking':
            return render_template('IndBooking.html', options=options)
        else:
            return render_template('IndBusiness.html', options=options)

    return render_template('analytics.html')


    

