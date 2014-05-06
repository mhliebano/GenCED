# -*- coding: utf-8 -*-
import webkit
import gtk
import os
import pango
import re
ruta=os.path.expanduser("~")+"/GenCED/"

class Ventana:

    def __init__(self):
        #La ventana
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Generador de CED")
        self.window.maximize()
        self.window.set_resizable(False)
        self.window.set_icon_from_file(ruta+'iconos/iconoApp.png')
        color = gtk.gdk.color_parse('#ffffff')
        self.window.modify_bg(gtk.STATE_NORMAL, color)
        self.window.connect("delete_event",self.salir) 
        self.window.connect("destroy",self.destroy)
               
        #contenedor
        tabla=gtk.Table(100,100,False)
               
        #El Menu
        menu = gtk.MenuBar()
        menuArchivo = gtk.Menu()
        menuEditar = gtk.Menu()
        menuProyecto=gtk.Menu()
        
        menuA = gtk.MenuItem("Archivo")
        menuE = gtk.MenuItem("Editar")
        menuP = gtk.MenuItem("Proyecto")
        menuH = gtk.MenuItem("Herramientas")
        menuL = gtk.MenuItem("Aplicacion")
        menuY = gtk.MenuItem("Ayuda")
        
        #El menu archivo
        menuA.set_submenu(menuArchivo)
        self.nue = gtk.MenuItem("Nuevo Proyecto")
        self.abr = gtk.MenuItem("Abrir Proyecto")
        self.gua = gtk.MenuItem("Guardar Proyecto")
        self.gua.set_sensitive(False)
        self.guc = gtk.MenuItem("Guardar Proyecto Como...")
        self.guc.set_sensitive(False)
        self.cer=gtk.MenuItem("Cerrar Proyecto")
        self.cer.set_sensitive(False)
        self.sep = gtk.SeparatorMenuItem()
        self.sal = gtk.MenuItem("Salir")
        
        menuArchivo.append(self.nue)
        menuArchivo.append(self.abr)
        menuArchivo.append(self.gua)
        menuArchivo.append(self.guc)
        menuArchivo.append(self.cer)
        menuArchivo.append(self.sep)
        menuArchivo.append(self.sal)
        
        #el menu edicion
        menuE.set_submenu(menuEditar)
        self.inHoja=gtk.MenuItem("Insertar Hoja")
        self.inImagen=gtk.MenuItem("Insertar Imagen")
        self.inSonido=gtk.MenuItem("Insertar Sonido")
        self.inVideo=gtk.MenuItem("Insertar Video")
        self.inArchivo=gtk.MenuItem("Insertar Archivo")
        self.sepEd1 = gtk.SeparatorMenuItem()
        self.cop=gtk.MenuItem("Copiar Objeto")
        self.peg=gtk.MenuItem("Pegar Objeto")
        self.elm=gtk.MenuItem("Eliminar Objeto")
        menuEditar.append(self.inHoja)
        menuEditar.append(self.inImagen)
        menuEditar.append(self.inSonido)
        menuEditar.append(self.inVideo)
        menuEditar.append(self.inArchivo)
        menuEditar.append(self.sepEd1)
        menuEditar.append(self.cop)
        menuEditar.append(self.peg)
        menuEditar.append(self.elm)
        
        #el Menu proyecto
        menuP.set_submenu(menuProyecto)
        self.eje=gtk.MenuItem("Ejecutar")
        self.verHtml=gtk.MenuItem("Ver Codigo Fuente")
        menuProyecto.append(self.eje)
        menuProyecto.append(self.verHtml)
        
        menu.append(menuA)
        menu.append(menuE)
        menu.append(menuP)
        menu.append(menuH)
        menu.append(menuL)
        menu.append(menuY)
        
        #La barra de herramientas
        self.barra = gtk.Toolbar()
        self.barra.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.barra.set_style(gtk.TOOLBAR_ICONS)
        self.barra.set_border_width(5)
        self.barra.set_tooltips(True)
        tooltips=gtk.Tooltips()
        #Botones estandar
        #icono=gtk.image_new_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size('iconos/proyecto.png', 25, 25))
        icoNue=gtk.Image()
        icoNue.set_from_file(ruta+'iconos/proyecto.png')
        self.barraNue = gtk.ToolButton(icoNue)
        self.barraNue.set_tooltip(tooltips,"Nuevo Proyecto")

        icoAbr=gtk.Image()
        icoAbr.set_from_file(ruta+'iconos/abrir.png')
        self.barraAbr = gtk.ToolButton(icoAbr)
        self.barraAbr.set_tooltip(tooltips,"Abrir Proyecto")
        
        icoGua=gtk.Image()
        icoGua.set_from_file(ruta+'iconos/guardar.png')
        self.barraGua = gtk.ToolButton(icoGua)
        self.barraGua.set_tooltip(tooltips,"Guardar Proyecto")
        self.barraGua.set_sensitive(False)
        
        icoGuc=gtk.Image()
        icoGuc.set_from_file(ruta+'iconos/guardarc.png')
        self.barraGuc = gtk.ToolButton(icoGuc)
        self.barraGuc.set_tooltip(tooltips,"Guardar Proyecto Como")
        self.barraGuc.set_sensitive(False)
        
        self.sep = gtk.SeparatorToolItem()
        icoSal=gtk.Image()
        icoSal.set_from_file(ruta+'iconos/salir.png')
        self.quittb = gtk.ToolButton(icoSal)
        
        #botones de recursos
        self.sep2 = gtk.SeparatorToolItem()
        icoHoj=gtk.Image()
        icoHoj.set_from_file(ruta+'iconos/hoja.png')
        self.barraHojaNueva=gtk.ToolButton(icoHoj)
        self.barraHojaNueva.set_tooltip(tooltips,"Insertar Nueva Hoja")
        self.barraHojaNueva.set_sensitive(False)
        
        icoImg=gtk.Image()
        icoImg.set_from_file(ruta+'iconos/imagen.png')
        self.barraImagenNuevo=gtk.ToolButton(icoImg)
        self.barraImagenNuevo.set_tooltip(tooltips,"Insertar Nueva Imagen")
        self.barraImagenNuevo.set_sensitive(False)
        
        icoSon=gtk.Image()
        icoSon.set_from_file(ruta+'iconos/sonido.png')
        self.barraSonidoNuevo=gtk.ToolButton(icoSon)
        self.barraSonidoNuevo.set_tooltip(tooltips,"Insertar Nuevo Sonido")
        self.barraSonidoNuevo.set_sensitive(False)
        
        icoVid=gtk.Image()
        icoVid.set_from_file(ruta+'iconos/video.png')
        self.barraVideoNuevo=gtk.ToolButton(icoVid)
        self.barraVideoNuevo.set_tooltip(tooltips,"Insertar Nuevo Video")
        self.barraVideoNuevo.set_sensitive(False)
        
        icoArc=gtk.Image()
        icoArc.set_from_file(ruta+'iconos/archivo.png')
        self.barraArchivoNuevo=gtk.ToolButton(icoArc)
        self.barraArchivoNuevo.set_tooltip(tooltips,"Insertar Nuevo Archivo")
        self.barraArchivoNuevo.set_sensitive(False)
        #botones de objetos
        self.sep3 = gtk.SeparatorToolItem()
        
        icoRec=gtk.Image()
        icoRec.set_from_file(ruta+'iconos/cuadrado.png')
        self.barraRectangulo=gtk.ToolButton(icoRec)
        self.barraRectangulo.set_tooltip(tooltips,"Insertar rectangulo");
        self.barraRectangulo.set_sensitive(False)
        
        icoCir=gtk.Image()
        icoCir.set_from_file(ruta+'iconos/circulo.png')
        self.barraCirculo=gtk.ToolButton(icoCir)
        self.barraCirculo.set_tooltip(tooltips,"Insertar circulo");
        self.barraCirculo.set_sensitive(False)
        
        icoTri=gtk.Image()
        icoTri.set_from_file(ruta+'iconos/triangulo.png')
        self.barraTriangulo=gtk.ToolButton(icoTri)
        self.barraTriangulo.set_tooltip(tooltips,"Insertar triangulo");
        self.barraTriangulo.set_sensitive(False)

        icoLin=gtk.Image()
        icoLin.set_from_file(ruta+'iconos/linea.png')
        self.barraLinea=gtk.ToolButton(icoLin)
        self.barraLinea.set_tooltip(tooltips,"Insertar Linea");
        self.barraLinea.set_sensitive(False)
        
        icoimg=gtk.Image()
        icoimg.set_from_file(ruta+'iconos/imagen.png')
        self.barraImagen=gtk.ToolButton(icoimg)
        self.barraImagen.set_tooltip(tooltips,"Insertar Imagen a la Hoja");
        self.barraImagen.set_sensitive(False)
        
        icotex=gtk.Image()
        icotex.set_from_file(ruta+'iconos/texto.png')
        self.barraTexto=gtk.ToolButton(icotex)
        self.barraTexto.set_tooltip(tooltips,"Insertar texto");
        self.barraTexto.set_sensitive(False)
        
        #botones de formularios
        self.sep4 = gtk.SeparatorToolItem()
        
        icoBot=gtk.Image()
        icoBot.set_from_file(ruta+'iconos/boton.png')
        self.barraBoton=gtk.ToolButton(icoBot)
        self.barraBoton.set_tooltip(tooltips,"Insertar Boton");
        self.barraBoton.set_sensitive(False)
        
        icoTex=gtk.Image()
        icoTex.set_from_file(ruta+'iconos/cajaTexto.png')
        self.barraCajaTexto=gtk.ToolButton(icoTex)
        self.barraCajaTexto.set_tooltip(tooltips,"Insertar caja de texto");
        self.barraCajaTexto.set_sensitive(False)
        
        icoLis=gtk.Image()
        icoLis.set_from_file(ruta+'iconos/lista.png')
        self.barraLista=gtk.ToolButton(icoLis)
        self.barraLista.set_tooltip(tooltips,"Insertar Lista Desplegable");
        self.barraLista.set_sensitive(False)
        
        icoChk=gtk.Image()
        icoChk.set_from_file(ruta+'iconos/check.png')
        self.barraCheck=gtk.ToolButton(icoChk)
        self.barraCheck.set_tooltip(tooltips,"Insertar CheckBox");
        self.barraCheck.set_sensitive(False)
        
        icoArea=gtk.Image()
        icoArea.set_from_file(ruta+'iconos/editor.png')
        self.barraArea=gtk.ToolButton(icoArea)
        self.barraArea.set_tooltip(tooltips,"Insertar Editor de Texto");
        self.barraArea.set_sensitive(False)
        
        icoSnd=gtk.Image()
        icoSnd.set_from_file(ruta+'iconos/corneta.png')
        self.barraSon=gtk.ToolButton(icoSnd)
        self.barraSon.set_tooltip(tooltips,"Insertar Sonido a la Hoja");
        self.barraSon.set_sensitive(False)
        
        icoCla=gtk.Image()
        icoCla.set_from_file(ruta+'iconos/clap.png')
        self.barraCla=gtk.ToolButton(icoCla)
        self.barraCla.set_tooltip(tooltips,"Insertar Video a la Hoja");
        self.barraCla.set_sensitive(False)
        
        icoScr=gtk.Image()
        icoScr.set_from_file(ruta+'iconos/escritos.png')
        self.barraScr=gtk.ToolButton(icoScr)
        self.barraScr.set_tooltip(tooltips,"Insertar Codigo Escrito a la Hoja");
        self.barraScr.set_sensitive(False)
        
        #Insertamos los botones estandar a la barra
        self.barra.insert(self.barraNue, 0)
        self.barra.insert(self.barraAbr, 1)
        self.barra.insert(self.barraGua, 2)
        self.barra.insert(self.barraGuc, 3)
        self.barra.insert(self.sep, 4)
        self.barra.insert(self.quittb, 5)
        #Insertamos los botones recuros a la barra
        self.barra.insert(self.sep2,6)
        self.barra.insert(self.barraHojaNueva,7)
        self.barra.insert(self.barraImagenNuevo,8)
        self.barra.insert(self.barraSonidoNuevo,9)
        self.barra.insert(self.barraVideoNuevo,10)
        self.barra.insert(self.barraArchivoNuevo,11)
        #Insertamos los botones objetos a la barra
        self.barra.insert(self.sep3,12)
        self.barra.insert(self.barraRectangulo,13)
        self.barra.insert(self.barraCirculo,14)
        self.barra.insert(self.barraTriangulo,15)
        self.barra.insert(self.barraLinea,16)
        self.barra.insert(self.barraImagen,17)
        self.barra.insert(self.barraTexto,18)
        #insertamos los botones de Controles de Formularios
        self.barra.insert(self.sep4, 19)
        self.barra.insert(self.barraBoton, 20)
        self.barra.insert(self.barraCajaTexto, 21)
        self.barra.insert(self.barraLista, 22)
        self.barra.insert(self.barraCheck, 23)
        self.barra.insert(self.barraArea, 24)
        self.barra.insert(self.barraSon, 25)
        self.barra.insert(self.barraCla, 26)
        self.barra.insert(self.barraScr, 27)
        #La zona de Trabajo
            #NAvegador de Proyecto

        self.treeview = gtk.TreeView()
        
        
        # Crear la columna para la lista
        self.columna=gtk.TreeViewColumn('Proyecto')
        
        self.celdaIcono = gtk.CellRendererPixbuf()
        self.cell = gtk.CellRendererText()
        
        self.columna.pack_start(self.celdaIcono, False)
        self.columna.pack_start(self.cell, False)
        
        self.columna.set_attributes(self.celdaIcono, stock_id=1)
        self.columna.set_attributes(self.cell, text=0)
        
        self.treeview.append_column(self.columna)
        self.treeview.set_enable_tree_lines(True)
        self.selFila=self.treeview.get_selection()
        
        #Vista de las propiedades de los objetos
        self.panelPropiedades=gtk.TreeView()
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Propiedad", rendererText, text=0)
        column.set_sort_column_id(0)    
        self.panelPropiedades.append_column(column)
        
        self.cajaEditable = gtk.CellRendererCombo()
        self.cajaEditable.set_fixed_size(5, -1)
        self.cajaEditable.set_property("editable", True)
        self.cajaEditable.set_property("text-column", 0)
        self.cajaEditable.set_property("has-entry", True)
        
        column = gtk.TreeViewColumn("Valor", self.cajaEditable,text=1)
        column.add_attribute(self.cajaEditable, "model", 2)
        
        self.panelPropiedades.append_column(column)
        self.panelPropiedades.set_grid_lines(True)
        
            #Zona de Previsualizacion
        self.lienzo= webkit.WebView()
        self.lienzo.set_view_source_mode(False)
        propLienzo=webkit.WebSettings()
        propLienzo.set_property("enable-plugins",False)
        self.lienzo.set_settings(propLienzo)
        #propLienzo.set_property("title","Titulo 1")
        #self.lienzo.set_settings(propLienzo)
        # Barras de desplazamiento para el contenedor
        scroll = gtk.ScrolledWindow()
        scroll2 = gtk.ScrolledWindow()
        scroll3= gtk.ScrolledWindow()
        #self.scroll3.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        #barra estado
        self.statusbar = gtk.Statusbar()
        #Agregamos al Contenedor
        scroll.add(self.treeview)
        scroll2.add(self.lienzo)
        scroll3.add(self.panelPropiedades)
        tabla.attach(menu, 0, 100, 0, 1, gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK, 0, 0)
        tabla.attach(self.barra, 0, 100, 1, 2, gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK, 0, 0)
        tabla.attach(scroll, 0, 20, 2, 50, gtk.FILL, gtk.FILL|gtk.EXPAND, 0, 0)
        tabla.attach(scroll3,0,20,50,98,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND, 0, 0)
        tabla.attach(scroll2,20,100,2,98,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND, 0, 0)
        tabla.attach(self.statusbar,0,100,98,100,gtk.FILL|gtk.EXPAND,gtk.FILL, 0, 0)
         #ACtrivamos las funciones de los menu
        self.sal.connect("activate",self.salir,2)

        #activamos las funciones de los botones de la barra
        self.quittb.connect("clicked", self.salir,2)
        
        
        
        #mostramos la ventana
        self.window.add(tabla)
        self.window.show_all()
    
    def cuadroMensajes(self,titulo,mensaje,tipo,botones):
        men=gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,tipo, botones,mensaje)
        men.set_title(titulo)
        response=men.run()
        men.destroy()
        return response
        
    def cuadroDialogo(self,titulo,accion,botones):
        dialogo = gtk.FileChooserDialog(titulo,self.window,accion,botones)
        response = dialogo.run()
        archivo=dialogo.get_filename()
        dialogo.destroy()
        return (response,archivo)

    def cuadroDialogoScript(self,objetos):
        eventosEscena=["alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        eventosObjetos=["click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"]
        window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title("editor de escritos")
        window.set_size_request(600,600)
        window.set_resizable(False)
        window.set_modal(True)
        color = gtk.gdk.color_parse('#ffffff')
        window.modify_bg(gtk.STATE_NORMAL, color)
        barra = gtk.Toolbar()
        barra.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        barra.set_style(gtk.TOOLBAR_ICONS)
        barra.set_border_width(1)
        barra.set_icon_size(gtk.ICON_SIZE_MENU)
        icoNue=gtk.Image()
        icoNue.set_from_file(ruta+'iconos/proyecto.png')
        barraSCAN = gtk.ToolButton(icoNue)
        barra.insert(barraSCAN,0)
        caja=gtk.VBox(False)
        txtScript=gtk.TextView()
        cntScript=txtScript.get_buffer()
        txtScript.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 24)
        txtScript.connect("expose-event", self._pintaNumeros,cntScript,txtScript)
        #txtScript.connect("key-press-event",self.analizador,cntScript,objetos)
        cntScript.set_text(objetos[0].escritos)
        barraSCAN.connect("clicked",self.analizador,cntScript)
        lista=gtk.TreeStore(str,gtk.gdk.Pixbuf)
        padre=lista.append(None,["Sistema",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/sistema.png')])
        f=lista.append(padre,["cicloSistema",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/ciclo.png')])
        f=lista.append(padre,["cronometroSistema",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/ciclo.png')])
        for i in range(len(objetos)):
            if i==0:
                padre=lista.append(None,[objetos[i].nombre,gtk.gdk.pixbuf_new_from_file(ruta+'iconos/hoja.png')])
                for n in range(len(eventosEscena)):
                    f=lista.append(padre,[eventosEscena[n],gtk.gdk.pixbuf_new_from_file(ruta+'iconos/evento.png')])
            else:
                padre=lista.append(None,[objetos[i].nombre,gtk.gdk.pixbuf_new_from_file(ruta+'iconos/objeto.png')])
                for n in range(len(eventosObjetos)):
                    f=lista.append(padre,[eventosObjetos[n],gtk.gdk.pixbuf_new_from_file(ruta+'iconos/evento.png')])
        listaObjetos = gtk.TreeView()
        listaObjetos.set_model(lista)
        lacolumna = gtk.TreeViewColumn("Objetos")
        listaObjetos.append_column(lacolumna)
        celda = gtk.CellRendererText()
        icono = gtk.CellRendererPixbuf()
        lacolumna.pack_start(icono, False)
        lacolumna.pack_start(celda, False)
        lacolumna.set_attributes(icono, pixbuf=1)
        lacolumna.set_attributes(celda, text=0)
        seleccionFila=listaObjetos.get_selection()
        listaObjetos.connect("row-activated", self.muestraAtributos,seleccionFila,cntScript)
        listaIzquierda=gtk.TreeStore(str,gtk.gdk.Pixbuf)
        padre=listaIzquierda.append(None,["Variables",None])
        f=listaIzquierda.append(padre,["general",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/variable.png')])
        f=listaIzquierda.append(padre,["local",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/variable.png')])
        padre=listaIzquierda.append(None,["Funciones",None])
        f=listaIzquierda.append(padre,["funcion",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/funcion.png')])
        padre=listaIzquierda.append(None,["Metodos",None])
        f=listaIzquierda.append(padre,["propiedad",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["mostrar",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["ocultar",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["mover",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["redimensionar",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["rotar",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["mensaje",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["confirmacion",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        f=listaIzquierda.append(padre,["entrada",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/metodo.png')])
        padre=listaIzquierda.append(None,["Controles de Flujo",None])
        f=listaIzquierda.append(padre,["Si",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/if.png')])
        f=listaIzquierda.append(padre,["Mientras",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/if.png')])
        f=listaIzquierda.append(padre,["Desde-Hasta",gtk.gdk.pixbuf_new_from_file(ruta+'iconos/if.png')])
        listaMetodos = gtk.TreeView()
        listaMetodos.set_model(listaIzquierda)
        lacolumna2 = gtk.TreeViewColumn("Metodos")
        listaMetodos.append_column(lacolumna2)
        celda2 = gtk.CellRendererText()
        icono2 = gtk.CellRendererPixbuf()
        lacolumna2.pack_start(icono2, False)
        lacolumna2.pack_start(celda2, True)
        lacolumna2.set_attributes(icono2, pixbuf= 1)
        lacolumna2.set_attributes(celda2, text= 0)
        seleccionFila2=listaMetodos.get_selection()
        listaMetodos.connect("row-activated", self.muestraAtributos2,seleccionFila2,cntScript)
        scroll = gtk.ScrolledWindow()
        scroll2 = gtk.ScrolledWindow()
        scroll.add(listaObjetos)
        scroll2.add(listaMetodos)
        caja.pack_start(barra,False)
        sep=gtk.HSeparator()
        scrolles=gtk.HBox(False)
        scrolles.pack_start(scroll,True,True)
        scrolles.pack_start(scroll2,True,True)
        caja.pack_start(scrolles,False,False,0)
        caja.pack_start(sep,False,True)
        caja.pack_start(txtScript,True)
        window.add(caja)
        window.show_all()
    
    def muestraAtributos(self,treeview,itera, path, fila,escrito):
        (mod,ite)= fila.get_selected_rows()
        iterador= ite[0]
        if len(iterador)==2:
            if mod[ite[0]][0]=="cicloSistema":
                self.statusbar.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(100)")
                linea=str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(100):"
            elif mod[ite[0]][0]=="cronometroSistema":
                self.statusbar.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(500)")
                linea=str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(500):"
            else:
                self.statusbar.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0]))
                linea=str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+":"
            base=escrito.get_text(*escrito.get_bounds())
            base=base + linea+"\n\t\nfin->"+str(mod[ite[0]][0])+"\n"
            escrito.set_text(base)
    
    def muestraAtributos2(self,treeview,itera, path, fila,escrito):
        (mod,ite)= fila.get_selected_rows()
        iterador= ite[0]
        base=escrito.get_text(*escrito.get_bounds())
        if len(iterador)==2:
            if iterador[0]==0:
                if iterador[1]==0:
                    lineaCodigo= "varg->mivariable=0\n"
                if iterador[1]==1:
                    lineaCodigo= "varl->mivariable=0\n"
            elif iterador[0]==1:
                lineaCodigo= "func->lafuncion(arg1,arg2,arg3):\n"
            elif iterador[0]==2:
                lineaCodigo= "\t"+str(mod[ite[0]][0])+"()\n"
            elif iterador[0]==3:
                lineaCodigo= "\t"+str(mod[ite[0]][0])+"()\n"
            base=base + lineaCodigo
            self.statusbar.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+":"+str(iterador[0]))
            escrito.set_text(base)
    
    def _pintaNumeros(self,window,event,text_buffer,text_view):
        bounds = text_buffer.get_bounds()
        text = text_buffer.get_text(*bounds)
        nlines = text_buffer.get_line_count()
        layout = pango.Layout(text_view.get_pango_context())
        layout.set_markup("\n".join([str(x + 1) for x in range(nlines)]))
        layout.set_alignment(pango.ALIGN_RIGHT)
        width = layout.get_pixel_size()[0]
        text_view.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, width + 4)
        y = -text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_RIGHT, 2, 0)[1]
        window = text_view.get_window(gtk.TEXT_WINDOW_RIGHT)
        window.clear()
        text_view.style.paint_layout(window=window,state_type=gtk.STATE_NORMAL,use_text=True,area=None,widget=text_view,detail=None,x=2,y=y,layout=layout)
    
    def analizador(self,widget,data=None,objetos=None):
        eventosValidos=["cronometroSistema","cicloSistema","alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        variablesValidas=["varg","varl"]
        variablesDeclaradas=[]
        ini,fin=data.get_bounds()
        lineas=data.get_line_count()+1
        #variables de control (banderas)
        inicioLinea=True
        declaracionVariables=True
        for i in range(lineas-1):
            p1=data.get_iter_at_line(i)
            ncr=p1.get_chars_in_line()-1
            if ncr>0:#esto es para evitar el molestoso aborto de gtk cuando las linea esta vacia
                p2=data.get_iter_at_line_offset(i,ncr)
                linea = data.get_text(p1,p2)
                print "evaluando "+linea
                if inicioLinea:
                    token=linea.split("->")[0]
                    nombre=linea.split("->")[1]
                    if token in variablesValidas:
                        if declaracionVariables:
                            if nombre in variablesDeclaradas:
                                print "Esta Variable ya fue declarada"
                            else:
                                variablesDeclaradas.append(nombre)
                        else:
                            print "No se puede declarar variables en este contexto"
                    elif token in eventosValidos:
                        declaracionVariables=False
                        inicioLinea=False
                    elif token=="func":
                        pass
                    else:
                        print "Inicio de linea no reconocido"
                else:
                    if re.search("^\t",linea):
                        print "elemento de funcion"
                    else:
                        if linea.split("->")[0]=="fin":
                            inicioLinea=True
                        else:
                            print "debe cerrar el evento"
            else:
                linea=""
            print i
            
        #tag=data.create_tag("error",foreground="#FF0000")
        """data.remove_all_tags(ini,fin)
        tagVar=data.create_tag(None,foreground="#0000FF")
        tagFun=data.create_tag(None,foreground="#0A6526")
        tagEve=data.create_tag(None,foreground="#FFA500")
        tagErr=data.create_tag(None,foreground="#FF0000")
        error="Todo fino!!!! OK"
            
            error="Todo fino!!!! OK"
            if re.search("^\t",linea):
                print "elemento de funcion"
            else:
                if re.search("^var\s",linea):
                    print "una variable"
                    data.apply_tag(tagVar,p1,p2)
                elif re.search("^funcion\s",linea):
                    print "una funcion"
                    data.apply_tag(tagFun,p1,p2)
                elif re.search("^al+[A,C,P,F,S]{1}.*_Hoja\d{1,2}$",linea):
                    if linea.split("_")[0] in eventos:
                        if linea.split("_")[1] in objetos:
                            data.apply_tag(tagEve,p1,p2)
                            continue
                        else:
                            data.apply_tag(tagErr,p1,p2)
                            error="Error de Sintaxis en la linea "+str(i+1)+" Esta Escena No existe"
                            break
                        els:
                        data.apply_tag(tagErr,p1,p2)
                        error="Error Lexico en la linea"+str(i+1)+" La escena no posee el evento"
                        break
                    els:
                    data.apply_tag(tagErr,p1,p2)
                    error= "Error de sintaxis no se reconoce lo escrito en la linea "+str(i+1)
                    break"""
        self.statusbar.push(0,str(lineas))

    def salir(self,widget,data=None):
        respuesta =self.cuadroMensajes("Confirmación de Salida","¿Está Seguro de Querer Salir del Programa?\nAsegurese de haber guardado los cambios en el proyecto",gtk.MESSAGE_INFO,gtk.BUTTONS_YES_NO)
        if respuesta == gtk.RESPONSE_YES:
            if data==2:
                gtk.main_quit()
            return False
        else:
            return True

    def destroy(self, widget):
        gtk.main_quit()
    
    def main(self):
        gtk.main()
    
    def hojaBienvenida(self,widget=None,data=None):
        FONDO="<html><head></head><body style='background:url(iconos/alma.png)'><h1 style='color:#006400;text-shadow: 5px 5px 5px #FF4500;top:0%;position:absolute'>Generador de Contenidos Educativos Digitales</h1><h2 style='position: absolute;top:5%;text-align:center'>GeCED</h2></body></html>"
        self.lienzo.load_html_string(FONDO,"file://"+ruta)
