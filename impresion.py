#coding=utf-8
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, funcionescli, variables, funcionesser

""" Modulo que crea y gestiona la factura
"""

def basico():
    """
    Pone el logo, telefono, CIF, e-mail del hotel en las partes de arriba y abajo del documento y da nombre al archivo pdf
    :return:
    """
    try:
        global bill
        bill = canvas.Canvas('prueba.pdf', pagesize= A4)
        text1 = 'Bienvenido a nuestro hotel'
        text2 = 'CIF = 000000000A '
        bill.drawImage('./img/logohotel.png', 475, 670, width = 64, height = 64)
        bill.setFont('Helvetica-Bold', size = 16)
        bill.drawString(250, 780, 'HOTEL LITE')
        bill.setFont('Times-Italic', size=10)
        bill.drawString(240, 765, text1)
        bill.drawString(260, 755, text2)
        bill.line(50, 660, 540, 660)
        textpie = ('Hotel Lite, CIF = 000000000A Tlfo = 986000000 e-mail = info@hotelite.com')
        bill.setFont('Times-Italic', size=8)
        bill.drawString(170, 20, textpie)
        bill.line(50, 30, 540, 30)
    except:
        print('error en basico')


def factura(datosfactura,datosfactura2):
    """
    :param datosfactura: -- conjunto de valores obtenidos de varios entries y labels
    :param datosfactura2: -- conjunto de valores obtenidos de varios entries y labels
    :return:
    """
    try:
        iva = float(variables.fac[4].get_text())
        iva = iva + (iva*0.21)
        total2 = variables.fac[3].get_text()
        total = variables.fac[4].get_text()
        total = float(total) - float(total2)
        basico()
        listado = funcionesser.listafac2()
        bill.setTitle('FACTURA')
        bill.setFont('Helvetica-Bold', size=8)
        text3 = 'Numero de Factura: '
        bill.drawString(50, 735, text3)
        bill.setFont('Helvetica', size=8)
        bill.drawString(140, 735, str(datosfactura[0]))
        bill.setFont('Helvetica-Bold', size=8)
        text4 = 'Fecha factura:'
        bill.drawString(300, 735, text4)
        bill.setFont('Helvetica', size=8)
        bill.drawString(380, 735, str(datosfactura[4]))
        bill.setFont('Helvetica-Bold', size=8)
        text5 = 'DNI CLIENTE:'
        bill.drawString(50, 710, text5)
        bill.setFont('Helvetica', size=8)
        bill.drawString(120, 710, str(datosfactura[2]))
        bill.setFont('Helvetica-Bold', size=8)
        text6 = 'Nu de Habitacion:'
        bill.drawString(300, 710, text6)
        bill.setFont('Helvetica', size=8)
        bill.drawString(380, 710, str(datosfactura[3]))
        apelnome = funcionescli.apelnomefac(str(datosfactura[2]))
        print(apelnome)
        bill.setFont('Helvetica-Bold', size=8)
        text7 = 'APELLIDOS:'
        bill.drawString(50, 680, text7)
        bill.setFont('Helvetica', size=9)
        bill.drawString(120, 680, str(apelnome[0]))
        bill.setFont('Helvetica-Bold', size=8)
        text8 = 'NOMBRE:'
        bill.drawString(300, 680, text8)
        bill.setFont('Helvetica', size=9)
        bill.drawString(350, 680, str(apelnome[1]))
        bill.setFont('Helvetica-Bold', size=10)
        text9 = ['CONCEPTO', 'UNIDADES', 'PRECIO/UNIDAD', 'TOTAL']
        x = 75
        y = 85
        tipo = 605
        precio = 605
        for i in range(0, 4):
            bill.drawString(x, 645, text9[i])
            x += 130
        for a in range(0, 4):
            bill.drawString(y, 625, str(datosfactura2[a]))
            y += 130
        for tipon in listado:
            bill.drawString(85, tipo, str(tipon[0]))
            tipo -= 20
        for precion in listado:
            if precion[0] not in ("comida", "desayuno", "parking"):
                bill.drawString(475, precio, str(precion[1]))
            else:
                preciofac = float(precion[1]) * float(variables.fac[1].get_text())
                bill.drawString(475, precio, str(preciofac))
            precio -= 20
        bill.line(50, 100, 540, 100)
        bill.drawString(425, 70, "TOTAL:")
        bill.drawString(475, 70, variables.fac[4].get_text())
        bill.drawString(388, 50, "CON IVA (21%):")
        bill.drawString(475, 50, str(iva))
        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system('/usr/bin/xdg-open ' + dir + '/prueba.pdf')
    except:
        print('Error en modulo factura')