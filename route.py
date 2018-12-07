#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,json
import re 

from pymongo import MongoClient
from flask import Flask, render_template, url_for
from flask import request
from beebotte import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)

def mediamongo():
    client = MongoClient('localhost', 27017)
    db = client.admin
    collection = db.valores
    cursor = collection.find()
    n = collection.find().count()
    media2 = 0
    i = 0
    for valors in cursor:
    	x = int(valors['meneos'])
    	media2 = x + media2
    	i += 1
    media = media2 / n
    client.close()
    return (media)

def mediabeebotte():
    bclient = BBT('q8uwUyqoZySTqG3gw6eRsjLT','ZNs82kRu26sMUv87g1JBI4TZrRBItKV4')
    numero_meneos = Resource(bclient, "Compu", "meneos")
    numero_meneos2 = numero_meneos.read(limit=100)

    media_ext = 0
    i = 0
    for valors in numero_meneos2:
         media_ext += float(valors["data"])
         i += 1
    mediab = (media_ext) / i
    return (int(mediab))
  

def umbralmongo(umbral, flag):
    umbral = umbral
    flag = flag 
    reload(sys)
    sys.setdefaultencoding('utf-8')
    client = MongoClient('localhost', 27017)
    db = client.admin
    collection = db.valores
    cursor = collection.find()
    n = collection.find().count()
    noticiameneostitulo = []
    noticiameneos = []
    noticiameneosfecha = []
    noticiameneoshora = []
    pruebaf = []
    umbraldb = ['','','','']
    carac = " Meneos="
    carac1 = " Fecha="
    carac2 = " Hora="
    global aux
    aux = 1
    for valors in cursor:
	x = float(valors['meneos'])
	if x > umbral:
              if aux == flag:
                  prueba = valors["titulo"]
                  prueba2 = valors["meneos"]
                  prueba3 = valors["fecha"]
                  prueba4 = valors["hora"]
                  pruebaf=(prueba +carac+prueba2 + carac1+prueba3 + carac2+prueba4)
              aux = aux + 1
    client.close()
   
    return (pruebaf)

def umbralmongo1(umbral, flag):
    umbral = umbral
    flag = flag 
    reload(sys)
    sys.setdefaultencoding('utf-8')
    client = MongoClient('localhost', 27017)
    db = client.admin
    collection = db.valores
    cursor = collection.find()
    n = collection.find().count()
    noticiameneostitulo = []
    noticiameneos = []
    noticiameneosfecha = []
    noticiameneoshora = []
    pruebaf = []
    umbraldb = ['','','','']
    carac = " Clics="
    carac1 = " Fecha="
    carac2 = " Hora="
    global aux
    aux = 1
    for valors in cursor:
	x = float(valors['clics'])
	if x > umbral:
              if aux == flag:
                  prueba = valors["titulo"]
                  prueba2 = valors["clics"]
                  prueba3 = valors["fecha"]
                  prueba4 = valors["hora"]
                  pruebaf=(prueba +carac+prueba2 + carac1+prueba3 + carac2+prueba4)
              aux = aux + 1
    client.close()
   
    return (pruebaf)
    

