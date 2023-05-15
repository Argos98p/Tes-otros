import os
from typing import Any
from dataclasses import dataclass
import json
import glob
import requests

@dataclass
class Recurso:
    usuarioId: str
    latitud: float
    longitud: float
    descripcion: str
    nombre: str
    categoria: str
    imagenes_directorio: str

    @staticmethod
    def from_dict(obj: Any) -> 'Recurso':
        _usuarioId = str(obj.get("usuarioId"))
        _latitud = float(obj.get("latitud"))
        _longitud = float(obj.get("longitud"))
        _descripcion = str(obj.get("descripcion"))
        _nombre = str(obj.get("nombre"))
        _categoria = str(obj.get("categoria"))
        _imagenes_directorio = str(obj.get("imagenes_directorio"))
        return Recurso(_usuarioId, _latitud, _longitud, _descripcion, _nombre, _categoria, _imagenes_directorio)
    


def images_in_directory(directoryPath):
    return glob.glob(directoryPath)
def send_request(recurso, imagesPaths,userId):
    payload = {   "usuarioId":userId,
    "latitud" : recurso.latitud,
    "longitud" : recurso.longitud,
    "descripcion": recurso.descripcion,
    "categoria" : recurso.categoria,
    "nombre" : recurso.nombre
    }

    files = []
    files.append(("recurso", (None, json.dumps(payload), 'application/json')))
    for image in imagesPaths:
        files.append(("files", (os.path.basename(image), open(image, 'rb'), 'application/octet-stream')))

    r = requests.post("http://0.0.0.0:8083/api/recurso/nuevo", files=files)
    print(r.content)


jsonFile = open('/home/argos98/Documentos/Tesis/Recursos/recursos.json')
jsonList = json.load(jsonFile)

for recursoStr in jsonList:
    
    recurso = Recurso.from_dict(recursoStr)
    imagenes_recurso = images_in_directory(recurso.imagenes_directorio+"/*")
    send_request(recurso=recurso,imagesPaths=imagenes_recurso,userId="3")
    

#recurso = Recurso.from_dict(jsonstring)
#print(recurso.categoria)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# recurso = Recurso.from_dict(jsonstring)