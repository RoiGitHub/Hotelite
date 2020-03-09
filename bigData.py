#coding=utf-8
from datetime import datetime

import xlrd
import xlwt

import conexion
import funcionescli
import variables

"""Modulo que gestiona las importacion y exportacion de datos

Este modulo contiene las funciones siguientes

importXls
Args:
    - ninguno
    importa una serie de datos de un documento excel a nuestra base de datos
    no devuelve nada

exportXls
Args:
    - ninguno
    exporta los datos de nuestra base de datos a un documento excel ya creado
    no devuelve nada

"""

def importXls():
    """
    importa los clientes que se encuentran en el documento listadoclientes.xlsx a nuestra base de datos
    :return:
    """
    try:
        fila = None
        # Abrimos el fichero excel
        document = xlrd.open_workbook("listadoclientes.xlsx")

        # Guarda cada una de las hojas y el numero indica la hoja
        clientes = document.sheet_by_index(0)

        cont = 0

        for i in range(clientes.nrows):
            if cont != 0:
                dni = clientes.cell_value(rowx=i, colx=0)
                apellidos = clientes.cell_value(rowx=i, colx=1)
                nombre = clientes.cell_value(rowx=i, colx=2)
                fechatabla = xlrd.xldate_as_datetime(clientes.cell_value(rowx=i, colx=3), document.datemode)
                fecha = datetime.date(fechatabla)

                fila = (str(dni), str(apellidos), str(nombre), str(fecha))

                if fila is not None:
                    conexion.cur.execute('insert into clientes (dni,apel,nome, data) values(?,?,?,?)', fila)
                    conexion.conex.commit()

                    funcionescli.listadocli(variables.listclientes)

            else:
                cont = 1


    except Exception as e:
        print("Error posible fallo ", e)


def exportXls():
    """
    exporta todos los clientes de nuestra base de datos en un nuevo documento llamado prueba.xls
    :return:
    """
    style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
    style1 = xlwt.easyxf("", num_format_str='DD-MM-YYYY')

    wb = xlwt.Workbook()

    ws = wb.add_sheet('NuevoClientes', cell_overwrite_ok=True)
    ws.write(0, 0, 'DNI', style0)
    ws.write(0, 1, 'APELLIDOS', style0)
    ws.write(0, 2, 'NOMBRE', style0)
    ws.write(0, 3, 'FECHA ALTA', style0)

    datos = funcionescli.listar()

    fila = 1
    for registro in datos:
        columna = 0
        cont = 0
        for dato in registro:
            if cont != 0:
                ws.write(fila, columna, dato, style1)
                columna = columna + 1
            cont = cont + 1
        fila = fila + 1

    wb.save('Prueba.xls')