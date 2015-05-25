# -*- coding: utf-8 -*-
import sys
import glib,gtk
import shutil
import os, stat
from objetos import *
from analizador import *
class Acciones:
    
    def __init__(self,IGU):
        #self.rutaProyecto=None
        #self.nombreProyecto=None
        #self.hojas=[]
        self.proyecto=""
        self.recursos=[]
        self.objetos=[]
        self.EDITADO=0
        self.puntero=-1
        self.nivel=-1
        self.igu=IGU
        self.__elimi=False
        self.__copi=None
        self.activaAccionMenu()
        self.activaBotonesBarra()
        
    def activaAccionMenu(self):
        self.igu.nue.connect("activate",self.nuevoProyecto)
        self.igu.abr.connect("activate",self.abrirProyecto)
        self.igu.gua.connect("activate",self.guardarProyecto)
        self.igu.cer.connect("activate",self.cerrarProyecto)
        self.igu.inHoja.connect("activate",self.insertarHoja)
        self.igu.inImagen.connect("activate",self.insertarRecurso,0)
        self.igu.inSonido.connect("activate",self.insertarRecurso,1)
        self.igu.inVideo.connect("activate",self.insertarRecurso,2)
        self.igu.inArchivo.connect("activate",self.insertarRecurso,3)
        self.igu.cop.connect("activate",self.copiarObjeto)
        self.igu.peg.connect("activate",self.pegarObjeto)
        self.igu.elm.connect("activate",self.eliminarObjetos)
        
        self.igu.treeview.connect("cursor-changed", self.punteroArbol)
        #eliminar al hacer doble click self.igu.treeview.connect("row-activated", self.eliminarObjetos)
        #self.igu.panelPropiedades.connect("row-activated", self.propiedadesElementos)
        self.igu.cajaEditable.connect('edited', self._cambiaAtributo, 1)
        #correr vista previa
        self.igu.eje.connect("activate",self.vistaPrevia)
        self.igu.verHtml.connect("activate",self.muestraCodigoFuente)
        
        self.igu.exP.connect("activate",self.exportarProyecto,1)
        self.igu.exH.connect("activate",self.exportarProyecto,2)
        
        self.igu.gaI.connect("activate",self.verImagenes,None)
        
        self.igu.lienzo.connect("key-press-event",self.presionaTecla)
        #self.igu.lienzo.connect("button-press-event",self.presionaRaton)
        self.igu.lienzo.connect('title-changed',self.cambiaTitulo)
    
    def verImagenes(self,widget,accion):
        if accion==None:
            pagina="<html><head><script>function cf(id){document.title=id}</script></head><body><h1>Categorias de Imagenes</h1>"
            for (path,directory,archivos) in os.walk("./recursos/imagenes"):
                categoria=path.split("/")
                if len(categoria)>3:
                    pagina+="<div style='width:10%;height:10%;margin-left:1%;margin-bottom:2%;float:left;text-align:center'><img src='"+os.path.dirname(os.path.realpath(__file__))+"/iconos/carpeta.png' style='display:block;width:90%;height;65%' onclick='cf(this.id)' id='0+"+str(categoria[3])+"'/>"+str(categoria[3])+"</div>"
            pagina+="</body></html>"
        else:
            pagina="<html><head><script>function cf(id){document.title=id}</script></head><body><h1>Categorias de Imagenes: "+str(accion)+"</h1>"
            i=0
            for (path,ficheros,archivos) in os.walk("./recursos/imagenes/"+str(accion)):
                for (imagen) in archivos:
                    pagina+="<div style='width:10%;height:10%;margin-left:1%;margin-bottom:2%;float:left;text-align:center;border:1px solid #000000'><img src='"+os.path.dirname(os.path.realpath(__file__))+"/recursos/imagenes/"+str(accion)+"/"+str(imagen)+"' style='display:block;width:80%;height:65%' onclick='cf(this.id)' id='2+"+accion+"+"+imagen+"'/>"+imagen+"</div>"
            pagina+="</body></html>"
        self.igu.lienzo.load_html_string(pagina,"file://"+os.path.dirname(os.path.realpath(__file__))+"/")
        
    def exportarProyecto(self,widget,tipo):
        if self.proyecto=="":
            self.igu.statusbar.push(0,"¿Cuál Proyecto vas a Ejecutar?")
            return
        if tipo==1:
            if str(os.name)== "posix":
                conf=open(self.proyecto.ruta+"/main","w")
                escrito='#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport gtk\nimport webkit\nimport os\nruta= os.path.dirname(os.path.realpath(__file__))\npaginas=[]\ndef destroy(self):\n\tgtk.main_quit()\ndef cambiaTitulo(self,widget,titulo):\n\tself.load_html_string(paginas[int(titulo)],"file://"+ruta+"/")\nif __name__ == "__main__":\n'
                for i in range(len(self.objetos)):
                    pagina="<html><head><script src='\"+str(ruta)+\"/recursos/jquery.js'></script><script type='text/javascript' src='\"+str(ruta)+\"/recursos/jquery.timer.js'></script>"+self.objetos[i][0].javascript+"</head>"
                    for j in range(len(self.objetos[i])):
                        pagina=pagina+str(self.objetos[i][j].trazaObjeto("\"+str(ruta)+\""))
                    pagina=pagina+"</body></html>"
                    escrito+='\tpaginas.append("'+str(pagina)+'")\n'
                    pagina=""
                escrito+='\twindow=gtk.Window(gtk.WINDOW_TOPLEVEL)\n\twindow.set_position(gtk.WIN_POS_CENTER)\n\twindow.set_title("Vista Previa de '+str(self.proyecto._nombre)+'")\n\twindow.set_size_request('+str(self.proyecto.ancho)+','+str(self.proyecto.alto)+')\n\tif "'+str(self.proyecto.maximizado)+'"=="Verdadero":\n\t\twindow.maximize()\n\twindow.set_resizable(False)\n\twindow.set_modal(True)\n\tcolor = gtk.gdk.color_parse("#ffffff")\n\twindow.modify_bg(gtk.STATE_NORMAL, color)\n\twindow.connect("destroy",destroy)\n\tlienzo= webkit.WebView()\n\tlienzo.set_view_source_mode(False)\n\tlienzo.load_html_string(paginas[0],"file://"+ruta+"/")\n\tlienzo.connect("title-changed",cambiaTitulo)\n\twindow.add(lienzo)\n\twindow.show_all()\n\tgtk.main()'
                conf.write(escrito)
                conf.close
                os.chmod(self.proyecto.ruta+"/main",stat.S_IRWXU)
                self.igu.statusbar.push(0,"Ok todo listo")
        elif tipo==2:
            if str(os.name)== "posix":
                os.mkdir(self.proyecto.ruta+"/html")
                for i in range(len(self.objetos)):
                    conf=open(self.proyecto.ruta+"/html/pagina"+str(i)+".html","w")
                    pagina="<html><head><script src='../recursos/jquery.js'></script><script type='text/javascript' src='../recursos/jquery.timer.js'></script>"+self.objetos[i][0].javascript+"</head>"
                    for j in range(len(self.objetos[i])):
                        pagina=pagina+str(self.objetos[i][j].trazaObjeto("../"))
                    pagina=pagina+"</body></html>"
                    conf.write(pagina)
                    conf.close
                    pagina=""
                self.igu.statusbar.push(0,"Ok todo listo")
        else:
            self.igu.statusbar.push(0,"Tipo No Reconocido")
    
    def vistaPrevia(self,widget,data=None):
        if self.proyecto=="":
            self.igu.statusbar.push(0,"¿Cuál Proyecto vas a Ejecutar?")
            return
        for i in range(len(self.objetos)):
            pagina="<html><head><script src='"+self.proyecto.ruta+"/recursos/jquery.js'></script><script type='text/javascript' src='"+self.proyecto.ruta+"/recursos/jquery.timer.js'></script>"+self.objetos[i][0].javascript+"</head>"
            for j in range(len(self.objetos[i])):
                pagina=pagina+str(self.objetos[i][j].trazaObjeto(self.proyecto.ruta))
            pagina=pagina+"</body></html>"
            self.proyecto.paginas[i]=pagina
            pagina=""
        self.proyecto.ejecutar()
    
    def presionaTecla(self,widget,event):
        keycode = gtk.gdk.keyval_to_upper(event.keyval)
        #65362 up,65364 dw,65361 lf,65363 rg
        if keycode==65361:
            self.objetos[self.nivel[2]][self.nivel[3]+1].x=float(self.objetos[self.nivel[2]][self.nivel[3]+1].x)-0.2
        if keycode==65362:
            self.objetos[self.nivel[2]][self.nivel[3]+1].y=float(self.objetos[self.nivel[2]][self.nivel[3]+1].y)-0.2
        if keycode==65363:
            self.objetos[self.nivel[2]][self.nivel[3]+1].x=float(self.objetos[self.nivel[2]][self.nivel[3]+1].x)+0.2
        if keycode==65364:
            self.objetos[self.nivel[2]][self.nivel[3]+1].y=float(self.objetos[self.nivel[2]][self.nivel[3]+1].y)+0.2
        self.actualizaVistaPropiedades(self.objetos[self.nivel[2]][self.nivel[3]+1])
        self.actulizaLienzo()
        #print keycode
    
    def presionaRaton(self,widget,event):
        assert event.type == gtk.gdk.BUTTON_PRESS
        self.igu.statusbar.push(0, 'Clicked at x={0}, y={0}'.format(event.x, event.y))
        self.igu.cuadroDialogoScript()
        #self.igu.lienzo.execute_script('tag= window.document.element.nodeName;alert("El elemento selecionado ha sido " + tag);')
        
        """doc = widget.get_dom_document()
        nodes = doc.getElementsByTagName('body')
        body = nodes.item(0)

        d = doc.createElement("div")
        b = doc.createElement("Button")
        b.innerHTML = "hello"
        b.onclick = self._button_click_event
        d.appendChild(b)
        txt = doc.createTextNode("hello world")
        body.appendChild(txt)
        body.appendChild(d)
        body.tabIndex = 5
        #body.addEventListener("mouseover", self._mouse_over_event, False)
        body.onmouseover = self._mouse_over_event"""
    
    def cambiaTitulo(self,widget,web,titulo):
        variables=titulo.split("+")
        if variables[0]=='0':
            self.verImagenes(widget,variables[1])
        elif variables[0]=='1':
            for i in range(len(self.objetos[self.puntero])):
                if self.objetos[self.puntero][i].nombre==variables[1]:
                    self.actualizaVistaPropiedades(self.objetos[self.puntero][i])
                    #widget.execute_script("select('"+titulo+"')")
                    self.igu.treeview.set_cursor((0,0,self.puntero,i-1))
                    break
        elif variables[0]=='2':
            pagina="<html><head><title></title></head>"
            pagina=pagina+"<img src='"+os.path.dirname(os.path.realpath(__file__))+"/recursos/imagenes/"+str(variables[1])+"/"+str(variables[2])+"'/>"
            if self.proyecto!="":
                pagina+="<button>Insertar al Proyecto</button>"
                
            pagina=pagina+"</body></html>"
            self.igu.lienzo.load_html_string(pagina,"file://"+os.path.dirname(os.path.realpath(__file__))+"/")
        else:
            self.igu.statusbar.push(0,"No se que hacer!!!");
        
    def muestraCodigoFuente(self,widget=None):
        print self.igu.lienzo.get_view_source_mode()
        if self.igu.lienzo.get_view_source_mode()==True:
            self.igu.lienzo.set_view_source_mode(False)
        else:
            self.igu.lienzo.set_view_source_mode(True)
    
    def activaBotonesBarra(self):
        self.igu.barraNue.connect("clicked",self.nuevoProyecto)
        self.igu.barraAbr.connect("clicked",self.abrirProyecto)
        self.igu.barraGua.connect("clicked",self.guardarProyecto)
        self.igu.barraHojaNueva.connect("clicked",self.insertarHoja)
        self.igu.barraImagenNuevo.connect("clicked",self.insertarRecurso,0)
        self.igu.barraSonidoNuevo.connect("clicked",self.insertarRecurso,1)
        self.igu.barraVideoNuevo.connect("clicked",self.insertarRecurso,2)
        self.igu.barraArchivoNuevo.connect("clicked",self.insertarRecurso,3)
        self.igu.barraRectangulo.connect("clicked",self.insertarObjeto,0)
        self.igu.barraCirculo.connect("clicked",self.insertarObjeto,1)
        self.igu.barraTriangulo.connect("clicked",self.insertarObjeto,2)
        self.igu.barraLinea.connect("clicked",self.insertarObjeto,3)
        self.igu.barraImagen.connect("clicked",self.insertarObjeto,4)
        self.igu.barraTexto.connect("clicked",self.insertarObjeto,5)
        self.igu.barraBoton.connect("clicked",self.insertarObjeto,6)
        self.igu.barraCajaTexto.connect("clicked",self.insertarObjeto,7)
        self.igu.barraLista.connect("clicked",self.insertarObjeto,8)
        self.igu.barraCheck.connect("clicked",self.insertarObjeto,9)
        self.igu.barraArea.connect("clicked",self.insertarObjeto,10)
        self.igu.barraSon.connect("clicked",self.insertarObjeto,11)
        self.igu.barraCla.connect("clicked",self.insertarObjeto,12)
        self.igu.barraScr.connect("clicked",self.insertarObjeto,13)

    def copiarObjeto(self,widget=None,data=None):
        if self.proyecto=="":
            self.igu.statusbar.push(0,"¿Que intentas copiar?")
            return
        if len(self.nivel)==4:
            if self.nivel[1]==0:
                self.__copi=self.objetos[self.nivel[2]][self.nivel[3]+1]
                self.igu.statusbar.push(0, "El tipo de objeto a copiar es: "+self.__copi.nombre)
            else:
                self.igu.statusbar.push(0, "Objeto no Copiable")
        else:
            self.igu.statusbar.push(0, "Objeto no Copiable")
    
    def pegarObjeto(self,widget=None,data=None):
        if self.proyecto=="":
            self.igu.statusbar.push(0,"¿Qué Intentas Pegar?")
            return
        if len(self.nivel)==4:
            if self.nivel[1]==0:
                self.igu.statusbar.push(0, "El tipo de objeto pegado es: "+self.__copi.nombre+" en la "+str(self.objetos[self.nivel[2]][0].nombre))
                objeto=self.__copi
                if objeto.__class__==Cuadro:
                    cuadrado=Cuadro(self.objetos[self.nivel[2]][0].cuentaObjetos["cuadro"])
                    self.objetos[self.nivel[2]][0].cuentaObjetos["cuadro"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["cuadro"])+1
                    self.objetos[self.puntero].append(cuadrado)
                    cuadrado.colorFondo=objeto.colorFondo
                    cuadrado.transparencia=objeto.transparencia
                    cuadrado.ancho=objeto.ancho
                    cuadrado.alto=objeto.alto
                    cuadrado.x=objeto.x
                    cuadrado.y=objeto.y
                    cuadrado.borde=objeto.borde
                    cuadrado.colorBorde=objeto.colorBorde
                    cuadrado.anchoBorde=objeto.anchoBorde
                    cuadrado.sombra=objeto.sombra
                    cuadrado.rotar=objeto.rotar
                    cuadrado.oculto=objeto.oculto
                if objeto.__class__==Circulo:
                    circulo=Circulo(self.objetos[self.nivel[2]][0].cuentaObjetos["circulo"])
                    self.objetos[self.nivel[2]][0].cuentaObjetos["circulo"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["circulo"])+1
                    self.objetos[self.puntero].append(circulo)
                    circulo.colorFondo=objeto.colorFondo
                    circulo.transparencia=objeto.transparencia
                    circulo.ancho=objeto.ancho
                    circulo.alto=objeto.alto
                    circulo.x=objeto.x
                    circulo.y=objeto.y
                    circulo.borde=objeto.borde
                    circulo.colorBorde=objeto.colorBorde
                    circulo.anchoBorde=objeto.anchoBorde
                    circulo.sombra=objeto.sombra
                    circulo.rotar=objeto.rotar
                    circulo.oculto=objeto.oculto
                    circulo.radio=objeto.radio
        
                if objeto.__class__==Triangulo:
                    triangulo=Triangulo(self.objetos[self.nivel[2]][0].cuentaObjetos["triangulo"])
                    self.objetos[self.nivel[2]][0].cuentaObjetos["triangulo"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["triangulo"])+1
                    self.objetos[self.puntero].append(triangulo)
                    triangulo.colorFondo=objeto.colorFondo
                    triangulo.transparencia=objeto.transparencia
                    triangulo.ancho=objeto.ancho
                    triangulo.alto=objeto.alto
                    triangulo.x=objeto.x
                    triangulo.y=objeto.y
                    triangulo.borde=objeto.borde
                    triangulo.colorBorde=objeto.colorBorde
                    triangulo.anchoBorde=objeto.anchoBorde
                    triangulo.sombra=objeto.sombra
                    triangulo.rotar=objeto.rotar
                    triangulo.oculto=objeto.oculto
                
                if objeto.__class__==Linea:
                    linea=Linea(self.objetos[self.nivel[2]][0].cuentaObjetos["linea"])
                    self.objetos[self.nivel[2]][0].cuentaObjetos["linea"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["linea"])+1
                    self.objetos[self.puntero].append(linea)
                    linea.ancho=objeto.ancho
                    linea.alto=objeto.alto
                    linea.x=objeto.x
                    linea.y=objeto.y
                    linea.borde=objeto.borde
                    linea.colorBorde=objeto.colorBorde
                    linea.anchoBorde=objeto.anchoBorde
                    linea.rotar=objeto.rotar
                    linea.oculto=objeto.oculto
                
                if objeto.__class__==Imagen:
                    imagen=Imagen(self.objetos[self.nivel[2]][0].cuentaObjetos["imagen"])
                    self.objetos[self.nivel[2]][0].cuentaObjetos["imagen"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["imagen"])+1
                    self.objetos[self.puntero].append(imagen)
                    imagen.colorFondo=objeto.colorFondo
                    imagen.transparencia=objeto.transparencia
                    imagen.ancho=objeto.ancho
                    imagen.alto=objeto.alto
                    imagen.x=objeto.x
                    imagen.y=objeto.y
                    imagen.borde=objeto.borde
                    imagen.colorBorde=objeto.colorBorde
                    imagen.anchoBorde=objeto.anchoBorde
                    imagen.sombra=objeto.sombra
                    imagen.rotar=objeto.rotar
                    imagen.oculto=objeto.oculto
                    imagen.imagen=objeto.imagen
                    imagen.clip=objeto.clip
                
                if objeto.__class__==Texto:
                    texto=Texto(self.objetos[self.nivel[2]][0].cuentaObjetos["texto"])
                    self.objetos[self.nivel[2]][0].cuentaObjetos["texto"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["texto"])+1
                    self.objetos[self.puntero].append(texto)
                    texto.colorFondo=objeto.colorFondo
                    texto.transparencia=objeto.transparencia
                    texto.ancho=objeto.ancho
                    texto.alto=objeto.alto
                    texto.x=objeto.x
                    texto.y=objeto.y
                    texto.borde=objeto.borde
                    texto.colorBorde=objeto.colorBorde
                    texto.anchoBorde=objeto.anchoBorde
                    texto.sombra=objeto.sombra
                    texto.rotar=objeto.rotar
                    texto.oculto=objeto.oculto
                    texto.texto=objeto.texto
                    texto.tamanoTexto=objeto.tamanoTexto
                    texto.colorTexto=objeto.colorTexto
                    texto.fuente=objeto.fuente
                    texto.alineacion=objeto.alineacion
                
                self.actualizaArbol()
                self.EDITADO=0
                self.igu.barraGua.set_sensitive(True)
                self.igu.barraGuc.set_sensitive(True)
                self.igu.gua.set_sensitive(True)
                self.igu.guc.set_sensitive(True)
                self.actulizaLienzo()
            else:
                self.igu.statusbar.push(0, "Imposible Pegar Fuera de Una hoja")
        else:
            self.igu.statusbar.push(0, "Imposible Pegar Fuera de Una hoja")

    def nuevoProyecto(self,widget=None,data=None):
        #Si estamos en linux =)
        if str(os.name)== "posix":
            if self.proyecto!="":
                self.igu.cuadroMensajes("Proyecto Abierto","Ya hay un Proyecto abierto\n por favor cierrelo antes de crear otro",gtk.MESSAGE_WARNING,gtk.BUTTONS_OK)
                return
            #print os.getcwd() muestra la ruta donde se ejecuta el main
            ruta= os.getenv("HOME") #saca la ruta del home del usuario
            dialogo = gtk.FileChooserDialog(title="Crear Nuevo Proyecto",action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
            resp=dialogo.run()
            if resp==gtk.RESPONSE_OK:
                proyecto=str(dialogo.get_filename())
                if os.path.exists(proyecto):
                    md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ya existe un proyecto con este nombre")
                    md.set_title("Error de Creacion de Proyecto")
                    md.run()
                    md.destroy()
                    dialogo.destroy()
                    self.nuevoProyecto()
                else:
                    nmb=proyecto.split("/")
                    self.proyecto=Proyecto(nmb[len(nmb)-1],proyecto)
                    try: #trato de crear las carpetas en el home del usuario
                        os.mkdir(proyecto)
                        os.mkdir(proyecto+"/recursos/")
                        os.mkdir(proyecto+"/recursos/imagenes")
                        os.mkdir(proyecto+"/recursos/sonidos")
                        os.mkdir(proyecto+"/recursos/videos")
                        os.mkdir(proyecto+"/recursos/archivos")
                        os.mkdir(proyecto+"/conf")
                    except:
                        md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ocurrio un error al intentar crear los directorios")
                        md.set_title("Error de Creacion Directorios")
                        md.run()
                        md.destroy()
                        dialogo.destroy()
                        self.igu.statusbar.push("Ocurrio un error al crear los directorios")
                        return
                    try: #trato de copiar los archivos js a las carpetas del proyecto
                        destino=self.proyecto.ruta+"/recursos/jquery.js"
                        origen=os.path.dirname(os.path.realpath(__file__))+"/recursos/js/jquery.js"
                        shutil.copy(origen,destino)
                        destino=self.proyecto.ruta+"/recursos/jquery.timer.js"
                        origen=os.path.dirname(os.path.realpath(__file__))+"/recursos/js/jquery.timer.js"
                        shutil.copy(origen,destino)
                    except:
                        md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ocurrio un error al intentar copiar los archivos javascript")
                        md.set_title("Error de Copiado de Archivos")
                        md.run()
                        md.destroy()
                        dialogo.destroy()
                        self.igu.statusbar.push("Ocurrio un error al copiar los archivos de Javascript")
                        return
                    try: #Trato de escribir el archivo de configuracion del proyecto
                        conf=open(proyecto+"/conf/configuracion.txt","a")
                        conf.write("GCEDV1.0"+"\n")
                        conf.write("0\Hoja0\n")
                        #Listas en Memoria de lo que contiene el proyecto hasta Ahora
                        hoja=Escena(0)
                        conf.write(hoja.propiedades())
                        conf.close()
                    except:
                        md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ocurrio un error crear el archivo de configuracion")
                        md.set_title("Error de Escritura de Archivos")
                        md.run()
                        md.destroy()
                        dialogo.destroy()
                        self.igu.statusbar.push("Ocurrio un error crear el archivo de configuracion")
                        return
                    try: #Trato de escribir el archivo de escritos del proyecto
                        conf=open(proyecto+"/conf/escrito0.gcd","a")
                        conf.write("[s]")
                        conf.close()
                    except:
                        md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ocurrio un error crear el archivo de escritos")
                        md.set_title("Error de Escritura de Archivos")
                        md.run()
                        md.destroy()
                        dialogo.destroy()
                        self.igu.statusbar.push("Ocurrio un error crear el archivo de escritos")
                        return
                    self.objetos.append([hoja])
                    self.recursos.append(["imagenes"])
                    self.recursos.append(["sonidos"])
                    self.recursos.append(["videos"])
                    self.recursos.append(["archivos"])
                    self.actualizaArbol()
                    self.igu.barraHojaNueva.set_sensitive(True)
                    self.igu.barraImagenNuevo.set_sensitive(True)
                    self.igu.barraSonidoNuevo.set_sensitive(True)
                    self.igu.barraVideoNuevo.set_sensitive(True)
                    self.igu.barraArchivoNuevo.set_sensitive(True)
                    self.igu.cer.set_sensitive(True)
                    self.igu.statusbar.push(0,"Se ha creado con Éxito el proyecto")
            else:
                dialogo.destroy()
                self.igu.statusbar.push(0,"Se ha cancelado la creación del proyecto")
            
    
    def actualizaArbol(self):
        almacen = gtk.TreeStore(str,str)
        padre=almacen.append(None,[self.proyecto.nombre,gtk.STOCK_FILE])
        f=almacen.append(padre,["Hojas",gtk.STOCK_DND_MULTIPLE])
        for fila in range(len(self.objetos)):
            x=almacen.append(f,[self.objetos[fila][0].nombre,gtk.STOCK_DND])
            for i in range(len(self.objetos[fila])-1):
                almacen.append(x,[self.objetos[fila][i+1].nombre,gtk.STOCK_FILE])
        f=almacen.append(padre,["Recursos",gtk.STOCK_DIRECTORY])
        
        for fila in self.recursos:
            x=almacen.append(f,[fila[0],gtk.STOCK_OPEN])
            for i in range(len(fila)-1):
                almacen.append(x,[fila[i+1],gtk.STOCK_CDROM])
        self.igu.treeview.set_model(almacen)
        self.igu.treeview.expand_all()
    

    def actulizaLienzo(self,tipo=0):
        marca=""
        pagina="<html><head><script src='"+self.proyecto.ruta+"/recursos/jquery.js'></script><script>$(document).ready(function(){$('.tiempoDiseno').click(function(){document.title='1+'+$(this).attr('id');})})</script></head>"
        if tipo==0:
            for i in range(len(self.objetos[self.puntero])):
                if len(self.nivel)==4 and (self.nivel[3]+1)==i:
                    x=float(self.objetos[self.nivel[2]][self.nivel[3]+1].x)-1
                    y=float(self.objetos[self.nivel[2]][self.nivel[3]+1].y)-1
                    w=float(self.objetos[self.nivel[2]][self.nivel[3]+1].ancho)+1.5
                    h=float(self.objetos[self.nivel[2]][self.nivel[3]+1].alto)+1.5
                    nm=self.objetos[self.nivel[2]][self.nivel[3]+1].nombre
                    if self.objetos[self.nivel[2]][self.nivel[3]+1].oculto=="Falso":
                        marca="<div style='position:absolute;font-size:10pt;top:"+str(y)+"%;left:"+str(x)+"%;border:dashed 2px red;width:"+str(w)+"%;height:"+str(h)+"%'></div>"
                    else:
                        marca="<div style='position:absolute;font-size:10pt;top:"+str(y)+"%;left:"+str(x)+"%;border:dotted 2px black;width:"+str(w)+"%;height:"+str(h)+"%'></div>"
                print self.objetos[self.puntero][i]
                pagina=pagina+self.objetos[self.puntero][i].trazaObjeto(self.proyecto.ruta)
                pagina=pagina+marca
        elif tipo==1:
            recurso= self.recursos[self.nivel[2]][self.nivel[3]+1]
            pagina=pagina+"<img src='"+self.proyecto.ruta+"/recursos/imagenes/"+str(recurso)+"'/>"
        elif tipo==2:
            recurso= self.recursos[self.nivel[2]][self.nivel[3]+1]
            pagina=pagina+"<div><audio id='player' autoplay><source src='"+self.proyecto.ruta+"/recursos/sonidos/"+str(recurso)+"' type='audio/ogg'   preload='none'><source src='"+self.proyecto.ruta+"/recursos/sonidos/"+str(recurso)+"' type='audio/mpeg'   preload='none'><source src='"+self.proyecto.ruta+"/recursos/sonidos/"+str(recurso)+"' type='audio/wav'   preload='none'></audio></div><h3>"+str(recurso)+"</h3><button onclick=\"document.getElementById('player').play();\">Reproducir</button><button onclick=\"document.getElementById('player').pause();document.getElementById('player').currentTime=0;\">Detener</button><button onclick=\"document.getElementById('player').pause()\">Pausa</button><button onclick=\"document.getElementById(\'player\').volume += 0.1;\">Subir Volumen</button><button onclick=\"document.getElementById(\'player\').volume -= 0.1;\">Bajar Volumen</button>"
        elif tipo==3:
            recurso= self.recursos[self.nivel[2]][self.nivel[3]+1]
            pagina=pagina+"<div><video autoplay><source src='"+self.proyecto.ruta+"/recursos/videos/"+str(recurso)+"' type='video/ogg' ><source src='"+self.proyecto.ruta+"/recursos/videos/"+str(recurso)+"' type='video/mp4'></video></div><h3>"+str(recurso)+"</h3>"
        elif tipo==4:
            recurso= self.recursos[self.nivel[2]][self.nivel[3]+1]
            pagina=pagina+"<div><style>@font-face{font-family:'fuente';src: url('"+self.proyecto.ruta+"/recursos/archivos/"+str(recurso)+"')}</style></div><h3 style='font-family:fuente'>El niño Simón Bolívar, Tocaba alegre el tambor, en un patio de granados, que siempre estaban en flor</h3><h4 style='font-family:fuente'>Pero un día se hizo grande, el que fue niño Simón y anduvo por America cuando era Libertador</h4>"

        pagina=pagina+"</body></html>"
        self.igu.lienzo.load_html_string(pagina,"file://"+self.proyecto.ruta+"/")
        
    def guardarProyecto(self,widget=None):
        #Rutina para Escribir el archivo de Configuracion
        if str(os.name)== "posix":
            conf=open(self.proyecto.ruta+"/conf/configuracion.txt","w")
            conf.write("GCEDV1.0"+"\n")
            conf.write("pr\\"+str(self.proyecto.ancho)+"\\"+str(self.proyecto.alto)+"\\"+str(self.proyecto.maximizado)+"\n")
            for fila in range(len(self.objetos)):
                conf.write("0\\"+str(self.objetos[fila][0].nombre)+"\n")
                esc=open(self.proyecto.ruta+"/conf/escrito"+str(fila)+".gcd","w")
                esc.write(self.objetos[fila][0].escritos)
                esc.write("[s]")
                esc.write(self.objetos[fila][0].javascript)
                esc.close()
                #gp=open(self.rutaProyecto+"/app/"+str(self.objetos[fila][0].nombre),"w")
                #gp.write(self.objetos[fila][0].nombre+"\n")
                conf.write(self.objetos[fila][0].propiedades())
                for i in range(len(self.objetos[fila])-1):
                    conf.write(self.objetos[fila][i+1].propiedades())
                #gp.close()
                #conf.write("0\\"+str(self.objetos[fila][0].nombre)+"\n")
            n=0
            for fila in self.recursos:
                n=n+1
                for i in range(len(fila)-1):
                    conf.write(str(n)+"\\"+fila[i+1]+"\n")
            conf.close()
            self.EDITADO=0
            self.igu.barraGua.set_sensitive(False)
            self.igu.barraGuc.set_sensitive(False)
            self.igu.gua.set_sensitive(False)
            self.igu.guc.set_sensitive(False)
   
    def cerrarProyecto(self,widget=None,data=None):
        self.proyecto=""
        del self.recursos[:]
        del self.objetos[:]
        self.EDITADO=0
        self.puntero=-1
        self.nivel=-1
        self.igu.cer.set_sensitive(False)
        ls=self.igu.treeview.get_model()
        ls.clear()
        ls=self.igu.panelPropiedades.get_model()
        ls.clear()
        self.igu.barraRectangulo.set_sensitive(False)
        self.igu.barraCirculo.set_sensitive(False)
        self.igu.barraTriangulo.set_sensitive(False)
        self.igu.barraLinea.set_sensitive(False)
        self.igu.barraImagen.set_sensitive(False)
        self.igu.barraTexto.set_sensitive(False)
        self.igu.barraBoton.set_sensitive(False)
        self.igu.barraCajaTexto.set_sensitive(False)
        self.igu.barraLista.set_sensitive(False)
        self.igu.barraCheck.set_sensitive(False)
        self.igu.barraArea.set_sensitive(False)
        self.igu.barraSon.set_sensitive(False)
        self.igu.barraCla.set_sensitive(False)
        self.igu.barraScr.set_sensitive(False)
        self.igu.barraHojaNueva.set_sensitive(False)
        self.igu.barraImagenNuevo.set_sensitive(False)
        self.igu.barraSonidoNuevo.set_sensitive(False)
        self.igu.barraVideoNuevo.set_sensitive(False)
        self.igu.barraArchivoNuevo.set_sensitive(False)
        self.igu.hojaBienvenida()
        self.igu.statusbar.push(0,"Proyecto Cerrado")
        
    def abrirProyecto(self,widget=None,data=None):
        if self.proyecto!="":
            self.igu.cuadroMensajes("Proyecto Abierto","Ya hay un Proyecto abierto\n por favor cierrelo antes de abrir otro",gtk.MESSAGE_WARNING,gtk.BUTTONS_OK)
            return
        response=self.igu.cuadroDialogo("Abrir Proyecto",gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        if response[0] == gtk.RESPONSE_OK:
            proyecto=str(response[1])+"/conf/configuracion.txt"
            if os.path.isfile(proyecto):
                conf=open(proyecto,"r")
                linea = conf.readline()[:-1]
                if linea!="GCEDV1.0":
                    self.igu.cuadroMensajes("Error Apertura de Proyecto","Este no es un Proyecto de CED",gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE)
                    return
                nmb=response[1].split("/")
                self.proyecto=Proyecto(nmb[len(nmb)-1],response[1])
                #self.rutaProyecto=
                #self.nombreProyecto=response[1]
                self.recursos.append(["imagenes"])
                self.recursos.append(["sonidos"])
                self.recursos.append(["videos"])
                self.recursos.append(["archivos"])
                i=0
                ind=-1
                while linea != "":
                    linea = conf.readline()[:-1]
                    x=linea.split("\\")
                    if x[0]=="pr":
                        self.proyecto.ancho=x[1]
                        self.proyecto.alto=x[2]
                        self.proyecto.maximizado=x[3]
                    if x[0]=="0":
                        hoja=Escena(len(self.objetos))
                        ind=ind+1
                        self.proyecto.paginas.append("")
                    if x[0]=="p":
                        hoja.colorFondo=x[1]
                        hoja.transparencia=x[2]
                        hoja.imagen=x[3]
                        hoja.ajusteImagen=x[4]
                        esc=open(self.proyecto.ruta+"/conf/escrito"+str(ind)+".gcd","r")
                        contenido=esc.read()
                        dupla=contenido.split("[s]")
                        esc.close()
                        hoja.escritos=dupla[0]
                        hoja.javascript=dupla[1]
                        self.objetos.append([hoja])
                    if x[0]=="c":
                        obj=Cuadro(self.objetos[ind][0].cuentaObjetos["cuadro"])
                        self.objetos[ind][0].cuentaObjetos["cuadro"]=int(self.objetos[ind][0].cuentaObjetos["cuadro"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.borde=x[7]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="o":
                        obj=Circulo(self.objetos[ind][0].cuentaObjetos["circulo"])
                        self.objetos[ind][0].cuentaObjetos["circulo"]=int(self.objetos[ind][0].cuentaObjetos["circulo"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.borde=x[7]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.radio=x[15]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="t":
                        obj=Triangulo(self.objetos[ind][0].cuentaObjetos["triangulo"])
                        self.objetos[ind][0].cuentaObjetos["triangulo"]=int(self.objetos[ind][0].cuentaObjetos["triangulo"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.borde=x[7]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="i":
                        obj=Imagen(self.objetos[ind][0].cuentaObjetos["imagen"])
                        self.objetos[ind][0].cuentaObjetos["imagen"]=int(self.objetos[ind][0].cuentaObjetos["imagen"])+1
                        obj.transparencia=x[1]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.borde=x[7]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.imagen=x[15]
                        obj.clip=x[16]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="l":
                        obj=Linea(self.objetos[ind][0].cuentaObjetos["linea"])
                        self.objetos[ind][0].cuentaObjetos["linea"]=int(self.objetos[ind][0].cuentaObjetos["linea"])+1
                        obj.ancho=x[3]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.borde=x[7]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra==x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                        
                    if x[0]=="x":
                        obj=Texto(self.objetos[ind][0].cuentaObjetos["texto"])
                        self.objetos[ind][0].cuentaObjetos["texto"]=int(self.objetos[ind][0].cuentaObjetos["texto"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.borde=x[7]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.texto=x[15]
                        obj.tamanoTexto=x[16]
                        obj.colorTexto=x[17]
                        obj.fuente=x[18]
                        obj.alineacion=x[19]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="b":
                        obj=Boton(self.objetos[ind][0].cuentaObjetos["boton"])
                        self.objetos[ind][0].cuentaObjetos["boton"]=int(self.objetos[ind][0].cuentaObjetos["boton"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.texto=x[15]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="e":
                        obj=Entrada(self.objetos[ind][0].cuentaObjetos["entrada"])
                        self.objetos[ind][0].cuentaObjetos["entrada"]=int(self.objetos[ind][0].cuentaObjetos["entrada"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.texto=x[15]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="s":
                        obj=Lista(self.objetos[ind][0].cuentaObjetos["lista"])
                        self.objetos[ind][0].cuentaObjetos["lista"]=int(self.objetos[ind][0].cuentaObjetos["lista"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.lista=x[15]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="k":
                        obj=Check(self.objetos[ind][0].cuentaObjetos["check"])
                        self.objetos[ind][0].cuentaObjetos["check"]=int(self.objetos[ind][0].cuentaObjetos["check"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.valor=x[15]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="r":
                        obj=Area(self.objetos[ind][0].cuentaObjetos["area"])
                        self.objetos[ind][0].cuentaObjetos["area"]=int(self.objetos[ind][0].cuentaObjetos["area"])+1
                        obj.colorFondo=x[1]
                        obj.transparencia=x[2]
                        obj.ancho=x[3]
                        obj.alto=x[4]
                        obj.x=x[5]
                        obj.y=x[6]
                        obj.colorBorde=x[8]
                        obj.anchoBorde=x[9]
                        obj.sombra=x[10]
                        obj.rotar=x[11]
                        obj.oculto=x[12]
                        obj.texto=x[15]
                        obj.tip=x[13]
                        obj.etiqueta=x[14]
                        self.objetos[ind].append(obj)
                    if x[0]=="m":
                        obj=Sonido(self.objetos[ind][0].cuentaObjetos["sonido"])
                        self.objetos[ind][0].cuentaObjetos["sonido"]=int(self.objetos[ind][0].cuentaObjetos["sonido"])+1
                        obj.sonido=x[15]
                        self.objetos[ind].append(obj)
                    if x[0]=="1":
                        self.recursos[0].append(x[1])
                    if x[0]=="2":
                        self.recursos[1].append(x[1])
                    if x[0]=="3":
                        self.recursos[2].append(x[1])
                    if x[0]=="4":
                        self.recursos[3].append(x[1])
                conf.close()
                self.actualizaArbol()
                self.igu.barraHojaNueva.set_sensitive(True)
                self.igu.barraImagenNuevo.set_sensitive(True)
                self.igu.barraSonidoNuevo.set_sensitive(True)
                self.igu.barraVideoNuevo.set_sensitive(True)
                self.igu.barraArchivoNuevo.set_sensitive(True)
                self.igu.cer.set_sensitive(True)
            else:
                self.igu.cuadroMensajes("Error Apertura de Proyecto","Este no es un Proyecto de CED",gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE)
        elif response[0] == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
     
    def insertarHoja(self,widget=None,data=None):
        #Insertamos una nueva hoja al proyecto
        if self.proyecto!="":
            hoja=Escena(str(len(self.objetos)))
            self.objetos.append([hoja])
            conf=open(self.proyecto.ruta+"/conf/escrito"+str(len(self.objetos)-1)+".gcd","a")
            conf.write("[s]")
            conf.close()
            self.actualizaArbol()
            self.igu.barraGua.set_sensitive(True)
            self.igu.barraGuc.set_sensitive(True)
            self.igu.gua.set_sensitive(True)
            self.igu.guc.set_sensitive(True)
            self.proyecto.paginas.append("")
            self.EDITADO=1
        else:
            self.igu.statusbar.push(0,"No hay proyecto para insertar Hojas")
    
    def insertarObjeto(self,widget=None,data=None):
        #Insertamos los objetos
        if self.proyecto=="":
            self.igu.statusbar.push(0,"No hay proyecto para insertar objetos")
            return
        if data==0:
            cuadrado=Cuadro(self.objetos[self.nivel[2]][0].cuentaObjetos["cuadro"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["cuadro"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["cuadro"])+1
            self.objetos[self.puntero].append(cuadrado)
            self.igu.statusbar.push(0,"Insertamos un cuadrado o rectangulo")
        if data==1:
            circulo=Circulo(self.objetos[self.nivel[2]][0].cuentaObjetos["circulo"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["circulo"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["circulo"])+1
            self.objetos[self.puntero].append(circulo)
            self.igu.statusbar.push(0,"Insertamos un circulo")
        if data==2:
            triangulo=Triangulo(self.objetos[self.nivel[2]][0].cuentaObjetos["triangulo"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["triangulo"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["triangulo"])+1
            self.objetos[self.puntero].append(triangulo)
            self.igu.statusbar.push(0,"Insertamos un triangulo")
        if data==3:
            linea=Linea(self.objetos[self.nivel[2]][0].cuentaObjetos["linea"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["linea"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["linea"])+1
            self.objetos[self.puntero].append(linea)
            self.igu.statusbar.push(0,"Insertamos una linea")
        if data==4:
            imagen=Imagen(self.objetos[self.nivel[2]][0].cuentaObjetos["imagen"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["imagen"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["imagen"])+1
            self.objetos[self.puntero].append(imagen)
            self.igu.statusbar.push(0,"Insertamos una imagen")
        if data==5:
            txt=Texto(self.objetos[self.nivel[2]][0].cuentaObjetos["texto"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["texto"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["texto"])+1
            self.objetos[self.puntero].append(txt)
            self.igu.statusbar.push(0,"Insertamos un texto")
        if data==6:
            btn=Boton(self.objetos[self.nivel[2]][0].cuentaObjetos["boton"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["boton"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["boton"])+1
            self.objetos[self.puntero].append(btn)
            self.igu.statusbar.push(0,"Insertamos un Boton")
        if data==7:
            cja=Entrada(self.objetos[self.nivel[2]][0].cuentaObjetos["entrada"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["entrada"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["entrada"])+1
            self.objetos[self.puntero].append(cja)
            self.igu.statusbar.push(0,"Insertamos una Caja de Texto")
        if data==8:
            lst=Lista(self.objetos[self.nivel[2]][0].cuentaObjetos["lista"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["lista"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["lista"])+1
            self.objetos[self.puntero].append(lst)
            self.igu.statusbar.push(0,"Insertamos una Lista Desplegable")
        if data==9:
            chk=Check(self.objetos[self.nivel[2]][0].cuentaObjetos["check"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["check"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["check"])+1
            self.objetos[self.puntero].append(chk)
            self.igu.statusbar.push(0,"Insertamos una Caja de Chequeo")
        if data==10:
            cja=Area(self.objetos[self.nivel[2]][0].cuentaObjetos["area"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["area"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["area"])+1
            self.objetos[self.puntero].append(cja)
            self.igu.statusbar.push(0,"Insertamos un Area de Edicion")
        if data==11:
            sonido=Sonido(self.objetos[self.nivel[2]][0].cuentaObjetos["sonido"])
            self.objetos[self.nivel[2]][0].cuentaObjetos["sonido"]=int(self.objetos[self.nivel[2]][0].cuentaObjetos["sonido"])+1
            self.objetos[self.puntero].append(sonido)
            self.igu.statusbar.push(0,"Insertamos un Sonido")
        if data==13:
            obj=[]
            for i in range(len(self.objetos[self.puntero])):
                obj.append(self.objetos[self.puntero][i])
            #self.igu.cuadroDialogoScript(obj)
            editorEscritos=Analizador(obj,self.recursos)
        self.actualizaArbol()
        self.EDITADO=0
        self.igu.barraGua.set_sensitive(True)
        self.igu.barraGuc.set_sensitive(True)
        self.igu.gua.set_sensitive(True)
        self.igu.guc.set_sensitive(True)
        self.actulizaLienzo()
    
    def insertarRecurso(self,widget=None,data=None):
        if self.proyecto=="":
            self.igu.statusbar.push(0,"No hay proyecto para insertar Recursos")
            return
        dialog = gtk.FileChooserDialog(title="Insertar Recurso",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        dialog.set_filename(os.path.dirname(os.path.realpath(__file__))+"/recursos")
        filtro = gtk.FileFilter()
        if data==0:
            filtro.set_name("Images")
            filtro.add_pattern("*.png")
            filtro.add_pattern("*.jpg")
            filtro.add_pattern("*.gif")
            filtro.add_pattern("*.GIF")
            filtro.add_pattern("*.JPG")
            filtro.add_pattern("*.PNG")
        elif data==1:
            filtro.set_name("Sonidos")
            filtro.add_pattern("*.wav")
            filtro.add_pattern("*.ogg")
            filtro.add_pattern("*.mp3")
        elif data==2:
            filtro.set_name("Videos")
            filtro.add_pattern("*.ogg")
            filtro.add_pattern("*.mp4")
        elif data==3:
            filtro.set_name("Archivos")
            filtro.add_pattern("*.*")
        dialog.add_filter(filtro)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            if data==0:
                e=dialog.get_filename().split("/")
                archivo=e[len(e)-1]
                destino=self.proyecto.ruta+"/recursos/imagenes/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
            elif data==1:
                e=dialog.get_filename().split("/")
                archivo=e[len(e)-1]
                destino=self.proyecto.ruta+"/recursos/sonidos/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
            elif data==2:
                e=dialog.get_filename().split("/")
                archivo=e[len(e)-1]
                destino=self.proyecto.ruta+"/recursos/videos/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
            elif data==3:
                e=dialog.get_filename().split("/")
                archivo=e[len(e)-1]
                destino=self.proyecto.ruta+"/recursos/archivos/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
            self.recursos[data].append(archivo)
            self.actualizaArbol()
            self.guardarProyecto()
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        dialog.destroy()
    
    def punteroArbol(self,widget=None,data=None):
        (mod,ite)= self.igu.selFila.get_selected_rows()
        #self.igu.statusbar.push(0,"El iterador tiene "+str(len(x))+" elementos")
        self.nivel=ite[0]
        if len(self.nivel)==1:
            self.igu.barraRectangulo.set_sensitive(False)
            self.igu.barraCirculo.set_sensitive(False)
            self.igu.barraTriangulo.set_sensitive(False)
            self.igu.barraLinea.set_sensitive(False)
            self.igu.barraImagen.set_sensitive(False)
            self.igu.barraTexto.set_sensitive(False)
            self.igu.barraBoton.set_sensitive(False)
            self.igu.barraCajaTexto.set_sensitive(False)
            self.igu.barraLista.set_sensitive(False)
            self.igu.barraCheck.set_sensitive(False)
            self.igu.barraArea.set_sensitive(False)
            self.igu.barraSon.set_sensitive(False)
            self.igu.barraCla.set_sensitive(False)
            self.igu.barraScr.set_sensitive(False)
            self.igu.statusbar.push(0,"Estas en el Proyecto")
            self.actualizaVistaPropiedades(self.proyecto)
        if len(self.nivel)==3:
            if self.nivel[1]==0:
                self.igu.statusbar.push(0,"Propíedad de la hoja"+str(self.nivel[2])+" el puntero es:"+str(self.nivel[2]))
                self.puntero=self.nivel[2]
                self.igu.barraRectangulo.set_sensitive(True)
                self.igu.barraCirculo.set_sensitive(True)
                self.igu.barraTriangulo.set_sensitive(True)
                self.igu.barraLinea.set_sensitive(True)
                self.igu.barraImagen.set_sensitive(True)
                self.igu.barraTexto.set_sensitive(True)
                self.igu.barraBoton.set_sensitive(True)
                self.igu.barraCajaTexto.set_sensitive(True)
                self.igu.barraLista.set_sensitive(True)
                self.igu.barraCheck.set_sensitive(True)
                self.igu.barraArea.set_sensitive(True)
                self.igu.barraSon.set_sensitive(True)
                self.igu.barraCla.set_sensitive(True)
                self.igu.barraScr.set_sensitive(True)
                self.actualizaVistaPropiedades(self.objetos[self.nivel[2]][0])
                self.__elimi=True
        elif len(self.nivel)==4:
            if self.nivel[1]==0:
                self.igu.barraRectangulo.set_sensitive(False)
                self.igu.barraCirculo.set_sensitive(False)
                self.igu.barraTriangulo.set_sensitive(False)
                self.igu.barraLinea.set_sensitive(False)
                self.igu.barraImagen.set_sensitive(False)
                self.igu.barraTexto.set_sensitive(False)
                self.igu.barraBoton.set_sensitive(False)
                self.igu.barraCajaTexto.set_sensitive(False)
                self.igu.barraLista.set_sensitive(False)
                self.igu.barraCheck.set_sensitive(False)
                self.igu.barraArea.set_sensitive(False)
                self.igu.barraSon.set_sensitive(False)
                self.igu.barraCla.set_sensitive(False)
                self.igu.barraScr.set_sensitive(False)
                self.puntero=self.nivel[2]
                #print self.objetos[self.nivel[2]][self.nivel[3]+1]
                #print self.igu.lienzo.get_main_frame().get_title()
                self.actualizaVistaPropiedades(self.objetos[self.nivel[2]][self.nivel[3]+1])
                self.__elimi=True
                #self.igu.statusbar.push(0,"Propíedad de los objetos de la hoja"+str(self.nivel[2])+"-"+str(self.nivel))
            if self.nivel[1]==1:
                if self.nivel[2]==0:
                    self.igu.statusbar.push(0,"Imagenes")
                    self.actulizaLienzo(1)
                    self.__elimi=True
                if self.nivel[2]==1:
                    self.igu.statusbar.push(0,"sonidos")
                    self.actulizaLienzo(2)
                    self.__elimi=True
                if self.nivel[2]==2:
                    self.igu.statusbar.push(0,"videos")
                    self.actulizaLienzo(3)
                    self.__elimi=True
                if self.nivel[2]==3:
                    self.igu.statusbar.push(0,"Archivos")
                    self.actulizaLienzo(4)
                    self.__elimi=True
        else:
            self.__elimi=False
            
        #self.actualizaVistaPropiedades()
    def llenaListas(self,tipoLista):
        lista = gtk.ListStore(str)
        if tipoLista==1:
            colores=[("Negro","#000000"),("Gris Oscuro","#696969"),("Gris","#808080"),("Gris Claro","#A9A9A9"),("Blanco","#FFFFFF"),("Rojo Oscuro","#8B0000"),("Rojo","#FF0000"),("Rojo Claro","#FA8072"),("Rosado Oscuro","#FF1493"),("Rosado","#FF69B4"),("Rosado Claro","#FFB6C1"),("Fucsia Oscuro","#8A2BE2"),("Fucsia","#FF00FF"),("Fucsia Claro","#CD5C5C"),("Marron Oscuro","#800000"),("Marron","#8B4513"),("Marron Claro","#A0522D"),("Naranja Oscuro","#FF8C00"),("Naranja","#FF4500"),("Naranja Claro","#FF6347"),("Purpura Oscuro","#4B0082"),("Purupura","#800080"),("Purpura Claro","#EE82EE"),("Amarillo Oscuro","#FFD700"),("Amarillo","#FFFF00"),("Amarillo Claro","#F0E68C"),("Teal","#008080"),("Azul Oscuro","#000080"),("Azul","#0000FF"),("Azul Claro","#00BFFF"),("AguaMarina Oscuro","#1E90FF"),("AguaMarina","#00FFFF"),("AguaMarina Claro","#00BFFF"),("Verde Oscuro","#006400"),("Verde","#008000"),("Verde Claro","#3CB371"),("Lima","#00FF00"),("Oliva Oscuro","#556B2F"),("Oliva","#808000"),("Oliva Claro","#BDB76B")]
            for i in range(len(colores)):
                lista.append([colores[i][0]])
        if tipoLista==2:
            x=0.0
            lista.append([x])
            for i in range(33):
                x=x+0.03
                lista.append([x])
            lista.append([1.0])
        if tipoLista==3:
            lista.append(["Verdadero"])
            lista.append(["Falso"])
        if tipoLista==4:
            lista.append(["Verdadero"])
            lista.append(["Falso"])
        if tipoLista==5:
            x=0
            lista.append([x])
            for i in range(100):
                x=x+1
                lista.append([x])
        if tipoLista==6:
            bordes=[("punteado","dotted"),("discontinuo","dashed"),("solido","solid"),("doble","double"),("acanalado","groove"),("corrugado","ridge"),("relieve bajo","inset"),("relieve alto","outset")]
            for i in range(len(bordes)):
                lista.append([bordes[i][0]])
        if tipoLista==7:
            x=0
            lista.append([x])
            for i in range(360):
                x=x+1
                lista.append([x])
        if tipoLista==8:
            lista.append(["None"])
            for fila in range(len(self.recursos[0])-1):
                lista.append([self.recursos[0][fila+1]])
        if tipoLista==9:
            lista.append(["Courier"])
            for fila in range(len(self.recursos[3])-1):
                lista.append([self.recursos[3][fila+1]])
        if tipoLista==10:
            lista.append(["None"])
            for fila in range(len(self.recursos[1])-1):
                lista.append([self.recursos[1][fila+1]])
        return lista
    
    def actualizaVistaPropiedades(self,objeto):
        almacen = gtk.ListStore(str,str,gtk.TreeModel)
        self.igu.statusbar.push(0,str(objeto.nombre))
        almacen.clear()
        if objeto.__class__== Escena:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["imagen",objeto.imagen,self.llenaListas(8)])
            almacen.append(["ajusteImagen",objeto.ajusteImagen,self.llenaListas(3)])
        
        if objeto.__class__==Cuadro:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        if objeto.__class__==Circulo:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["radio",objeto.radio,self.llenaListas(7)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        if objeto.__class__==Triangulo:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        if objeto.__class__==Linea:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        if objeto.__class__==Imagen:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["imagen",objeto.imagen,self.llenaListas(8)])
            almacen.append(["clip",objeto.clip,self.llenaListas(4)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        
        if objeto.__class__==Texto:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["texto",objeto.texto,self.llenaListas(4)])
            almacen.append(["tamanoTexto",objeto.tamanoTexto,self.llenaListas(5)])
            almacen.append(["colorTexto",objeto.colorTexto,self.llenaListas(1)])
            almacen.append(["fuente",objeto.fuente,self.llenaListas(9)])
            almacen.append(["alineacion",objeto.alineacion,self.llenaListas(4)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        if objeto.__class__==Boton:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["texto",objeto.texto,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
       
        if objeto.__class__==Entrada:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["texto",objeto.texto,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
            
        if objeto.__class__==Lista:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["lista",objeto.lista,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
            
        if objeto.__class__==Check:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["valor",objeto.valor,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
            
        if objeto.__class__==Area:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["texto",objeto.texto,self.llenaListas(4)])
            almacen.append(["colorFondo",objeto.colorFondo,self.llenaListas(1)])
            almacen.append(["transparencia",objeto.transparencia,self.llenaListas(2)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(5)])
            almacen.append(["alto",objeto.alto,self.llenaListas(5)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["colorBorde",objeto.colorBorde,self.llenaListas(1)])
            almacen.append(["anchoBorde",objeto.anchoBorde,self.llenaListas(5)])
            almacen.append(["sombra",objeto.sombra,self.llenaListas(4)])
            almacen.append(["rotar",objeto.rotar,self.llenaListas(7)])
            almacen.append(["oculto",objeto.oculto,self.llenaListas(3)])
            almacen.append(["tip",objeto.tip,self.llenaListas(4)])
            almacen.append(["etiqueta",objeto.etiqueta,self.llenaListas(4)])
        
        if objeto.__class__==Sonido:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["sonido",objeto.sonido,self.llenaListas(10)])
        
        if objeto.__class__==Proyecto:
            almacen.append(["ruta",objeto.ruta,self.llenaListas(4)])
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(4)])
            almacen.append(["alto",objeto.alto,self.llenaListas(4)])
            almacen.append(["maximizado",objeto.maximizado,self.llenaListas(3)])
        
        
        
        self.igu.panelPropiedades.set_model(almacen)
        self.actulizaLienzo()
    
    def eliminarObjetos(self,widget):
        if self.proyecto=="":
            self.igu.statusbar.push(0,"¿Qué Intentas Eliminar?")
            return
        if self.__elimi==True:
            respuesta=self.igu.cuadroMensajes("Confirmar Eliminar Objeto","Esta Seguro de Eliminar Este Objeto",gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO)
            if respuesta==gtk.RESPONSE_YES:
                modelo = self.igu.treeview.get_model()
                if len(self.nivel)==3:
                    if self.nivel[1]==0:
                        print "Eliminar la Hoja"+str(self.puntero)
                        del self.objetos[self.puntero]
                        del self.proyecto.paginas[self.puntero]
                        self.actualizaArbol()
                elif len(self.nivel)==4:
                    if self.nivel[1]==0:
                        #print "Eliminar Objeto"+str(self.nivel[3])+" de la Hoja"+str(self.nivel[2])
                        texto= "El tipo de objeto a Eliminar es: "+self.objetos[self.nivel[2]][self.nivel[3]+1].nombre
                        del self.objetos[self.nivel[2]][self.nivel[3]+1]
                        self.actualizaArbol()
                        try:
                            self.actualizaVistaPropiedades(self.objetos[self.nivel[2]][self.nivel[3]+1])
                        except IndexError,e:
                            print e
                            self.actualizaVistaPropiedades(self.objetos[self.nivel[2]][self.nivel[3]])
                    if self.nivel[1]==1:
                        recurso= self.recursos[self.nivel[2]][self.nivel[3]+1]
                        a=self.igu.cuadroMensajes("Confirmar Eliminar Objeto","Esta Seguro de Eliminar Este Objeto ("+str(recurso)+")",gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO)
                        if a==gtk.RESPONSE_YES:
                            if self.nivel[2]==0:
                                os.remove(self.proyecto.ruta+"/recursos/imagenes/"+str(recurso))
                            if self.nivel[2]==1:
                                os.remove(self.proyecto.ruta+"/recursos/sonidos/"+str(recurso))
                            if self.nivel[2]==2:
                                os.remove(self.proyecto.ruta+"/recursos/videos/"+str(recurso))
                            if self.nivel[2]==3:
                                os.remove(self.proyecto.ruta+"/recursos/archivos/"+str(recurso))
                            del self.recursos[self.nivel[2]][self.nivel[3]+1]
                            self.actualizaArbol()
        self.__elimi=False
        self.igu.barraGua.set_sensitive(True)
        self.igu.barraGuc.set_sensitive(True)
        self.igu.gua.set_sensitive(True)
        self.igu.guc.set_sensitive(True)
        texto ="Se ha Eliminado "+str(recurso)
        self.igu.statusbar.push(0,texto)
    
    def _cambiaAtributo( self,widget, fila, valor, columna):
        modelo = self.igu.panelPropiedades.get_model()
        modelo[fila][columna] = valor
        atributo=modelo[fila][0]
        if len(self.nivel)==3:
            s=self.objetos[self.puntero][0].__dict__
        if len(self.nivel)==4:
            s=self.objetos[self.puntero][self.nivel[3]+1].__dict__
        if len(self.nivel)==1:
            s=self.proyecto.__dict__
        s[atributo]=valor
        self.actulizaLienzo()
        self.EDITADO=1
        self.igu.barraGua.set_sensitive(True)
        self.igu.barraGuc.set_sensitive(True)
        self.igu.gua.set_sensitive(True)
        self.igu.guc.set_sensitive(True)
        
