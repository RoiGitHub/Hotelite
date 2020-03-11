#coding=utf-8
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk

import eventos, conexion, variables
import funcionescli, funcioneshab, funcionesreser,funcionesvar, funcionesser

'''
el main contiene los elementos necesarios para lanzar la aplicacion
asi como la declaracion de los widgets que se usaran. También los modulos
que tenemos que importar de las librerias graficas
'''

class Empresa:
    def __init__(self):
        #iniciamos la libreria Gtk
        self.b = Gtk.Builder()
        self.b.add_from_file('ventana.glade')

        #cargamos los widgets con algún evente asociado o que son referenciados
        vprincipal = self.b.get_object('venPrincipal')
        self.vendialog = self.b.get_object('venDialog')
        variables.venacercade = self.b.get_object('venAcercade')
        variables.venprecios = self.b.get_object('venPrecio')
        variables.panel = self.b.get_object('Panel')
        variables.filechooserbackup = self.b.get_object('fileChooserbackup')
        menubar = self.b.get_object('menuBar').get_style_context()

        #declaracion de wigdets
        entdni = self.b.get_object('entDni')
        entapel = self.b.get_object('entApel')
        entnome = self.b.get_object('entNome')
        entdatacli = self.b.get_object('entDatacli')
        lblerrdni = self.b.get_object('lblErrdni')
        lblcodcli = self.b.get_object('lblCodcli')
        lblnumnoches = self.b.get_object('lblNumnoches')
        lbldirbackup = self.b.get_object('lblFolderbackup')
        lbldnires = self.b.get_object('lblDnires')
        lblapelres = self.b.get_object('lblApelres')
        variables.vencalendar = self.b.get_object('venCalendar')
        variables.vendialogsalir = self.b.get_object('vendialogSalir')
        variables.calendar = self.b.get_object('Calendar')
        variables.filacli = (entdni, entapel, entnome, entdatacli)
        variables.listclientes = self.b.get_object('listClientes')
        variables.treereservas = self.b.get_object('treeReservas')
        variables.listreservas = self.b.get_object('listReservas')
        variables.listservicios = self.b.get_object('listSer')
        variables.listfacturas = self.b.get_object('listSerFac')
        variables.treeclientes = self.b.get_object('treeClientes')
        variables.menslabel = (lblerrdni, lblcodcli, lblnumnoches, lbldirbackup, lbldnires, lblapelres)


        #widgets habitaciones
        entnumhab = self.b.get_object('entNumhab')
        entprezohab = self.b.get_object('entPrezohab')
        rbtsimple = self.b.get_object('rbtSimple')
        rbtdoble = self.b.get_object('rbtDoble')
        rbtfamily = self.b.get_object('rbtFamily')
        variables.treehab = self.b.get_object('treeHab')
        variables.listhab = self.b.get_object('listHab')
        variables.filahab = (entnumhab, entprezohab)
        variables.filarbt = (rbtsimple, rbtdoble, rbtfamily)
        variables.listcmbhab = self.b.get_object('listcmbHab')
        variables.cmbhab = self.b.get_object('cmbNumres')
        variables.switch = self.b.get_object('switch')

        #widgtes reservas

        entdatain = self.b.get_object('entDatain')
        entdataout = self.b.get_object('entDataout')

        variables.filareserva = (entdni, entapel, entdatain, entdataout)


        #widgets factura
        lblfacdni = self.b.get_object('lblFacDNI')
        lblfacapel = self.b.get_object('lblFacApel')
        lblfacnome = self.b.get_object('lblFacNome')
        lblfaccod = self.b.get_object('lblFacCod')
        lblfachab = self.b.get_object('lblFacHab')
        lblfacfecha = self.b.get_object('lblFacFecha')
        lblfacconcepto = self.b.get_object('lblFacConcepto')
        lblfacunidades = self.b.get_object('lblFacUnidades')
        lblfacpreciouni = self.b.get_object('lblFacPrecioUnidad')
        lblfactotal = self.b.get_object('lblFacTotal')
        lblfactotalisimo = self.b.get_object('lblFacTotalisimo')
        lblfacdes = self.b.get_object('lblFacDes')
        lblfaccom = self.b.get_object('lblFacCom')
        lblfacpark = self.b.get_object('lblFacPark')
        lblfacotros = self.b.get_object('lblFacOtros')
        lblfaciva = self.b.get_object('lblFacIVA')
        variables.treeserviciosfac = self.b.get_object('treeFactura')

        variables.mensfac = (lblfacdni, lblfacapel, lblfacnome, lblfaccod, lblfachab, lblfacfecha)
        variables.fac = (lblfacconcepto, lblfacunidades, lblfacpreciouni, lblfactotal, lblfactotalisimo, lblfaciva)
        variables.lblfac = (lblfacdes, lblfaccom, lblfacpark, lblfacotros)

        #widgets servicios
        lblcodresser = self.b.get_object('lblCodResSer')
        lblhabser = self.b.get_object('lblHabSer')
        rbtSA = self.b.get_object('rbtSoloA')
        rbtdesayuno = self.b.get_object('rbtDesayuno')
        rbtcomida = self.b.get_object('rbtComida')
        chkparking = self.b.get_object('chkParking')
        enttiposer = self.b.get_object('entTipoSer')
        entprecioser = self.b.get_object('entPrecioSer')
        variables.treeservicios = self.b.get_object('treeSer')

        variables.labelser = (lblcodresser, lblhabser)
        variables.filarbtser = (rbtSA, rbtdesayuno, rbtcomida, chkparking)
        variables.entser = (enttiposer, entprecioser)

        #widgets precios
        lblpreciodesayuno = self.b.get_object('lblpreciodesayuno')
        lblprecioparking = self.b.get_object('lblprecioparking')
        lblpreciocomida = self.b.get_object('lblpreciocomida')
        entpreciodesayuno = self.b.get_object('entpreciodesayuno')
        entprecioparking = self.b.get_object('entprecioparking')
        entpreciocomida = self.b.get_object('entpreciocomida')

        variables.labelprecios = (lblpreciodesayuno, lblprecioparking, lblpreciocomida)
        variables.entprecios = (entpreciodesayuno, entprecioparking, entpreciocomida)


        #conectamos
        self.b.connect_signals(eventos.Eventos())

        vprincipal.show_all()
        vprincipal.maximize()
        conexion.Conexion().abrirbbdd()
        funcionesreser.listadores()
        funcionesser.listadoser()
        funcioneshab.listadonumhab(self)
        funcionescli.listadocli(variables.listclientes)
        funcioneshab.listadohab(variables.listhab)
        funcionesvar.controlhab()
        funcionesser.precios()


if __name__=='__main__':
    main = Empresa()
    Gtk.main()

