#coding=utf-8
""" Modulo que gestiona las habitaciones
"""

import conexion, sqlite3, variables

def insertarhab(fila):
    """
    Inserta una habitacion en la base de datos
    :param fila: -- conjunto de atributos de habitacion
    :return:
    """
    try:
        conexion.cur.execute('insert into habitacion(numero,tipo,prezo,libre) values(?,?,?,?)', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarhab():
    """
    obtiene todas las instancias de habitaciones y las guarda en una lista
    :return: listado habitaciones
    """
    try:
        conexion.cur.execute('select * from habitacion')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarentry(fila):
    """
    Limpia los widgets del panel de habitaciones
    :param fila: conjunto de widgets del panel habitaciones
    :return:
    """
    for i in range(len(fila)):
        fila[i].set_text('')

def listadohab(listhab):
    """
    visualiza en el treeview de habitaciones las habitaciones obtenidas del metodo listar
    :param listhab: listado de habitaciones
    :return:
    """
    try:
        variables.listado = listarhab()
        variables.listhab.clear()
        for registro in variables.listado:
            listhab.append(registro)
    except:
        print("error en cargar treeview de hab")


def bajahab(numhab):
    """
    Elimina una habitacion de la base de datos
    :param numhab: -- valor del _Numhab_habitacion
    :return:
    """
    try:
        conexion.cur.execute('delete from habitacion where numero = ?', (numhab,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def modifhab(registro, numhab):
    """
    Modifica los valores de los atributos de una habitacion por los pasados en el conjunto de valores del registro
    :param registro: -- valores de los atributos del cliente
    :param numhab: -- valor del _Numhab_habitacion
    :return:
    """
    try:
        conexion.cur.execute('update habitacion set tipo = ?, prezo = ?, libre = ? where numero = ?',
                             (registro[1], registro[0], registro[2], numhab))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadonumhab(self):
    """
    Obtiene un listado de todos los numeros de habitaciones de las habitaciones y los carga en un ComboBox
    :param self:
    :return:
    """
    try:
        conexion.cur.execute('select numero from habitacion')
        listado = conexion.cur.fetchall()
        variables.listcmbhab.clear()
        for row in listado:
            variables.listcmbhab.append(row)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def listadonumhabres():
    """
    Obtiene un listado de todos los numeros de habitaciones de las habitaciones
    :return: listado numeros de habitaciones
    """
    try:
        conexion.cur.execute('select numero from habitacion')
        lista = conexion.cur.fetchall()
        return lista
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def cambiaestadohab(libre, numhabres):
    """
    cambia el estado de una habitacion a SI o NO dependiendo de si se esta dando de alta o baja una reserva
    :param libre: -- valor del _Libre_habitacion
    :param numhabres: -- valor del _Numhab_habitacion
    :return:
    """
    try:
        print(libre)
        conexion.cur.execute('update habitacion set libre = ? where numero = ?',
                             (libre[0], numhabres))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
       print(e)
       conexion.conex.rollback()