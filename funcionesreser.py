#coding=utf-8
""" Modulo que gestiona las reservas
"""
import conexion
import sqlite3
import variables
import funcioneshab
from datetime import datetime


def limpiarentry(fila):
    """
    limpia los distintos widgets del panel reservas
    :param fila: -- contiene un listado de widgets del panel reservas
    :return:
    """
    for i in range(len(fila)):
        fila[i].set_text('')
    for i in range(len(variables.menslabel)):
        variables.menslabel[i].set_text('')
    variables.cmbhab.set_active(-1)

def calculardias():
    """
    calcula el numero de dias que hay entre el check-in y el check-out
    :return:
    """
    diain = variables.filareserva[2].get_text()
    date_in = datetime.strptime(diain, '%d/%m/%Y').date()
    diaout = variables.filareserva[3].get_text()
    date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
    noches = (date_out-date_in).days
    if noches <= 0:
        variables.menslabel[2].set_text('Check-Out debe ser posterior')
        variables.reserva = 0
    else:
        variables.reserva = 1
        variables.menslabel[2].set_text(str(noches))

def insertares(fila):
    """
    Inserta una reserva en la base de datos
    :param fila: -- conjunto de atributos de reserva
    :return:
    """
    try:
        conexion.cur.execute('insert into  reservas(dni, numhab, checkin, checkout, noches) values(?,?,?,?,?)', fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadores():
    """
    visualiza en el treeview de reservas las reservas obtenidas del metodo listares
    :return:
    """
    try:
        variables.listado = listares()
        variables.listreservas.clear()
        for registro in variables.listado:
            variables.listreservas.append(registro)
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listares():
    """
    obtiene todas las instancias de reservas y las guarda en una lista
    :return: listado reservas
    """
    try:
        conexion.cur.execute('select codreser, dni, numhab, checkin, checkout, noches from reservas')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarapelcli(dni):
    """
    devuelve el apellido del cliente que le hemos pasado
    :param dni: -- valor del _Dni_cliente
    :return: apellido del cliente
    """
    try:
        conexion.cur.execute('select apel from clientes where dni = ?', (dni,))
        apel = conexion.cur.fetchone()
        conexion.conex.commit()
        return apel
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarpreciohabitacion(snumhab):
    """
    devuelve el precio de la habitacion que le hemos pasado
    :param snumhab: -- valor del _Numhab_habitacion
    :return: precio habitacion
    """
    try:
        conexion.cur.execute('select prezo from habitacion where numero = ?', (snumhab,))
        precio = conexion.cur.fetchone()
        conexion.conex.commit()
        return precio
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def buscarnomecli(dni):
    """
    devuelve el nombre del cliente que le hemos pasado
    :param dni: -- valor del _Dni_cliente
    :return: nombre del cliente
    """
    try:
        conexion.cur.execute('select nome from clientes where dni = ?', (dni,))
        apel = conexion.cur.fetchone()
        conexion.conex.commit()
        return apel
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajareserva(cod):
    """
    Elimina una reserva de la base de datos
    :param cod: -- valor del _Codigo_reserva
    :return:
    """
    try:
        print(cod)
        conexion.cur.execute('delete from reservas where codreser = ?', (cod,))
        conexion.conex.commit()
        if variables.switch.get_active():
            libre = 'SI'
        else:
            libre = 'NO'
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def versilibre(numhab):
    """
    comprueba si la habitacion esta libre o no
    :param numhab: -- valor del _Numhab_habitacion
    :return: booleano
    """
    try:
        conexion.cur.execute('select libre from habitacion where numero = ?', (numhab,))
        lista = conexion.cur.fetchone()
        conexion.conex.commit()
        if lista[0] == 'SI':
            return True
        else:
            return False
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifreserva(registro,codr):
    """
    Modifica los valores de los atributos de una reserva por los pasados en el conjunto de valores del registro
    :param registro: -- valores de los atributos de la reserva
    :param codr: -- valor del _Codigo_reserva
    :return:
    """
    try:
        conexion.cur.execute('update reservas set dni = ?, numhab = ?, checkin = ?, chekcout = ? where codreser = ?', (registro[0],registro[1],registro[2],registro[3],registro[4],codr))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
