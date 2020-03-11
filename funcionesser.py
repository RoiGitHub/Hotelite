#coding=utf-8
"""
Modulo que gestiona los servicios
"""
import conexion, sqlite3, variables, funcioneshab

def insertarserA(fila):
    """
    Inserta un servicio adicional en la base de datos
    :param fila: -- conjunto de atributos de servicio
    :return:
    """
    try:
        conexion.cur.execute('insert into servicios (codres,tipo,prezouni) values(?,?,?)', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajaserA(codser):
    """
    Elimina un servicio de la base de datos
    :param codser: valor del _Codser_Servicio
    :return:
    """
    try:
        conexion.cur.execute('delete from servicios where codser = ?', (codser,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoser():
    """
    visualiza en el treeview de servicios los servicios obtenidos del metodo listaser
    :return:
    """
    try:
        variables.listado = listaser()
        variables.listservicios.clear()
        for registro in variables.listado:
            variables.listservicios.append(registro)
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listaser():
    """
    obtiene todas las instancias de servicios y las guarda en una lista
    :return: return: listado servicios
    """
    try:
        codigoreserva = variables.mensfac[3].get_text()
        conexion.cur.execute('select * from servicios where codres = ?',(codigoreserva,))
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadofac():
    """
    visualiza en el treeview de facturas los servicios obtenidos del metodo listafac
    :return:
    """
    try:
        variables.listado = listafac()
        variables.listfacturas.clear()
        for registro in variables.listado:
            variables.listfacturas.append(registro)
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listafac():
    """
    obtiene todas las instancias de servicios de un determinado codigo de reserva y las guarda en una lista
    :return: listado de servicios
    """
    try:
        codigoreserva = variables.mensfac[3].get_text()
        print(codigoreserva)
        conexion.cur.execute('select * from servicios where codres = ?', (codigoreserva,))
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listafac2():
    """
    obtiene todas las instancias de servicios de un determinado codigo de reserva y las guarda en una lista
    :return: listado de servicios
    """
    try:
        codigoreserva = variables.mensfac[3].get_text()
        conexion.cur.execute('select tipo, prezouni from servicios where codres = ?', (codigoreserva,))
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def precios():
    """
    Modifica los precios por dia de parking, desayuno y estancia completa
    :return:
    """
    try:
        variables.labelprecios[0].set_text('5')
        variables.labelprecios[1].set_text('7')
        variables.labelprecios[2].set_text('10')
    except:
        print('error cargar precios')
