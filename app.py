from flask import Flask, render_template
import time
from sense_hat import SenseHat
import datetime
import mysql.connector




app = Flask(__name__)
@app.route('/')
def index():
    sense=SenseHat()
    temp = round(sense.get_temperature(), 1)
    kosteus = round (sense.get_humidity(), 1)
    paine = round (sense.get_pressure(), 1)
    currentDT = datetime.datetime.now()
    date = currentDT.strftime("%Y-%m-%d")
    clock = currentDT.strftime("%H:%M:%S")
    huono = 'Bad value!'
    hyvä = 'Good value!'
    heading = sense.get_compass()
    pohjoinen= 'North'
    east = 'East'
    south = 'South'
    west = 'West'
    mydb =mysql.connector.connect(host="localhost", user="root", passwd="salasana123",
                                  database="sensehat")
    mycursor =mydb.cursor()
    
    sqlform = "Insert into luvut(pvm,clock,temperature,humidity,pressure) values(%s, %s, %s, %s, %s)"

    sql = [(date, clock, temp, kosteus, paine) ]


    mycursor.executemany(sqlform, sql)
    mydb.commit()
    
    mycursor.execute("SELECT ROUND(AVG(temperature),2) FROM luvut WHERE pvm=CURDATE()")

    mytemp = mycursor.fetchall()

    mycursor.execute("SELECT ROUND(AVG(pressure),2) FROM luvut WHERE pvm=CURDATE()")

    mypres = mycursor.fetchall()

    mycursor.execute("SELECT ROUND(AVG(humidity),2) FROM luvut WHERE pvm=CURDATE()")

    myhum = mycursor.fetchall()
    
    mycursor.execute("SELECT ROUND(AVG(temperature),2) FROM luvut WHERE pvm=CURDATE()- INTERVAL 1 DAY")

    yetemp = mycursor.fetchall()

    mycursor.execute("SELECT ROUND(AVG(pressure),2) FROM luvut WHERE pvm=CURDATE()- INTERVAL 1 DAY")

    yepres = mycursor.fetchall()

    mycursor.execute("SELECT ROUND(AVG(humidity),2) FROM luvut WHERE pvm=CURDATE() - INTERVAL 1 DAY")

    yehum = mycursor.fetchall()
    
    mycursor.execute("SELECT ROUND(AVG(temperature),2) FROM luvut WHERE pvm=CURDATE()- INTERVAL 2 DAY")

    twotemp = mycursor.fetchall()

    mycursor.execute("SELECT ROUND(AVG(pressure),2) FROM luvut WHERE pvm=CURDATE()- INTERVAL 2 DAY")

    twopres = mycursor.fetchall()

    mycursor.execute("SELECT ROUND(AVG(humidity),2) FROM luvut WHERE pvm=CURDATE() - INTERVAL 2 DAY")

    twohum = mycursor.fetchall()

    
    if temp <= 16:
            arvo=huono
    else:   
        if temp>= 17:
            arvo=hyvä
    
    if kosteus <= 22:
            kostarvo=hyvä
    else:    
        if kosteus >= 23:
            kostarvo=huono
    if paine <= 1010:
            painearvo=hyvä
    else:
        if paine >= 1011:
            painearvo=huono

    
    if heading < 45 or heading > 315:
            ilmansuunta=pohjoinen
    elif heading < 135:
            ilmansuunta= east
    elif heading < 225:
            ilmansuunta = south
    else:
            ilmansuunta = west
            
    return render_template('index.html', temp=temp, kosteus=kosteus, paine=paine, date=date,
                        clock = clock, mytemp=mytemp, myhum=myhum, mypres=mypres,
                        yetemp=yetemp, yehum=yehum, yepres=yepres, arvo=arvo,
                        painearvo=painearvo, kostarvo=kostarvo, ilmansuunta = ilmansuunta,
                        twotemp=twotemp, twohum=twohum, twopres=twopres)
           


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.143')
    
