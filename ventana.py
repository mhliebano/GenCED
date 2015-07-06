# -*- coding: utf-8 -*-
import webkit
import gtk
import glib
import os, shutil
ruta= os.path.dirname(os.path.realpath(__file__))

class Ventana:

    def __init__(self):
        #La ventana
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Generador de CED")
        self.window.set_default_size(640,480)
        self.window.maximize()
        self.window.set_resizable(True)
        self.window.set_icon_from_file(os.path.join(ruta,'iconos/iconoApp.png'))
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
        menuHerramienta=gtk.Menu()
        menuAplicacion=gtk.Menu()
        
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
        
        #el Menu Herramientas
        menuH.set_submenu(menuHerramienta)
        self.gaI=gtk.MenuItem("Galeria de Imagenes")
        self.imF=gtk.MenuItem("Importar desde Proyecto Fuente")
        self.imE=gtk.MenuItem("Importar desde Proyecto Exportado")
        menuHerramienta.append(self.gaI)
        menuHerramienta.append(self.imF)
        menuHerramienta.append(self.imE)
        
        #el menu aplicacion
        menuL.set_submenu(menuAplicacion)
        self.exP=gtk.MenuItem("Exportar Canaima (Linux)")
        self.exH=gtk.MenuItem("Exportar a HTML5")
        menuAplicacion.append(self.exP)
        menuAplicacion.append(self.exH)
        
        
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
        icoNue.set_from_file(os.path.join(ruta,'iconos/proyecto.png'))
        self.barraNue = gtk.ToolButton(icoNue)
        self.barraNue.set_tooltip(tooltips,"Nuevo Proyecto")

        icoAbr=gtk.Image()
        icoAbr.set_from_file(os.path.join(ruta,'iconos/abrir.png'))
        self.barraAbr = gtk.ToolButton(icoAbr)
        self.barraAbr.set_tooltip(tooltips,"Abrir Proyecto")
        
        icoGua=gtk.Image()
        icoGua.set_from_file(os.path.join(ruta,'iconos/guardar.png'))
        self.barraGua = gtk.ToolButton(icoGua)
        self.barraGua.set_tooltip(tooltips,"Guardar Proyecto")
        self.barraGua.set_sensitive(False)
        
        icoGuc=gtk.Image()
        icoGuc.set_from_file(os.path.join(ruta,'iconos/guardarc.png'))
        self.barraGuc = gtk.ToolButton(icoGuc)
        self.barraGuc.set_tooltip(tooltips,"Guardar Proyecto Como")
        self.barraGuc.set_sensitive(False)
        
        self.sep = gtk.SeparatorToolItem()
        icoSal=gtk.Image()
        icoSal.set_from_file(os.path.join(ruta,'iconos/salir.png'))
        self.quittb = gtk.ToolButton(icoSal)
        
        #botones de recursos
        self.sep2 = gtk.SeparatorToolItem()
        icoHoj=gtk.Image()
        icoHoj.set_from_file(os.path.join(ruta,'iconos/hoja.png'))
        self.barraHojaNueva=gtk.ToolButton(icoHoj)
        self.barraHojaNueva.set_tooltip(tooltips,"Insertar Nueva Hoja")
        self.barraHojaNueva.set_sensitive(False)
        
        icoImg=gtk.Image()
        icoImg.set_from_file(os.path.join(ruta,'iconos/imagen.png'))
        self.barraImagenNuevo=gtk.ToolButton(icoImg)
        self.barraImagenNuevo.set_tooltip(tooltips,"Insertar Nueva Imagen")
        self.barraImagenNuevo.set_sensitive(False)
        
        icoSon=gtk.Image()
        icoSon.set_from_file(os.path.join(ruta,'iconos/sonido.png'))
        self.barraSonidoNuevo=gtk.ToolButton(icoSon)
        self.barraSonidoNuevo.set_tooltip(tooltips,"Insertar Nuevo Sonido")
        self.barraSonidoNuevo.set_sensitive(False)
        
        icoVid=gtk.Image()
        icoVid.set_from_file(os.path.join(ruta,'iconos/video.png'))
        self.barraVideoNuevo=gtk.ToolButton(icoVid)
        self.barraVideoNuevo.set_tooltip(tooltips,"Insertar Nuevo Video")
        self.barraVideoNuevo.set_sensitive(False)
        
        icoArc=gtk.Image()
        icoArc.set_from_file(os.path.join(ruta,'iconos/archivo.png'))
        self.barraArchivoNuevo=gtk.ToolButton(icoArc)
        self.barraArchivoNuevo.set_tooltip(tooltips,"Insertar Nuevo Archivo")
        self.barraArchivoNuevo.set_sensitive(False)
        #botones de objetos
        self.sep3 = gtk.SeparatorToolItem()
        
        icoRec=gtk.Image()
        icoRec.set_from_file(os.path.join(ruta,'iconos/cuadrado.png'))
        self.barraRectangulo=gtk.ToolButton(icoRec)
        self.barraRectangulo.set_tooltip(tooltips,"Insertar rectangulo");
        self.barraRectangulo.set_sensitive(False)
        
        icoCir=gtk.Image()
        icoCir.set_from_file(os.path.join(ruta,'iconos/circulo.png'))
        self.barraCirculo=gtk.ToolButton(icoCir)
        self.barraCirculo.set_tooltip(tooltips,"Insertar circulo");
        self.barraCirculo.set_sensitive(False)
        
        icoTri=gtk.Image()
        icoTri.set_from_file(os.path.join(ruta,'iconos/triangulo.png'))
        self.barraTriangulo=gtk.ToolButton(icoTri)
        self.barraTriangulo.set_tooltip(tooltips,"Insertar triangulo");
        self.barraTriangulo.set_sensitive(False)

        icoLin=gtk.Image()
        icoLin.set_from_file(os.path.join(ruta,'iconos/linea.png'))
        self.barraLinea=gtk.ToolButton(icoLin)
        self.barraLinea.set_tooltip(tooltips,"Insertar Linea");
        self.barraLinea.set_sensitive(False)
        
        icoimg=gtk.Image()
        icoimg.set_from_file(os.path.join(ruta,'iconos/imagen.png'))
        self.barraImagen=gtk.ToolButton(icoimg)
        self.barraImagen.set_tooltip(tooltips,"Insertar Imagen a la Hoja");
        self.barraImagen.set_sensitive(False)
        
        icotex=gtk.Image()
        icotex.set_from_file(os.path.join(ruta,'iconos/texto.png'))
        self.barraTexto=gtk.ToolButton(icotex)
        self.barraTexto.set_tooltip(tooltips,"Insertar texto");
        self.barraTexto.set_sensitive(False)
        
        #botones de formularios
        self.sep4 = gtk.SeparatorToolItem()
        
        icoBot=gtk.Image()
        icoBot.set_from_file(os.path.join(ruta,'iconos/boton.png'))
        self.barraBoton=gtk.ToolButton(icoBot)
        self.barraBoton.set_tooltip(tooltips,"Insertar Boton");
        self.barraBoton.set_sensitive(False)
        
        icoTex=gtk.Image()
        icoTex.set_from_file(os.path.join(ruta,'iconos/cajaTexto.png'))
        self.barraCajaTexto=gtk.ToolButton(icoTex)
        self.barraCajaTexto.set_tooltip(tooltips,"Insertar caja de texto");
        self.barraCajaTexto.set_sensitive(False)
        
        icoLis=gtk.Image()
        icoLis.set_from_file(os.path.join(ruta,'iconos/lista.png'))
        self.barraLista=gtk.ToolButton(icoLis)
        self.barraLista.set_tooltip(tooltips,"Insertar Lista Desplegable");
        self.barraLista.set_sensitive(False)
        
        icoChk=gtk.Image()
        icoChk.set_from_file(os.path.join(ruta,'iconos/check.png'))
        self.barraCheck=gtk.ToolButton(icoChk)
        self.barraCheck.set_tooltip(tooltips,"Insertar CheckBox");
        self.barraCheck.set_sensitive(False)
        
        icoArea=gtk.Image()
        icoArea.set_from_file(os.path.join(ruta,'iconos/editor.png'))
        self.barraArea=gtk.ToolButton(icoArea)
        self.barraArea.set_tooltip(tooltips,"Insertar Editor de Texto");
        self.barraArea.set_sensitive(False)
        
        icoSnd=gtk.Image()
        icoSnd.set_from_file(os.path.join(ruta,'iconos/corneta.png'))
        self.barraSon=gtk.ToolButton(icoSnd)
        self.barraSon.set_tooltip(tooltips,"Insertar Sonido a la Hoja");
        self.barraSon.set_sensitive(False)
        
        icoCla=gtk.Image()
        icoCla.set_from_file(os.path.join(ruta,'iconos/clap.png'))
        self.barraCla=gtk.ToolButton(icoCla)
        self.barraCla.set_tooltip(tooltips,"Insertar Video a la Hoja");
        self.barraCla.set_sensitive(False)
        
        icoScr=gtk.Image()
        icoScr.set_from_file(os.path.join(ruta,'iconos/escritos.png'))
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
        #control para el proyecto activo
        self.proy=None
    
    def cuadroMensajes(self,titulo,mensaje,tipo,botones):
        men=gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,tipo, botones,mensaje)
        men.set_title(titulo)
        response=men.run()
        men.destroy()
        return response
        
    def cuadroDialogo(self,titulo,accion,botones):
        dialogo = gtk.FileChooserDialog(titulo,self.window,accion,botones)
        dialogo.set_current_folder(os.path.expanduser('~'))
        filtro=gtk.FileFilter()
        filtro.set_name("Proyectos GenCED")
        filtro.add_pattern("*.gcd")
        dialogo.add_filter(filtro)
        response = dialogo.run()
        archivo=dialogo.get_filename()
        dialogo.destroy()
        return (response,archivo)

    def salir(self,widget,data=None):
        respuesta =self.cuadroMensajes("Confirmación de Salida","¿Está Seguro de Querer Salir del Programa?\nAsegurese de haber guardado los cambios en el proyecto",gtk.MESSAGE_INFO,gtk.BUTTONS_YES_NO)
        if respuesta == gtk.RESPONSE_YES:
            if data==2:
                if self.proy!=None:
                    shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proy)
                gtk.main_quit()
            return False
        else:
            if self.proy!=None:
                shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proy)
            return True

    def destroy(self, widget):
        gtk.main_quit()
    
    def main(self):
        gtk.main()
    
    def hojaBienvenida(self,widget=None,data=None):
        FONDO="<html><head></head><body style='background:url("+ruta+"/iconos/alma.png)'><h1 style='color:#006400;text-shadow: 5px 5px 5px #FF4500;top:0%;position:absolute'>Generador de Contenidos Educativos Digitales</h1><h2 style='position: absolute;top:5%;text-align:center'>GenCED</h2><audio source src='"+str(ruta)+"/recursos/sonidos/HARP1.ogg' type='audio/ogg'   preload autoplay></audio></body></html>"
        self.lienzo.load_html_string(FONDO,"file://"+ruta)
