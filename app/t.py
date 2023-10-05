import os #Me permite trabajar con los archivos del OS
from config import connectionBD

refere=connectionBD()
refere.img = img.data.filename
file = img.data
file.save(os.path.abspath(os.getcwd() + '/app/templates/4BusosOver/' + refere.img))