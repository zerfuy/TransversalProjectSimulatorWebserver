# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2019 Grey Li
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_ckeditor import CKEditor
import json
import psycopg2
import ctypes
import serial
import sys



app = Flask(__name__)
app.secret_key = 'dev key'

assets = Environment(app)
ckeditor = CKEditor(app)

css = Bundle('css/bootstrap.min.css',
             'css/bootstrap.css',
             'css/dropzone.min.css',
             'css/jquery.Jcrop.min.css',
             'css/style.css',
             'css/leaflet-routing-machine.css',
             'css/leaflet.css',
             filters='cssmin', output='gen/packed.css')

js = Bundle('js/jquery.min.js',
            'js/popper.min.js',
            'js/bootstrap.min.js',
            'js/bootstrap.js',
            'js/moment-with-locales.min.js',
            'js/dropzone.min.js',
            'js/jquery.Jcrop.min.js',
            'js/leaflet-routing-machine.js',
            'js/leaflet.js',
            filters='jsmin', output='gen/packed.js')

assets.register('js_all', js)
assets.register('css_all', css)



@app.route('/')
def index():
    json = []
    try:
        conn = psycopg2.connect(host="manny.db.elephantsql.com",
        database="juynhvrm",
        user="juynhvrm",
        password="H-FZ4Jrenwgd_c2Xzte7HLsYJzB_6q5D")

        # initialise all database info
        fire_table = {}
        fire_table["fire_id"] = "id"
        fire_table["fire_intensity"] = "intensity"
        fire_table["fire_table_name"] = "fire"

        cur = conn.cursor()

        # get fires info
        cur.execute("SELECT {0}, {1} from {2} order by {3} desc".format(
            fire_table["fire_id"],
            fire_table["fire_intensity"],
            fire_table["fire_table_name"],
            fire_table["fire_intensity"]))
        fires = cur.fetchmany(60)

        # format fire info
        
        for seq in fires:
            json.append(list(seq))

        if sys.platform.startswith('win'):
            SERIALPORT = "COM5"
        else:
            SERIALPORT = "/dev/ttyUSB0"

        ser = serial.Serial(
            port=SERIALPORT,
            baudrate=115200
        )

        ser.write((str(json) + "\n\r").replace(" ", "").replace("[[", "").replace("]]", "").replace("],[", ";").encode())
        ser.close()
        if cur is not None:
                cur.close()
    except Exception as e:
        print("BD error")
    except serial.SerialException:
        print("Serial {} port not available".format(SERIALPORT))

    return render_template('index.html', fires=json)
