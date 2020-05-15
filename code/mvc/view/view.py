class View:
    def end(self):
        print('\n ¡ Vuelva Pronto ! \n')

    def opcion(self, n):
        print('\n- Selecciona una opción (1 - '+n+'): ', end='\n\t> ')

    def opcion_incorrecta(self):
        print('\n¡¡ Opción Incorrecta !!')

    def input(self, campo):
        print('- Ingresa '+campo+': ', end='\n\t> ')

    def err(self):
        print('\n¡¡ Ha ocurrido un error !!')

    def msj(self, mensaje):
        print('\n*** '+mensaje+' ***')

    def print_all(self, campo, valor):
        print('* '+ campo+ ': '+ str(valor))

    def menu_login(self):
        print('\n\t---- CINEMA ----')
        print('\n 1.- Inicia Sesión')
        print(' 2.- Resgistrate')
        print(' 3.- Salir')

    def menu(self, admin):
        print('\n\t---- MENU PRINCIPAL ----\n')
        if admin:
            print(' 1. Funciones')
            print(' 2. Peliculas')
            print(' 3. Salas')
            print(' 4. Compras')
            print(' 5. Usuarios')
            print(' 6. Salir')
        else:
            print(' 1. Ver todas las funciones')
            print(' 2. Ver funciones de un día')
            print(' 3. Ver funciones de una pelicula')
            print(' 4. Comprar Entrada')
            print(' 5. Ver mis compras')
            print(' 6. Salir')

    def menu_funcion(self):
        print('\n\t---- Funciones ----')
        print(' 1. Crear nueva funcion')
        print(' 2. Editar funcion')
        print(' 3. Ver todas las funciones')
        print(' 4. Ver funciones de un día')
        print(' 5. Ver funciones de una pelicula')
        print(' 6. Eliminar funcion')
        print(' 7. Salir')

    def menu_pelicula(self):
        print('\n\t---- Peliculas ----')
        print(' 1. Crear nueva pelicula')
        print(' 2. Editar pelicula')
        print(' 3. Ver todas las peliculas')
        print(' 4. Eliminar pelicula')
        print(' 5. Salir')

    def menu_sala(self):
        print('\n\t---- Salas ----')
        print(' 1. Crear nueva sala')
        print(' 2. Editar sala')
        print(' 3. Ver todas las salas')
        print(' 4. Salir')

    def menu_usuario(self):
        print('\n\t---- Usuarios ----')
        print(' 1. Crear nuevo usuario')
        print(' 2. Editar usuario')
        print(' 3. Ver todos los usuarios')
        print(' 4. Eliminar usuario')
        print(' 5. Salir')

    def menu_compra(self):
        print('\n\t---- Compras ----')
        print(' 1. Ver todas las compras')
        print(' 2. Salir')

    def menu_boleto(self):
        print('\n\t---- Boletos ----')
        print(' 1. Agregar Boleto')
        print(' 2. Terminar')


    def print_asientos(self, asientos):

        fila_vieja = 'A'
        print('\n---- Guia de Asientos ----\n')
        print('\n------------------ Pantalla ---------------\n')
        for a in asientos:
            id_asiento = a[0]
            estado = a[1]
            fila = id_asiento[0]
            if fila_vieja != fila:
                print('\n')
                fila_vieja = fila
            if estado:
                print('(---)', end=' ')
            else:
                print('('+id_asiento+')', end=' ')
            
        print('\n\n---- Guia de Asientos ----\n')