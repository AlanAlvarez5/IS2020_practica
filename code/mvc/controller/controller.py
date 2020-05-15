from model.model import Model
from view.view import View
from datetime import datetime


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.logged = False

    def start(self):
        self.on = True

        while self.on:
            if self.logged:
                self.menu()
            else:
                self.menu_login()

    def menu_login(self):
        self.view.menu_login()
        self.view.opcion('3')
        o = input()
        if o == '1':
            self.login()
        elif o == '2':
            self.signin()
        elif o == '3':
            self.on = False
        else:
            self.view.opcion_incorrecta()

    def login(self):
        self.view.input('email')
        self.correo = input()
        self.view.input('contraseña')
        password = input()

        usuario = self.model.select_usuario_email(self.correo)
        if usuario:
            if usuario[3] == password:
                self.nombre = usuario[1]
                self.id_usuario = usuario[0]
                self.admin = usuario[4]
                self.logged = True
                self.view.msj('Bienvenido '+self.nombre)
                return
            else:
                self.email = ''
                self.view.msj('Email o contraseña incorrectos')

        else:
            self.view.err()
    
    def signin(self):
        self.view.input('nombre completo')
        nombre = input()
        self.view.input('correo electrónico')
        correo = input()
        self.view.input('contraseña')
        password = input()

        res = self.model.sign_in((nombre, correo, password, False))
        if res == True:
            self.view.msj('usuario '+ nombre+ ' creado')
            usuario = self.model.select_usuario_email(correo)
            self.correo = correo
            self.id_usuario = usuario[0]            
            self.nombre = usuario[1]
            self.admin = usuario[4]
            self.logged = True
            self.view.msj('Bienvenido '+self.nombre)
        else:
            self.view.err()

    # -------------------------
    # Métodos Generales
    # -------------------------

    def update_lists(self, fs, vs):
        fields = []
        vals = []
        for f,v in zip(fs, vs):
            if v != '':
                fields.append(f+' = %s')
                vals.append(v)
        return fields, vals
    
    def delete(self, tabla):
        self.view.input('ID del elemento a eliminar del registro '+tabla)
        id = input()
        res = self.model.delete(tabla,id)
        if res == True:
            self.view.msj('Elemento eliminado')
        else:
           self.view.err()

    def print_registros(self, tabla, registros = []):


        if tabla == 'pelicula':
            campos = ['ID', 'Nombre', 'Despcripción']
            if not registros:
                registros = self.model.select_all('pelicula')
        elif tabla == 'funcion':
            campos = ['ID', 'Pelicula', 'Sala', 'Fecha y Hora', 'Precio']
            if not registros:
                registros = self.model.select_all_funcion()
        elif tabla == 'sala':
            campos = ['Número', 'Número de filas', 'Número de asientos']
            if not registros:
                registros = self.model.select_all('sala')
        elif tabla == 'usuario':
            campos = ['ID', 'Nombre', 'Correo', 'Contraseña', 'Administrador']
            if not registros:
                registros = self.model.select_all('usuario')
        elif tabla == 'compra':
            campos = ['ID', 'ID de usuario', 'Fecha', 'Total']
            if not registros:
                registros = self.model.select_compra_id( self.id_usuario)
        


        if registros:
            for r in registros:
                self.view.msj('*************************')
                for c, v in zip(campos, r):
                    self.view.print_all(c,v)
                if tabla == 'compra':
                    asientos = self.model.select_ca_id(r[0])
                    a_vals = ['Asiento', 'Funcion']
                    print('* Asientos:')
                    for asiento in asientos:
                        for a, av in zip(asiento, a_vals):
                            print('\t'+str(av)+': '+str(a))
                        print('\n')                            

        else:
            self.view.msj('No existen registros de ' + tabla)

    def create(self, tabla):
        if tabla == 'funcion':
            campos = ['id de pelicula', 'número de sala', 'fecha y hora (YYYY-MM-DD HH:MM:SS)', 'precio de la entrada' ]
        elif tabla == 'pelicula':
            campos = ['nombre de la pelicula', 'descripción de la trama']
        elif tabla == 'sala':
            campos = ['número de filas', 'número de asientos por fila']
        elif tabla == 'usuario':
            campos = ['nombre completo', 'correo electrónico', 'contraseña', 'administrador (True o False)']

        vals = []
        for c in campos:
            self.view.input(c)
            vals.append(input())

        if tabla == 'usuario':
            if vals[-1] == 'True':
                vals[-1] = True
            else:
                vals[-1] = False

        if tabla == 'funcion':
            res = self.model.c_funcion(tuple(vals))
        else:
            res = self.model.create(tabla, tuple(vals))

        if res == True:
            self.view.msj('Nuevo '+tabla+' creado')
        else:
            self.view.err()


    def update(self, tabla):
        if tabla == 'funcion':
            campos = ['ID de la pelicula', 'ID de la sala', 'fecha y hora (YYYY-MM-DD HH:MM:SS)', 'precio de la entrada']
            fields = ['id_pelicula', 'id_sala', 'fecha_hora', 'precio']
        elif tabla == 'pelicula':
            campos = ['Nombre de la pelicula', 'Descripción de la trama']
            fields = ['nombre', 'descr']
        elif tabla == 'sala':
            campos = ['número de filas', 'número de asientos por fila']
            fields = ['n_filas', 'n_asientos']
        elif tabla == 'usuario':
            campos = ['nombre completo', 'correo electrónico', 'contraseña', 'administrador (True o False)']
            fields = ['nombre', 'correo', 'password', 'admin']


        self.view.input('ID de '+tabla+' a editar')
        id = input()

        registro = self.model.select_id(tabla, id)
        if registro:       
            vals = []
            i = 1
            self.view.msj('Ingresa los valores a modificar (Dejar vacio para no modificar)')
            for c in campos:
                self.view.input(c +'. Valor anterior: '+str(registro[i]))
                vals.append(input())
                i = i + 1
            
            if tabla == 'usuario':
                if vals[-1] == 'True':
                    vals[-1] = True
                else:
                    vals[-1] = False

            fields, vals = self.update_lists(fields, vals)

            vals.append(id)
            res = self.model.update(tabla, fields, tuple(vals))
            if res == True:
                self.view.msj( 'Elemento en '+tabla+' actualizado')
            else:
                self.view.err()
        else:
            self.view.err()
            self.view.msj(tabla + 'inexistente')
    # -------------------------
    # Menú principal
    # -------------------------

    def menu(self):
        self.view.menu(self.admin)
        if self.admin:
            self.view.opcion('6')
            op = input()
            if op == '1':
                self.menu_funcion()
            elif op == '2':
                self.menu_pelicula()
            elif op == '3':
                self.menu_sala()
            elif op == '4':
                self.menu_compra()
            elif op == '5':
                self.menu_usuario()
            elif op == '6':
                self.logged = False
                self.admin = False
                self.correo = ''
                self.nombre = ''
                self.id_usuario = 0
            else:
                self.view.opcion_incorrecta()

        else:
            self.view.opcion('6')
            op = input()
            if op == '1':
                self.print_registros('funcion')
            elif op == '2':
                self.select_funcion_day()
            elif op == '3':
                self.select_funcion_pelicula()
            elif op == '4':
                self.comprar_entrada()
            elif op == '5':
                self.print_registros('compra')
            elif op == '6':
                self.logged = False
                self.admin = False
                self.correo = ''
                self.nombre = ''
                self.id_usuario = 0
            else:
                self.view.opcion_incorrecta()

    # -------------------------
    # Métodos para funciones
    # -------------------------

    def menu_funcion(self):
        self.view.menu_funcion()
        self.view.opcion('7')
        op = input()
        if op == '1':
            self.create('funcion')
        elif op == '2':
            self.update('funcion')
        elif op == '3':
            self.print_registros('funcion')
        elif op == '4':
            self.select_funcion_day()
        elif op == '5':
            self.select_funcion_pelicula()
        elif op == '6':
            self.delete('funcion')
        elif op == '7':
            return

    def select_funcion_day(self):
        self.view.input('dia (YYYY-MM-DD)')
        dia = input()

        funciones_id = self.model.select_funcion_dia(dia)

        if funciones_id:
            funciones = []
            for id in funciones_id:
                funciones.append(self.model.select_funcion_id_join(id[0]))
            
            self.print_registros('funcion', funciones)
        else:
            self.view.msj('No hay registros de funciones')

    def select_funcion_pelicula(self):
        self.view.input('nombre de la pelicula')
        pelicula = input()

        funciones = self.model.select_funcion_pelicula(pelicula)
        if funciones:
            self.print_registros('funcion', funciones)
        else:
            self.view.msj('No existen funciones con esa pelicula')

    # -------------------------
    # Métodos para peliculas
    # -------------------------

    def menu_pelicula(self):
        self.view.menu_pelicula()
        self.view.opcion('5')
        op = input()
        if op == '1':
            self.create('pelicula')
        elif op == '2':
            self.update('pelicula')
        elif op == '3':
            self.print_registros('pelicula')
        elif op == '4':
            self.delete('pelicula')
        elif op == '5':
            return
        else:
            self.view.opcion_incorrecta()


    # -------------------------
    # Métodos para salas
    # -------------------------

    def menu_sala(self):
        self.view.menu_sala()
        self.view.opcion('4')
        op = input()
        if op == '1':
            self.create('sala')
        elif op == '2':
            self.update('sala')
        elif op == '3':
            self.print_registros('sala')
        elif op == '4':
            return
        else:
            self.view.opcion_incorrecta()

    # -------------------------
    # Métodos para usuarios
    # -------------------------

    def menu_usuario(self):
        self.view.menu_usuario()
        self.view.opcion('5')
        op = input()
        if op == '1':
            self.create('usuario')
        elif op == '2':
            self.update('usuario')
        elif op == '3':
            self.print_registros('usuario')
        elif op == '4':
            self.delete('usuario')
        elif op == '5':
            return
        else:
            self.view.opcion_incorrecta()


    # -------------------------
    # Métodos para compras
    # -------------------------
    def menu_compra(self):
        self.view.menu_compra()
        self.view.opcion('2')

        op = input()
        if op == '1':
            self.print_registros('compra')
        elif op == '2':
            return
        else:
            self.view.opcion_incorrecta()


    def comprar_entrada(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.model.c_compra((self.id_usuario, date, 0))

        id_compra = self.model.s_current_compra()
        
        count = 0
        while True:
            self.view.menu_boleto()
            self.view.opcion('2')
            op = input()
            if op == '1':
                self.compra_boleto(id_compra)
                count = count + 1
            elif op == '2':
                if count > 0:
                    break
                else:
                    self.view.msj('Debes de agregar al menos un boleto')
            else:
                self.view.opcion_incorrecta()

        boletos = self.model.select_compraid_ca(id_compra)
        total = 0
        for b in boletos:
            total = total + float(self.model.select_precio_id(b[0])[0])

        print('TOTAL ---' ,total)
        res = self.model.u_total(int(total), id_compra)
        if res == True:
            self.view.msj('Compra realizada con éxito')
        else:
            self.view.err()
        


    def compra_boleto(self, id_compra):
        self.view.input('ID de función')
        id_funcion = input()

        asientos = self.model.s_asientos_funcion( id_funcion)
        self.view.print_asientos(asientos)


        self.view.input('número de asiento')
        id_asiento = input()


        res = self.model.c_compra_asiento((id_compra, id_asiento, id_funcion ))
        if res == True:
            self.view.msj('Asiento añadido com éxito')
        else:
            self.view.err()





