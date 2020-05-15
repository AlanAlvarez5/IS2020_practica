from model.model import Model
from controller.controller import Controller
m = Model()
c = Controller()
# YYYY-MM-DD HH:MM:SS

# m.c_sala(('10', '10'))
# m.c_pelicula(('Interestellar', 'Viaje al espacio.'))
# m.c_funcion((1,1,'2020-08-03 16:00:00', 50))

# print(m.c_compra((1,'2020-08-03 16:00:00',0)))

# print(m.c_compra_asiento((1,'A02',1)))

# print(m.select_all('funcion'))
# print(m.select_all('asiento'))
# m.delete('funcion', 1)

c.start()

# print(m.select_funcion_pelicula('Interestellar'))

# print(m.select_funcion_id_join(1))

# campos = ['nombre',  'correo', 'password', 'admin']

# first = True
# for c in reversed(campos):
#     if first:
#         fields = '`'+c+'`'
#         first = False
#     else:
#         fields = '`'+c+'`, ' + fields

# print(fields)

# from datetime import datetime

# today =  
# print(today)

# print(m.select_precio_id(1))

# print(m.select_all('compra'))

# print(m.select_compraid_ca(2))