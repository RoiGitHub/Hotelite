#coding=utf-8
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, funcionescli, variables, funcionesser

def listaclientes():

    try:
        global listadoclientes
        lista = funcionescli.listarimpresion()
        listadoclientes = canvas.Canvas('clientes.pdf', pagesize=A4)
        listadoclientes.setFont('Helvetica-Bold', size = 16)
        dni = 30
        apellidos = 240
        nombre = 500
        y = 800
        listadoclientes.drawString(dni,800,"DNI")
        listadoclientes.drawString(apellidos,800,"APELLIDOS")
        listadoclientes.drawString(nombre,800,"NOMBRE")
        listadoclientes.setFont('Helvetica', size=9)
        y = 785
        for cliente in lista:
            if y <= 50:
                listadoclientes.showPage()
                listadoclientes.setFont('Helvetica-Bold', size=16)
                listadoclientes.drawString(dni, 800, "DNI")
                listadoclientes.drawString(apellidos, 800, "APELLIDOS")
                listadoclientes.drawString(nombre, 800, "NOMBRE")
                listadoclientes.setFont('Helvetica', size=9)
                y = 785
            else:
                listadoclientes.drawString(dni, y, str(cliente[0]))
                listadoclientes.drawString(apellidos, y, str(cliente[1]))
                listadoclientes.drawString(nombre, y, str(cliente[2]))
                y = y - 15
        listadoclientes.save()
        dir = os.getcwd()
        os.system('/usr/bin/xdg-open ' + dir + '/clientes.pdf')
    except:
        print('ERROR AL GENERAR LISTA CLIENTES')