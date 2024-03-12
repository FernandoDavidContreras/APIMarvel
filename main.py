import hashlib 
import requests as req
import time
from datetime import datetime
from pprint import pprint# podes usarla te recomiendo usarla para ver como esta la estructura pprint('aqui lo que te retorne una funcion')

url = f"http://gateway.marvel.com/v1/public/characters"
urlcomics = f"http://gateway.marvel.com/v1/public/comics"
urlpersonajes = f"http://gateway.marvel.com/v1/public/characters"
private_key = "d82d58686385b5490fc535829e9856c2da37fe7e"
public_key = "49034033b1faf7ef2b2535194286c4ee"
ts = time.time()

hash = hashlib.md5(f"{ts}{private_key}{public_key}".encode())

#funcion para mostrar todos los comics con los datos pedidos en el pdf(incluye id se puede usar para pasar como identificador al usar el boton de detalles)
#esta funcion si la podes usar es para el 1.1 del pdf
def get_comics():
  params = {
    'ts':ts,
    'apikey':public_key,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlcomics, params)
  data = response.json()['data']['results']
  lista = []

  for i in data:
    id = i['id']
    title = i['title']
    image = i['thumbnail']['path']+'.'+i['thumbnail']['extension']
    date = datetime.strptime(i['dates'][0]['date'], '%Y-%m-%dT%H:%M:%S-%f').strftime('%Y-%m')
    #id
    dic = {'id':id,'title':title,'image':image,'date':date,'details':''}
    lista.append(dic)
  return lista

#print(get_comics())

#funcion para buscar un dato en especifico(unicamente para parte del servidor no tocar plis JAJAJAJ)
def look_for_date_personajes(urlpersonaje):
  params = {
    'ts':ts,
    'apikey':public_key,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlpersonaje, params)
  data = response.json()['data']['results']
  name = data[0]['name']
  img = data[0]['thumbnail']['path']+'.'+data[0]['thumbnail']['extension']
  dic={'name':name,'image':img}
  return dic


#funcion para buscar un dato en especifico(unicamente para parte del servidor no tocar plis JAJAJAJ y no la llames no te servira de nada)
def look_for_date_autores(urlautor):
  params = {
    'ts':ts,
    'apikey':public_key,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlautor, params)
  data = response.json()['data']['results']
  name = data[0]['fullName']
  img = data[0]['thumbnail']['path']+'.'+data[0]['thumbnail']['extension']
  dic={'name':name,'image':img}
  return dic


#busca un comic en especifico (recomiendo usar cuando le den al boton de detalles solo pasar id)aqui esta todo para 1.2 del pdf proyecto
#esta funcion tambien la podes usar es
def look_for_comics(id):
  params = {
    'ts':ts,
    'apikey':public_key,
    'id':id,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlcomics, params)
  data = response.json()['data']['results']

  for i in data:
    id = i['id']
    title = i['title']
    isbn = i['isbn']
    description = i['description']
    personajes_date = i['characters']['items']
    personajesTotal = []
    for a in personajes_date:
      personajesTotal.append(look_for_date_personajes(a['resourceURI']))
    
    creadores_date = i['creators']['items']
    creadoresTotal = [] 
    for e in creadores_date:
      creadoresTotal.append(look_for_date_autores(e['resourceURI']))

    dic = {'id':id,'title':title,'ISBN':isbn,'description':description,'personajes':personajesTotal,'autores':creadoresTotal}
    return dic
  
#aqui un ejemplo para que mires como se usa la funcion y lo que regresa es una lista con los detalles en un objeto 
#look_for_comics(1590) asi se deberia de usar la funcion de detalles 1.2 pdf
#print(look_for_comics(21366)) #ejemplo

#funciones que te van a servir para la seccion 2 Area de personajes pdf 2.1
def get_personajes():
  params = {
    'ts':ts,
    'apikey':public_key,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlpersonajes, params)
  data = response.json()['data']['results']
  lista = []
  contador=0
  for i in data:
    contador+=1
    id = i['id']
    name = i['name']
    image = i['thumbnail']['path']+'.'+i['thumbnail']['extension']
    dic = {'id':id,'nombre':name,'image':image}
    lista.append(dic)
  return lista
#print(get_personajes())#podes ver el ejemplo

#funcion para la conexion
def get_comicsPersonaje(urlcomicsPerson):
  params = {
    'ts':ts,
    'apikey':public_key,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlcomicsPerson, params)
  data = response.json()['data']['results']
  id = data[0]['id']
  title = data[0]['title']
  img = data[0]['thumbnail']['path']+'.'+data[0]['thumbnail']['extension']
  dic = {'id':id,'title':title,'img':img,}
  return dic

#funcion para que la uses en el 2.2 pdf proyecto
#recomendacion podes hacer lo mismo que a la hora de mostrar los comics en el 1.1 en el boton de detalles podes pasar el id y listo pa
def get_personajesId(id): 
  params = {
    'ts':ts,
    'apikey':public_key,
    'id':id,
    'hash':hash.hexdigest(),
  }
  response = req.get(urlpersonajes, params)
  data = response.json()['data']['results']
  name = data[0]['name']
  image = data[0]['thumbnail']['path']+'.'+data[0]['thumbnail']['extension']
  description = data[0]['description']
  comicsPerson = data[0]['comics']['items']
  events_person = data[0]['events']['items']
  listevents = []
  listcomics = []
  for c in comicsPerson:
    listcomics.append(get_comicsPersonaje(c['resourceURI']))
  for z in events_person:
    listevents.append(get_comicsPersonaje(z['resourceURI']))
    
  dic = {'name':name,'image':image,'description':description,'list_comics':listcomics,'list_events':listevents} 
  return dic

#pprint(get_personajesId(1011334))
#get_personajesId(1011334)