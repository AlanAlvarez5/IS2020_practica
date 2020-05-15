from mysql import connector
from string import ascii_letters 


class Model:

    # --- Conexón a la base de datos
    def __init__(self, config_db_file='config.txt'):
        self.config_db_file = config_db_file
        self.config_db = self.read_config_db()
        self.connect_to_db()
    
    def read_config_db(self):
        d = {}
        with open(self.config_db_file) as f_r:
            for line in f_r:
                (key, val) = line.strip().split(':')
                d[key] = val
        return d
    
    def connect_to_db(self):
        self.cnx = connector.connect(**self.config_db)
        self.cursor = self.cnx.cursor(buffered=True)
    
    def close_db(self):
        self.cnx.close()

    #----------------------------------------------
    # Métodos Generales
    #----------------------------------------------

    # Seleccionar un elemento de cualquier tabla por id

    def sign_in(self, vals):
        try:
            sql = 'insert into usuario(`nombre`, `correo`, `password`, `admin`) values (%s, %s, %s, %s)'
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err

    def select_id(self, tabla, id):
        try:
            sql = 'select * from '+tabla+' where id = %s'
            vals = (id,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err

    # Seleccionar todos los elementos de una tabla

    def select_all(self, tabla):
        try:
            sql = 'select * from '+tabla
            self.cursor.execute(sql)
            record = self.cursor.fetchall()
            return record
        except connector.Error  as err:
            return err

    # Actualizar elementos de una tabla

    def update(self, tabla, campos, vals):
        try:
            sql = 'update '+tabla+' set '+','.join(campos)+ ' where id = %s'
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err

    # Eliminar elemento de una tabla por id

    def delete(self, tabla, id):
        try:
            sql = 'delete from '+tabla+' where id = %s'
            vals = (id,)
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err

    def create(self, tabla, vals):

        if tabla == 'usuario':
            campos = ['nombre',  'correo', 'password', 'admin']
        elif tabla == 'sala':
            campos = ['n_filas', 'n_asientos']
        elif tabla == 'pelicula':
            campos = ['nombre', 'descr']
        elif tabla == 'funcion':
            campos = ['id_pelicula', 'id_sala', 'fecha_hora', 'precio']
        elif tabla == 'compra':
            campos = ['id_usuario', 'fecha_hora', 'total' ]
        elif tabla == 'compra_asiento':
            campos = ['id_compra', 'id_asiento', 'id_funcion']
        
        first = True
        for c in reversed(campos):
            if first:
                fields = '`'+c+'`'
                first = False
            else:
                fields = '`'+c+'`, ' + fields

        first = True
        for _ in range(len(campos)):
            if first:
                first = False
                value = '%s'
            else:
                value = '%s, ' + value

        try:
            sql = 'insert into '+tabla+'('+fields+') values ('+value+')'
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err
    # --------------------------------------------
    # Métodos para el usuario
    # --------------------------------------------

    # Crear un usuario
    # Recibe tupla con valores
    # Sign in: admin = False
   
    def select_usuario_email(self, email):
        try:
            sql = 'select * from usuario where correo = %s'
            vals = (email,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err  

    # --------------------------------------------
    # Métodos para pelicula
    # --------------------------------------------

    def select_pelicula_nombre(self, nombre):
        try:
            sql = 'select * from pelicula where nombre = %s'
            vals = (nombre,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err

    # --------------------------------------------
    # Métodos para función
    # --------------------------------------------

    def c_funcion(self, vals):
        filas = list(ascii_letters)[26:]
        try:
            sql = 'insert into funcion (`id_pelicula`,`id_sala`, `fecha_hora`, `precio`) values (%s, %s, %s, %s)'
            self.cursor.execute(sql, vals)
            self.cnx.commit()
        except connector.Error as err:
            self.cnx.rollback()
            return err

        try:
            sql = 'select MAX(id) from funcion'
            self.cursor.execute(sql)
            id_funcion = self.cursor.fetchone()
        except connector.Error as err:
            return err
        
        sala = self.select_id('sala', vals[1])
        for i in range(sala[1]):
            for j in range(sala[2]):
                if j < 9:
                    self.c_asiento(filas[i]+'0'+str(j+1), id_funcion[0])
                else:
                    self.c_asiento(filas[i]+str(j+1), id_funcion[0])
        
        return True

    def select_all_funcion(self):
        try:
            sql = 'select funcion.id, pelicula.nombre, funcion.id_sala, funcion.fecha_hora, funcion.precio from funcion join pelicula on funcion.id_pelicula = pelicula.id'
            self.cursor.execute(sql)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    def select_funcion_id_join(self, id):
        try:
            sql = 'select funcion.id, pelicula.nombre, funcion.id_sala, funcion.fecha_hora, funcion.precio from funcion join pelicula on funcion.id_pelicula = pelicula.id where funcion.id = %s'
            val = (id,)
            self.cursor.execute(sql, val)
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err


    def select_funcion_dia(self, dia):
        try:
            fecha_1 = dia + ' 00:00:00'
            fecha_2 = dia + ' 23:59:59'
            sql = 'select id from funcion where fecha_hora >= %s AND fecha_hora < %s'
            vals = (fecha_1, fecha_2)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    def select_funcion_pelicula(self, pelicula):
        try:
            sql = 'select funcion.id, pelicula.nombre, funcion.id_sala, funcion.fecha_hora, funcion.precio from funcion join pelicula on funcion.id_pelicula = pelicula.id where pelicula.nombre = %s'
            vals = (pelicula,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    def select_precio_id(self, id):
        try:
            sql = 'select precio from funcion where id = %s'
            vals = (id,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchone()
            return record
        except connector.Error as err:
            return err
    # --------------------------------------------
    # Métodos para asientos
    # --------------------------------------------

    def c_asiento(self, id, id_funcion):
        try:
            sql = 'insert into asiento (`id`,`id_funcion`, `estado`) values (%s, %s, %s)'
            vals = (id, id_funcion, False)
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err

    def u_asiento(self, id_asiento, id_funcion, estado):
        try:
            sql = 'update asiento set estado = %s where id = %s and id_funcion = %s'
            vals = (estado, id_asiento, id_funcion)
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err

    def s_asientos_funcion(self, id_funcion):
        try:
            sql = 'select id, estado from asiento where id_funcion = %s'
            vals = (id_funcion,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    # --------------------------------------------
    # Métodos para compra
    # --------------------------------------------

    def c_compra(self, vals):
        try:
            sql = 'insert into compra (`id_usuario`, `fecha_hora`, `total`) values (%s, %s, %s)'
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err

    def u_total(self, val, id):
        try:
            sql = 'update compra set total = %s where id = %s'
            vals = (val, id)
            self.cursor.execute(sql, vals)
            self.cnx.commit()
            return True
        except connector.Error as err:
            self.cnx.rollback()
            return err
    
    def select_compra_id(self, id_usuario):
        try:
            sql = 'select * from compra where id_usuario = %s'
            vals = (id_usuario,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    # --------------------------------------------
    # Métodos para compra_asiento
    # --------------------------------------------
    

    def c_compra_asiento(self, vals):
        try:
            sql = 'insert into compra_asiento (`id_compra`, `id_asiento`, `id_funcion`) values (%s, %s, %s)'
            self.cursor.execute(sql, vals)
            self.cnx.commit()
        except connector.Error as err:
            self.cnx.rollback()
            return err

        self.u_asiento(vals[1], vals[2], True)

        return True

    def s_current_compra(self):
        try:
            sql = 'select MAX(id) from compra'
            self.cursor.execute(sql)
            id = self.cursor.fetchone()
            return id[0]
        except connector.Error as err:
            return err

    def select_ca_id(self, id):
        try:
            sql = 'select compra_asiento.id_asiento, compra_asiento.id_funcion from compra join compra_asiento on compra.id = compra_asiento.id_compra where compra.id = %s'
            vals = (id,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    def select_compraid_ca(self, id_compra):
        try:
            sql = 'select id_funcion from compra_asiento where id_compra = %s'
            vals = (id_compra,)
            self.cursor.execute(sql, vals)
            record = self.cursor.fetchall()
            return record
        except connector.Error as err:
            return err

    