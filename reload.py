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
clics = web_m[(noticiasf[i]+33):(noticiasf[i]+36)] 
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

print hora
print fecha
