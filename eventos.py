#coding=utf-8
import impresion
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import conexion, variables, funcionescli, funcioneshab, funcionesreser, funcionesvar, bigData, funcionesser, impresionclientes
import os, shutil
from datetime import *


class Eventos():

    # eventos generales
    def on_acercade_activate(self, widget):
        try:
            variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venacercade.show()
        except:
            print('error abrira acerca de')

    def on_btnCerrarabout_clicked(self, widget):
        try:
            variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venacercade.hide()
        except:
            print('error abrir calendario')

    def on_menuBarsalir_activate(self, widget):
        try:
            self.salir()
        except:
            print('salir en menubar')

    def salir(self):
        try:
            conexion.Conexion.cerrarbbdd(self)
            funcionesvar.cerrartimer()
            Gtk.main_quit()
        except:
            print('error funcion salir')

    def on_venPrincipal_destroy(self, widget):
        self.salir()

    def on_btnSalirtool_clicked(self, widget):
        variables.vendialogsalir.show()

    def on_btnCancelarsalir_clicked(self, widget):
        variables.vendialogsalir.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vendialogsalir.hide()

    def on_btnAceptarsalir_clicked(self, widget):
        self.salir()

    """
    Eventos Clientes
    """

    def on_btnAltacli_clicked(self, widget):
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if funcionescli.validoDNI(dni):
                funcionescli.insertarcli(registro)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                variables.menslabel[0].set_text('ERROR DNI')
        except:
            print("Error alta cliente")

    def on_btnBajacli_clicked(self, widget):
        try:
            dni = variables.filacli[0].get_text()
            if dni != '':
                funcionescli.bajacli(dni)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta dni u otro error')
        except:
            print("error en boton baja cliente")

    def on_btnModifcli_clicked(self, widget):
        try:
            cod = variables.menslabel[1].get_text()
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '':
                funcionescli.modifcli(registro, cod)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta el dni')
        except:
            print('error en boton modificar')

    # controla el valor del deni
    def on_entDni_focus_out_event(self, widget, dni):
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.validoDNI(dni):
                variables.menslabel[0].set_text('')
                pass
            else:
                variables.menslabel[0].set_text('ERROR')
        except:
            print("Error alta cliente en out focus")

    def on_treeClientes_cursor_changed(self, widget):
        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el numero que identifica a la fila que marcamos
            variables.menslabel[0].set_text('')
            funcionescli.limpiarentry(variables.filacli)
            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if sdata == None:
                    sdata = ''
                cod = funcionescli.selectcli(sdni)
                variables.menslabel[1].set_text(str(cod[0]))
                variables.filacli[0].set_text(str(sdni))
                variables.filacli[1].set_text(str(sapel))
                variables.filacli[2].set_text(str(snome))
                variables.filacli[3].set_text(str(sdata))
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel))
        except:
            print("error carga cliente")

    def on_btnCalendar_clicked(self, widget):
        try:
            variables.semaforo = 1
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()

        except:
            print('error abrir calendario')

    def on_btnCalendarResIn_clicked(self, widget):
        try:
            variables.semaforo = 2
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_btnCalendarResOut_clicked(self, widget):
        try:
            variables.semaforo = 3
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_Calendar_day_selected_double_click(self, widget):
        try:
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%02d/" % dia + "%02d/" % (mes + 1) + "%s" % agno
            if variables.semaforo == 1:
                variables.filacli[3].set_text(fecha)
            elif variables.semaforo == 2:
                variables.filareserva[2].set_text(fecha)
            elif variables.semaforo == 3:
                variables.filareserva[3].set_text(fecha)
                funcionesreser.calculardias()
            else:
                pass
            # variables.semaforo = 0
            variables.vencalendar.hide()
        except:
            print('error al coger la fecha')

    # Eventos de las habitaciones

    def on_btnAltahab_clicked(self, widget):
        try:
            numhab = variables.filahab[0].get_text()
            prezohab = variables.filahab[1].get_text()
            prezohab = prezohab.replace(',', '.')
            prezohab = float(prezohab)
            prezohab = round(prezohab, 2)
            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass

            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'
            registro = (numhab, tipo, prezohab, libre)
            if numhab != None:
                funcioneshab.insertarhab(registro)
                funcioneshab.listadohab(variables.listhab)
                funcioneshab.listadonumhab()
                funcioneshab.limpiarentry(variables.filahab)
            else:
                pass
        except:
            print("Error alta habitacion")

    def on_treeHab_cursor_changed(self, widget):
        try:
            model, iter = variables.treehab.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el numero que identifica a la fila que marcamos
            funcioneshab.limpiarentry(variables.filahab)
            if iter != None:
                snumhab = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprezo = model.get_value(iter, 2)
                sprezo = round(sprezo, 2)
                variables.filahab[0].set_text(str(snumhab))
                variables.filahab[1].set_text(str(sprezo))
                if stipo == str('simple'):
                    variables.filarbt[0].set_active(True)
                elif stipo == str('doble'):
                    variables.filarbt[1].set_active(True)
                elif stipo == str('family'):
                    variables.filarbt[2].set_active(True)
                slibre = model.get_value(iter, 3)
                if slibre == str('SI'):
                    variables.switch.set_active(True)
                else:
                    variables.switch.set_active(False)
        except:
            print("error carga habitacion")

    def on_btnBajahab_clicked(self, widget):
        try:
            numhab = variables.filahab[0].get_text()
            if numhab != '':
                funcioneshab.bajahab(numhab)
                funcioneshab.limpiarentry(variables.filahab)
                funcioneshab.listadohab(variables.listhab)
            else:
                pass
        except:
            print('borrar baja hab')

    def on_btnModifhab_clicked(self, widget):
        try:
            numhab = variables.filahab[0].get_text()
            prezo = variables.filahab[1].get_text()
            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'

            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass
            registro = (prezo, tipo, libre)
            if numhab != '':
                funcioneshab.modifhab(registro, numhab)
                funcioneshab.listadohab(variables.listhab)
                funcioneshab.limpiarentry(variables.filahab)
            else:
                print('falta el numhab')
        except:
            print('error modif hab')

    # eventos de los botones del toolbar
    def on_Panel_select_page(self, widget):
        try:
            funcioneshab.listadonumhab()
        except:
            print("error boton cliente barra herramientas")

    def on_btnClitool_clicked(self, widget):
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass
        except:
            print("error boton cliente barra herramientas")

    def on_btnReservatool_clicked(self, widget):
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
                funcioneshab.listadonumhab(self)
            else:
                pass
        except:
            print("error boton cliente barra herramientas")

    def on_btnHabita_clicked(self, widget):
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except:
            print("error boton habitacion barra herramientas")

    def on_btnCalc_clicked(self, widget):
        try:
            os.system('/snap/bin/gnome-calculator')
        except:
            print('error lanzar calculadora')

    def on_btnRefresh_clicked(self, widget):
        try:
            funcioneshab.limpiarentry(variables.filahab)
            funcionescli.limpiarentry(variables.filacli)
            funcionesreser.limpiarentry(variables.filareserva)
        except:
            print('error referes')

    def on_btnBackup_clicked(self, widget):
        try:
            variables.filechooserbackup.show()
            variables.neobackup = funcionesvar.backup()
            variables.neobackup = str(os.path.abspath(variables.neobackup))
            print(variables.neobackup)

        except:
            print('error abrir file choorse backup')

    def on_btnGrabarbackup_clicked(self, widget):
        try:
            destino = variables.filechooserbackup.get_filename()
            destino = destino + '/'
            variables.menslabel[3].set_text(str(destino))
            if shutil.move(str(variables.neobackup), str(destino)):
                variables.menslabel[3].set_text('Copia de Seguridad Creada')
        except:
            print('error dselect fichero')

    def on_btnCancelfilechooserbackup_clicked(self, widget):
        try:
            variables.filechooserbackup.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserbackup.hide()
        except:
            print('error cerrar file chooser')

    ## reservas

    def on_cmbNumres_changed(self, widget):
        try:
            index = variables.cmbhab.get_active()
            model = variables.cmbhab.get_model()
            item = model[index]
            variables.numhabres = item[0]
        except:
            print('error mostrar habitacion combo')

    def on_btnAltares_clicked(self, widget):
        try:
            if variables.reserva == 1:
                dnir = variables.menslabel[4].get_text()
                chki = variables.filareserva[2].get_text()
                chko = variables.filareserva[3].get_text()
                noches = int(variables.menslabel[2].get_text())
                registro = (dnir, variables.numhabres, chki, chko, noches)
                if funcionesreser.versilibre(variables.numhabres):
                    funcionesreser.insertares(registro)
                    funcionesreser.listadores()
                    # actualizar a NO
                    libre = ['NO']
                    funcioneshab.cambiaestadohab(libre, variables.numhabres)
                    funcioneshab.listadohab(variables.listhab)
                    funcioneshab.limpiarentry(variables.filahab)
                    funcionesreser.limpiarentry(variables.filareserva)
                else:
                    print('habitacion ocupada')
        except:
            print('error en alta res')

    def on_btnRefreshcmbhab_clicked(self, widget):
        try:
            variables.cmbhab.set_active(-1)
            funcioneshab.listadonumhab(self)
        except:
            print('error limpiar combo hotel')

    def on_treeReservas_cursor_changed(self, widget):
        try:
            totalfac = 0
            model, iter = variables.treereservas.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el numero que identifica a la columna que marcamos
            funcionesreser.limpiarentry(variables.filareserva)
            if iter != None:
                variables.codr = model.get_value(iter, 0)
                sdni = model.get_value(iter, 1)
                sapel = funcionesreser.buscarapelcli(str(sdni))
                snome = funcionesreser.buscarnomecli(str(sdni))
                snumhab = model.get_value(iter, 2)
                precio = funcionesreser.buscarpreciohabitacion(str(snumhab))
                lista = funcioneshab.listadonumhabres()
                m = -1
                for i, x in enumerate(lista):
                    if str(x[0]) == str(snumhab):
                        m = i
                variables.cmbhab.set_active(m)
                schki = model.get_value(iter, 3)
                schko = model.get_value(iter, 4)
                snoches = model.get_value(iter, 5)
                concepto = 'NOCHES'
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel[0]))
                variables.menslabel[2].set_text(str(snoches))
                variables.filareserva[2].set_text(str(schki))
                variables.filareserva[3].set_text(str(schko))
                variables.mensfac[0].set_text(str(sdni))
                variables.mensfac[1].set_text(str(sapel[0]))
                variables.mensfac[2].set_text(str(snome[0]))
                variables.mensfac[3].set_text(str(variables.codr))
                variables.mensfac[4].set_text(str(snumhab))
                variables.mensfac[5].set_text(str(schko))
                variables.fac[0].set_text(str(concepto))
                variables.fac[1].set_text(str(snoches))
                variables.fac[2].set_text(str(precio[0]))
                total = float(snoches) * float(precio[0])
                variables.fac[3].set_text(str(total))
                listado = funcionesser.listafac2()
                for preciofac in listado:
                    if preciofac[0] not in ("comida", "desayuno", "parking"):
                        totalfac = totalfac + float(preciofac[1])
                    else:
                        totalfac = totalfac  + (float(preciofac[1]) * float(snoches))
                totalisimo = float(totalfac) +  float(total)
                variables.fac[4].set_text(str(totalisimo))
                iva = totalisimo + (totalisimo * 0.21)
                variables.fac[5].set_text(str(iva))
                variables.labelser[0].set_text(str(variables.codr))
                variables.labelser[1].set_text(str(snumhab))
                funcionesser.listadofac()
                global datosfactura
                global datosfactura2
                datosfactura = (variables.codr, snoches, sdni, snumhab, schko)
                datosfactura2 = (concepto, snoches, precio[0], total)
        except:
            print('error cargar valores de reservas')

    def on_btnModifres_clicked(self, widget):
        try:
            dnir = variables.menslabel[4].get_text()
            chki = variables.filareserva[2].get_text()
            chko = variables.filareserva[3].get_text()
            noches = int(variables.menslabel[2].get_text())
            registro = (dnir, variables.numhabres, chki, chko, noches)
            funcionesreser.modifreserva(registro, variables.codr)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()
        except:
            print()

    def on_btnBajares_clicked(self, widget):
        try:
            funcionesreser.bajareserva(variables.codr)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()
            libre = ['SI']
            funcioneshab.cambiaestadohab(libre, variables.numhabres)
            funcioneshab.listadohab(variables.listhab)
        except:
            print('error baja reserva')

    # def on_btnBajares_clicked(self, widget):
    #     try:
    #         chko = variables.filareserva[3].get_text()
    #         today = date.today()
    #         print(chko)
    #
    #         hoy = datetime.strftime(today,'%d/%m/%Y')
    #         print(hoy)
    #         registro = (variables.numhabres)
    #         if str(hoy) == str(chko):
    #             funcioneshab.modifhabres(registro)
    #             funcioneshab.listadohab(variables.listhab)
    #         else:
    #             print('puede facturar')
    #             funcionesreser.bajareserva(variables.codr)
    #             funcionesreser.limpiarentry(variables.filareserva)
    #             funcionesreser.listadores()
    #             #cambiar el estado de la habitacion de ocupada a libre
    #
    #     except:
    #         print('error en checkout')

    def on_btnImprimir_clicked(self, widget):
        try:
            impresion.factura(datosfactura, datosfactura2)
            impresionclientes.listaclientes()
        except:
            print('error impresion')

    ## EVENTOS SERVICIOS

    def on_btnAltaSerB_clicked(self, widget):
        try:
            codres = variables.labelser[0].get_text()
            if variables.filarbtser[0].get_active():
                tipo = 'S/A'
                precio = "0"
            elif variables.filarbtser[1].get_active():
                tipo = 'desayuno'
                precio = variables.labelprecios[0].get_text()
            elif variables.filarbtser[2].get_active():
                tipo = 'comida'
                precio = variables.labelprecios[2].get_text()
            else:
                pass
            if variables.filarbtser[3].get_active():
                tipo = "parking"
                precio = variables.labelprecios[1].get_text()
            fila = (codres, tipo, precio)
            funcionesser.insertarserA(fila)
            funcionesser.listadoser()
            funcionesser.listadofac()
        except:
            print('error alta servicio')

    def on_btnAltaSerA_clicked(self, widget):
        try:
            codres = variables.labelser[0].get_text()
            tipo = variables.entser[0].get_text()
            precio = variables.entser[1].get_text()
            fila = (codres, tipo, precio)
            funcionesser.insertarserA(fila)
            funcionesser.listadoser()
            funcionesser.listadofac()
        except:
            print('error alta servicio')

    def on_btnBajaSer_clicked(self, widget):
        try:
            model, iter = variables.treeservicios.get_selection().get_selected()
            if iter != None:
                codser = model.get_value(iter, 0)
                funcionesser.bajaserA(codser)
                funcionesser.listadoser()
                funcionesser.listadofac()
        except:
            print('error baja servicio')

    def on_precios_activate(self, widget):
        try:
            variables.venprecios.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venprecios.show()
        except:
            print('error abrir precios')

    def on_btnPrecios_clicked(self, widget):
        try:
            preciodesayuno = variables.entprecios[0].get_text()
            precioparking = variables.entprecios[1].get_text()
            preciocomida = variables.entprecios[2].get_text()
            if preciodesayuno != "":
                variables.labelprecios[0].set_text(preciodesayuno)
            if precioparking != "":
                variables.labelprecios[1].set_text(precioparking)
            if preciocomida != "":
                variables.labelprecios[2].set_text(preciocomida)
        except:
            print('error actualizar precio')

    def on_btnSalirPrecios_clicked(self, widget):
        try:
            variables.venprecios.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venprecios.hide()
        except:
            print('error abrir calendario')

    def on_btnImprimi_clicked(self, widget):
        try:
            impresionclientes.listaclientes()
        except:
            print('ERROR IMPRIMIR CLIENTES')

    ## EVENTOS BIG DATA

    def on_menu_importar_activate(self, widget):
        bigData.importXls()

    def on_menu_exportar_activate(self, widget):
        bigData.exportXls()

    def on_menuBarbackup_activate(self, widget):
        pass
