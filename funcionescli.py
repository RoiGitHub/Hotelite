#coding=utf-8
""" Modulo que gestiona los clientes
"""

import conexion
import sqlite3
import variables

def limpiarentry(fila):
    '''
    limpia los widgets del panel clientes
    :param fila: -- conjunto de widgets del panel clientes
    :return:
    '''

    variables.menslabel[1].set_text('')
    for i in range(len(fila)):
        fila[i].set_text('')

def validoDNI(dni):
    '''
    Controlo que el dni sea correcto
    :param dni: -- valor del _Dni_cliente
    :return: booleano
    '''
    try:
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"   #letras del dni, es estandar
        dig_ext = "XYZ"
        #tabla letras extranjeroreemp_
        reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
        numeros = "1234567890"
        dni = dni.upper()
        if len(dni) == 9: #el dni debe tener 9 caracteres
            dig_control = dni[8]
            dni = dni[:8]                                          #el número que son los 8 primeros
            if dni[0] in dig_ext:
                print(dni)
                dni = dni.replace(dni[0],reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control
        return False
    except:
        print("Error")
        return None

def insertarcli(fila):
    '''
    Inserta un cliente en la base de datos
    :param fila: -- conjunto de atributos de cliente
    :return:
    '''
    try:
        conexion.cur.execute('insert into  clientes(dni, apel, nome, data) values(?,?,?,?)',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    """
    obtiene todas las instancias de clientes y las guarda en una lista
    :return: listado clientes
    """
    try:
        conexion.cur.execute('select * from clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarimpresion():
    """
    obtiene un listado con todos los dni, nombre y apellidos de los clientes
    :return:
    """
    try:
        conexion.cur.execute('select dni, apel, nome from clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajacli(dni):
    """
    Elimina a un cliente de la base de datos
    :param dni: -- valor del _Dni_cliente
    :return:
    """
    try:
        conexion.cur.execute('delete from clientes where dni = ?', (dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifcli(registro, cod):
    """
    Modifica los valores de los atributos de un cliente por los pasados en el conjunto de valores del registro
    :param registro: -- nuevos valores de los atributos del cliente
    :param cod: -- valor del _Id_cliente
    :return:
    """
    try:
        conexion.cur.execute('update clientes set dni = ?, apel= ?, nome = ?, data = ? where id = ?',
                             (registro[0], registro[1], registro[2], registro[3], cod))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadocli(listclientes):
    """
    visualiza en el treeview de clientes los clientes obtenidos del metodo listar
    :param listclientes: -- lista del panel de clientes
    :return:
    """
    try:
        variables.listado = listar()
        listclientes.clear()
        for registro in variables.listado:
            listclientes.append(registro[1:5])
    except:
        print("error en cargar treeview")


def selectcli(dni):
    """
    Obtiene el id del cliente que le pasamos
    :param dni: -- valor del _Dni_cliente
    :return: id del cliente
    """
    try:
        conexion.cur.execute('select id from clientes where dni = ?', (dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def apelnomefac(dni):
    """
    Devuelve el nombre y apellidos del cliente que le pasamos
    :param dni: -- valor del _Id_cliente
    :return: nombre y apellidos
    """
    try:
        conexion.cur.execute('select apel, nome from clientes where dni = ?', (dni,))
        apelnome = conexion.cur.fetchone()
        conexion.conex.commit()
        return apelnome
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