@app.route('/')
def home():
    global flag
    flag = 1
    web = urllib.urlopen("https://www.meneame.net/")   
    web_m = str(web.read())

    texto = "«" 
    lista = re.finditer(texto, web_m)
    texto_2 = "»"
    lista_2 = re.finditer(texto_2, web_m)
    noticiasi = ['']
    noticiasf = ['']
    noticiasc = ['']
    noticiasm = ['']
    for encontrado in lista:
        x = (encontrado.start())
        noticiasi.append(x)

    for listado in lista_2:
        y = (listado.end())
        noticiasf.append(y)

    texto_3= "clics"
    lista_3 = re.finditer(texto_3, web_m)
    for encontrada in lista_3:
        z = (encontrada.start())
        noticiasc.append(z)
       
    texto_4= "meneos"
    lista_4 = re.finditer(texto_4, web_m)
    for encontrada in lista_4:
        k = (encontrada.start())
        noticiasm.append(k)
          
    i = 1
    titulo = web_m[noticiasi[i]:noticiasf[i]]
    clics = web_m[(noticiasf[i]+33):(noticiasf[i]+35)] 
    meneos = web_m[(noticiasc[(2*i)+9]+9):(noticiasc[(2*i)+10]-1)]
    comentarios = web_m[(noticiasm[i]-8):(noticiasm[i]-5)]
    fecha = time.strftime("%x")
    hora = time.strftime("%X")

    ####### MONGO #######

    client = MongoClient('localhost', 27017)
    db = client.admin
    collection = db.valores

    users = client.admin.valores

    titulo_mongo = titulo
    clics_mongo = clics
    comentarios_mongo = comentarios
    meneos_mongo = meneos

    user = {
    'titulo' : titulo_mongo,
    'clics' : clics_mongo,
    'comentarios' : comentarios_mongo,
    'meneos' : meneos_mongo,
    'fecha' : fecha,
    'hora' : hora
    }

    result=users.insert_one(user)

    total = users.find().count()

    ###### BEEBOTTE ######
    bclient = BBT('q8uwUyqoZySTqG3gw6eRsjLT','ZNs82kRu26sMUv87g1JBI4TZrRBItKV4')

    numero_clics = Resource(bclient, "Compu", "clics")
    prueba_numero_clics = numero_clics.write(clics_mongo)

    numero_comentarios = Resource(bclient, "Compu", "comentarios")
    prueba_numero_comentarios  = numero_comentarios.write(comentarios_mongo)

    numero_meneos = Resource(bclient, "Compu", "meneos")
    prueba_numero_meneos= numero_meneos.write(meneos_mongo)

    numero_titulo = Resource(bclient, "Compu", "titulo")
    prueba_numero_titulo = numero_titulo.write(titulo_mongo)

    fechab = Resource(bclient, "Compu", "fecha")
    prueba_fecha = fechab.write(fecha)

    horab = Resource(bclient, "Compu", "hora")
    prueba_hora = horab.write(hora)

    return render_template('home.html', meneos = meneos_mongo, clics = clics_mongo, comentarios = comentarios_mongo, titulo = (titulo_mongo), fecha = fecha, hora = hora)

  
@app.route('/about', methods=['POST','GET'])
def about():
    global umbral
    global flag
    global aux
    if request.method == 'POST':
           if request.form['intr'] == 'Enviar':
                flag = 1
		umbral = float(request.form['dato'])
		noticias = umbralmongo(umbral, flag)
           elif request.form['intr'] == 'Next':
                flag = flag + 1
                noticias = umbralmongo(umbral,flag)
    else:
	    noticias = 0
    return render_template('about.html', valor=noticias, bandera = flag, umbrale = umbral)

@app.route('/about1', methods=['POST','GET'])
def about1():
    global umbral
    global flag
    global aux
    if request.method == 'POST':
           if request.form['intr'] == 'Enviar':
                flag = 1
		umbral = float(request.form['dato'])
		noticias = umbralmongo1(umbral, flag)
           elif request.form['intr'] == 'Next':
                flag = flag + 1
                noticias = umbralmongo1(umbral,flag)
    else:
	    noticias = 0
    return render_template('about1.html', valor=noticias, bandera = flag, umbrale = umbral)	

@app.route('/medio')
def medio():
    mediam = mediamongo()
    mediabe = mediabeebotte()

    return render_template('medio.html', media = mediam, mediab = mediabe)

@app.route('/extra')
def extra():
    return render_template('extra.html')
  
if __name__ == '__main__':
        global flag
        global umbral
        umbral = 0
        flag = 1
        app.debug = True
        app.run(host ='0.0.0.0', port=5000) 
     

