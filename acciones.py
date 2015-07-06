# -*- coding: utf-8 -*-
import sys
import glib,gtk
import shutil
import os, stat,tarfile,json
from objetos import *
from analizador import *
class Acciones:
    
    def __init__(self,IGU):
        self.proyecto=None
        self.objetos={"Proyecto":{"ancho":640,"alto":480,"maximizado":"Falso"},"Hojas":[],"Imagenes":[],"Sonidos":[],"Videos":[],"Archivos":[]}
        self.seleccionado=None
        self.EDITADO=0
        self.puntero=-1
        self.nivel=-1
        self.igu=IGU
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
        self.igu.imF.connect("activate",self.importarFuente)
        self.igu.imE.connect("activate",self.importarExportado)
        
        self.igu.gaI.connect("activate",self.verImagenes,None)
        
        self.igu.lienzo.connect("key-press-event",self.presionaTecla)
        self.igu.lienzo.connect("button-press-event",self.presionaRaton)
        self.igu.lienzo.connect('title-changed',self.cambiaTitulo)
    
    def importarExportado(self,widget,data=None):
        if self.proyecto=="":
            self.igu.cuadroMensajes("Proyecto Cerrado","Debe Abrir un proyecto primero antes de importar",gtk.MESSAGE_WARNING,gtk.BUTTONS_OK)
            return
        response=self.igu.cuadroDialogo("Abrir Proyecto",gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        if response[0] == gtk.RESPONSE_OK:
            proyecto=str(response[1])+"/main.py"
            self.igu.cuadroMensajes("Error Importacion de Proyecto Importado","Este metodo aun esta por implementacion",gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE)
    
    def importarFuente(self,widget,data=None):
        if self.proyecto=="":
            self.igu.cuadroMensajes("Proyecto Cerrado","Debe Abrir un proyecto primero antes de importar",gtk.MESSAGE_WARNING,gtk.BUTTONS_OK)
            return
        response=self.igu.cuadroDialogo("Abrir Proyecto",gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        if response[0] == gtk.RESPONSE_OK:
            proyecto=str(response[1])+"/conf/configuracion.txt"
            if os.path.isfile(proyecto):
                conf=open(proyecto,"r")
                linea = conf.readline()[:-1]
                if linea!="GCEDV1.0":
                    self.igu.cuadroMensajes("Error Importacion de Proyecto Fuente","Este no es un Proyecto de CED",gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE)
                    return
                nmb=response[1].split("/")
                importado=nmb[len(nmb)-1]
                rtnmb=response[1]
                if importado==self.proyecto.nombre:
                    self.igu.cuadroMensajes("Error Importacion de Proyecto Fuente","No se puede importar un proyecto sobre si mismo",gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE)
                    conf.close()
                    return
                i=0
                ind=len(self.objetos)-1
                print ind
                print self.objetos
                while linea != "":
                    linea = conf.readline()[:-1]
                    x=linea.split("\\")
                    if x[0]=="pr":
                        continue
                    if x[0]=="0":
                        hoja=Escena(len(self.objetos))
                        ind=ind+1
                        #self.proyecto.paginas.append("")
                    if x[0]=="p":
                        hoja.colorFondo=x[1]
                        hoja.transparencia=x[2]
                        hoja.imagen=x[3]
                        hoja.ajusteImagen=x[4]
                        esc=open(rtnmb+"/conf/escrito"+str(ind-len(self.objetos))+".gcd","r")
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
                        destino=self.proyecto.ruta+"/recursos/imagenes/"+x[1]
                        origen=rtnmb+"/recursos/imagenes/"+x[1]
                        shutil.copy(origen,destino)
                    if x[0]=="2":
                        self.recursos[1].append(x[1])
                        destino=self.proyecto.ruta+"/recursos/sonidos/"+x[1]
                        origen=rtnmb+"/recursos/sonidos/"+x[1]
                        shutil.copy(origen,destino)
                    if x[0]=="3":
                        self.recursos[2].append(x[1])
                        destino=self.proyecto.ruta+"/recursos/videos/"+x[1]
                        origen=rtnmb+"/recursos/videos/"+x[1]
                        shutil.copy(origen,destino)
                    if x[0]=="4":
                        self.recursos[3].append(x[1])
                        destino=self.proyecto.ruta+"/recursos/archivos/"+x[1]
                        origen=rtnmb+"/recursos/archivos/"+x[1]
                        shutil.copy(origen,destino)
                conf.close()
                self.actualizaArbol()
                self.igu.barraHojaNueva.set_sensitive(True)
                self.igu.barraImagenNuevo.set_sensitive(True)
                self.igu.barraSonidoNuevo.set_sensitive(True)
                self.igu.barraVideoNuevo.set_sensitive(True)
                self.igu.barraArchivoNuevo.set_sensitive(True)
                self.igu.cer.set_sensitive(True)
                self.igu.statusbar.push(0,"Fuente del Protecto Importado con Exito")
            else:
                self.igu.cuadroMensajes("Error Apertura de Proyecto","Este no es un Proyecto de CED",gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE)
        elif response[0] == gtk.RESPONSE_CANCEL:
            self.igu.statusbar.push(0,"No se Importo proyecto. Cancelado")
    
    
    def verImagenes(self,widget,accion):
        if accion==None:
            pagina="<html><head><script>function cf(id){document.title=id}</script></head><body><h1>Categorias de Imagenes</h1>"
            for (path,directory,archivos) in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)),"recursos/imagenes")):
                categoria=path.split("GenCED")
                categoria= categoria[1].split("/")
                if len(categoria)>3:
                    pagina+="<div style='width:10%;height:10%;margin-left:1%;margin-bottom:8%;float:left;text-align:center'><img src='"+os.path.dirname(os.path.realpath(__file__))+"/iconos/carpeta.png' style='display:block;width:90%;height;65%;margin-bottom:5%' onclick='cf(this.id)' id='0+"+str(categoria[3])+"'/>"+str(categoria[3])+"</div>"
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
        if self.proyecto==None:
            self.igu.statusbar.push(0,"¿Cuál Proyecto vas a Ejecutar?")
            return
        self.proyecto.paginas[:]=[]
        rutaTemporal=str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre
        i=0
        for d in self.objetos["Hojas"]:
            pagina="<html><head><script src='"+rutaTemporal+"/recursos/jquery.js'></script><script type='text/javascript' src='"+rutaTemporal+"/recursos/jquery.timer.js'></script></head>"
            pagina+=d["objeto"].trazaObjeto(rutaTemporal)
            for e in self.objetos["Hojas"][i]["hijos"]:
                pagina+= e["objeto"].trazaObjeto(rutaTemporal)
            pagina=pagina+"</body></html>"
            print pagina
            self.proyecto.paginas.append(pagina)
            pagina=""
            i+=1
        self.proyecto.ejecutar()

    def presionaTecla(self,widget,event):
        keycode = gtk.gdk.keyval_to_upper(event.keyval)
        #65362 up,65364 dw,65361 lf,65363 rg
        if self.seleccionado!=None:
            if keycode==65361:
                self.seleccionado.x=float(self.seleccionado.x)-0.2
            if keycode==65362:
                self.seleccionado.y=float(self.seleccionado.y)-0.2
            if keycode==65363:
                self.seleccionado.x=float(self.seleccionado.x)+0.2
            if keycode==65364:
                self.seleccionado.y=float(self.seleccionado.y)+0.2
            self.actualizaVistaPropiedades()
            self.actulizaLienzo()
        #print keycode
    
    def presionaRaton(self,widget,event):
        assert event.type == gtk.gdk.BUTTON_PRESS
        f=widget.get_main_frame()
        print f.__dict__
        self.igu.statusbar.push(0, 'Clicked at x={0}, y={1}'.format(event.x, event.y))
        #self.igu.cuadroDialogoScript()
        #self.igu.lienzo.execute_script('tag= window.document.element.nodeName;alert("El elemento selecionado ha sido " + tag);')
        
        """"doc = widget.get_dom_document()
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
            i=0
            for d in self.objetos["Hojas"]:
                if self.puntero==i:
                    j=0
                    for e in self.objetos["Hojas"][i]["hijos"]:
                        if e["objeto"].nombre==variables[1]:
                            self.seleccionado=e["objeto"]
                            self.actualizaVistaPropiedades()
                            self.igu.treeview.expand_all()
                            self.igu.treeview.set_cursor((0,0,self.puntero,j))
                            break
                        j+=1
                    break
                i+=1
                
        elif variables[0]=='2':
            pagina="<html><head><title></title></head>"
            pagina=pagina+"<img src='"+os.path.dirname(os.path.realpath(__file__))+"/recursos/imagenes/"+str(variables[1])+"/"+str(variables[2])+"'/>"
            if self.proyecto!="":
                pagina+="<button onclick='document.title=\"3+"+str(variables[1])+"/"+str(variables[2])+"\"'>Insertar al Proyecto</button>"
                
            pagina=pagina+"</body></html>"
            self.igu.lienzo.load_html_string(pagina,"file://"+os.path.dirname(os.path.realpath(__file__))+"/")
        elif variables[0]=='3':
            if self.proyecto=="":
                self.igu.statusbar.push(0,"No hay Proyecto Abierto");
            else:
                archivo=variables[1]
                par=variables[1].split("/")[1]
                destino=str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre+"/recursos/imagenes/"+par
                origen=os.path.dirname(os.path.realpath(__file__))+"/recursos/imagenes/"+str(variables[1])
                shutil.copy(origen,destino)
                self.objetos["Imagenes"].append(str(par))
                self.actualizaArbol()
                self.igu.statusbar.push(0,"Insertada la Imagen "+str(par));
                self.igu.barraGua.set_sensitive(True)
                self.igu.barraGuc.set_sensitive(True)
                self.igu.gua.set_sensitive(True)
                self.igu.guc.set_sensitive(True)
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
        self.igu.barraRectangulo.connect("clicked",self.insertarObjeto,"cuadro")
        self.igu.barraCirculo.connect("clicked",self.insertarObjeto,"circulo")
        self.igu.barraTriangulo.connect("clicked",self.insertarObjeto,"triangulo")
        self.igu.barraLinea.connect("clicked",self.insertarObjeto,"linea")
        self.igu.barraImagen.connect("clicked",self.insertarObjeto,"imagen")
        self.igu.barraTexto.connect("clicked",self.insertarObjeto,"texto")
        self.igu.barraBoton.connect("clicked",self.insertarObjeto,"boton")
        self.igu.barraCajaTexto.connect("clicked",self.insertarObjeto,"entrada")
        self.igu.barraLista.connect("clicked",self.insertarObjeto,"lista")
        self.igu.barraCheck.connect("clicked",self.insertarObjeto,"check")
        self.igu.barraArea.connect("clicked",self.insertarObjeto,"area")
        self.igu.barraSon.connect("clicked",self.insertarObjeto,"sonido")
        self.igu.barraCla.connect("clicked",self.insertarObjeto,"video")
        self.igu.barraScr.connect("clicked",self.insertarObjeto,"codigo")

    def copiarObjeto(self,widget=None,data=None):
        if self.proyecto==None:
            self.igu.statusbar.push(0,"¿Que intentas copiar?")
        elif self.seleccionado==None:
            self.igu.statusbar.push(0,"Selecciona un objeto primero!!!")
        else:
            if self.seleccionado.__class__==Proyecto:
                self.igu.statusbar.push(0,"Un proyecto no se puede copiar!!!")
            else:
                self.igu.statusbar.push(0, "Objeto a copiar: "+self.seleccionado.nombre)
                self.__copi=self.seleccionado

    def pegarObjeto(self,widget=None,data=None):
        if self.proyecto==None:
            self.igu.statusbar.push(0,"No hay proyecto activo")
        elif self.__copi==None:
            self.igu.statusbar.push(0, "Copie un objeto Primero!!!")
        else:
            if self.__copi.__class__==Escena:
                ref= len(self.objetos["Hojas"])
                self.insertarHoja()
                self.puntero=ref
                self.objetos["Hojas"][ref]["objeto"].asignaPropiedades(self.__copi.propiedades())
                j=0
                for i in self.objetos["Hojas"]:
                    print j
                    if i["objeto"]==self.__copi:
                        for k in i["hijos"]:
                            self.insertarObjeto(None,k["tipo"])
                            self.objetos["Hojas"][ref]["hijos"][j]["objeto"].asignaPropiedades(k["objeto"].propiedades())
                            j+=1
                        break
                self.igu.statusbar.push(0, "Copiado de Hoja: OK")
            else:
                if len(self.nivel)<3:
                    self.igu.statusbar.push(0, "No se puede copiar en este nivel")
                elif self.nivel[1]==1:
                    self.igu.statusbar.push(0, "No se puede copiar en este nivel")
                else:
                    self.insertarObjeto(None,self.__copi.tipo())
                    self.objetos["Hojas"][self.puntero]["hijos"][len(self.objetos["Hojas"][self.puntero]["hijos"])-1]["objeto"].asignaPropiedades(self.__copi.propiedades())
                    self.igu.statusbar.push(0, "Copiado de Objeto "+str(self.__copi.tipo())+": OK")
                    self.actulizaLienzo()
        
    def nuevoProyecto(self,widget=None,data=None):
        #Si estamos en linux =)
        if str(os.name)== "posix":
            if self.proyecto!=None:
                self.igu.cuadroMensajes("Proyecto Abierto","Ya hay un Proyecto abierto\n por favor cierrelo antes de crear otro",gtk.MESSAGE_WARNING,gtk.BUTTONS_OK)
                return
            #print os.getcwd() muestra la ruta donde se ejecuta el main
            ruta= os.getenv("HOME") #saca la ruta del home del usuario
            dialogo = gtk.FileChooserDialog(title="Crear Nuevo Proyecto",action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
            resp=dialogo.run()
            if resp==gtk.RESPONSE_OK:
                proyecto=str(dialogo.get_filename())
                dialogo.destroy()
                if os.path.isfile(str(proyecto)+".gcd"):
                    md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ya existe un proyecto con este nombre")
                    md.set_title("Error de Creacion de Proyecto")
                    md.run()
                    md.destroy()
                    return
                print "creo el proyecto en:"+str(proyecto)
                nmb=proyecto.split("/")
                print "nombre Proyecto:"+str(nmb[len(nmb)-1])
                rutaTemporal=str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(nmb[len(nmb)-1])
                print "lso temporales en "+str(rutaTemporal)
                try: #trato de crear las carpetas temporales en el path de GENCED
                    os.mkdir(rutaTemporal)
                    os.mkdir(os.path.join(rutaTemporal,"recursos/"))
                    os.mkdir(os.path.join(rutaTemporal,"recursos/imagenes"))
                    os.mkdir(os.path.join(rutaTemporal,"recursos/sonidos"))
                    os.mkdir(os.path.join(rutaTemporal,"recursos/videos"))
                    os.mkdir(os.path.join(rutaTemporal,"recursos/archivos"))
                    os.mkdir(os.path.join(rutaTemporal,"conf"))
                except:
                    md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ocurrio un error al intentar crear los directorios")
                    md.set_title("Error de Creacion Directorios")
                    md.run()
                    md.destroy()
                    self.igu.statusbar.push(0,"Ocurrio un error al crear los directorios")
                    return
                try: #trato de copiar los archivos js a las carpetas temporales del proyecto
                    destino=os.path.join(rutaTemporal,"recursos/jquery.js")
                    origen=os.path.join(os.path.dirname(os.path.realpath(__file__)),"recursos/js/jquery.js")
                    shutil.copy(origen,destino)
                    destino=os.path.join(rutaTemporal,"recursos/jquery.timer.js")
                    origen=os.path.join(os.path.dirname(os.path.realpath(__file__)),"recursos/js/jquery.timer.js")
                    shutil.copy(origen,destino)
                except:
                    md=gtk.MessageDialog(None, gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Ocurrio un error al intentar copiar los archivos javascript")
                    md.set_title("Error de Copiado de Archivos")
                    md.run()
                    md.destroy()
                    self.igu.statusbar.push("Ocurrio un error al copiar los archivos de Javascript")
                    return
                self.proyecto=Proyecto(nmb[len(nmb)-1],proyecto+".gcd") #Se crea el objeto Proyecto
                hoja=Escena(0) #Se crea la primera Hoja
                self.objetos["Hojas"].append({"objeto":hoja,"hijos":[],"cuadro":0,"circulo":0,"triangulo":0,"linea":0,"imagen":0,"texto":0,"boton":0,"entrada":0,"lista":0,"check":0,"area":0,"video":0,"sonido":0}) #Se anexa al diccionario de Objetos
                i=0
                parseJSON={"Proyecto":{"ancho":self.proyecto.ancho,"alto":self.proyecto.alto,"maximizado":self.proyecto.maximizado},"Hojas":[],"Imagenes":[],"Sonidos":[],"Videos":[],"Archivos":[]} #hacemos un parseo de objetos a entradas JSON serializables
                for d in self.objetos["Hojas"]:
                    h= {"hoja"+str(i):{"propiedades":d["objeto"].propiedades(),"elementos":[],"cuadro":0,"circulo":0,"triangulo":0,"linea":0,"imagen":0,"texto":0,"boton":0,"entrada":0,"lista":0,"check":0,"area":0,"video":0,"sonido":0}}
                    parseJSON["Hojas"].append(h)
                    for e in self.objetos["Hojas"][i]["hijos"]:
                        j={"prop":[e.propiedades()],"tipo":e.tipo()}
                        parseJSON["Hojas"][i]["hoja"+str(i)]["elementos"].append(j)
                    i+=1
                #creo el archivo de configuracion
                with open(os.path.join(rutaTemporal,"conf/conf.cfg"), 'w') as f:
                    f.write(unicode(json.dumps(parseJSON, ensure_ascii=False)))
                #se crea el tar
                tar = tarfile.open(self.proyecto.ruta, "w")
                tar.add(rutaTemporal,arcname=str(nmb[len(nmb)-1]))
                tar.close()
                self.proyecto.paginas.append("<html></html>")
                self.actualizaArbol()
                self.igu.barraHojaNueva.set_sensitive(True)
                self.igu.barraImagenNuevo.set_sensitive(True)
                self.igu.barraSonidoNuevo.set_sensitive(True)
                self.igu.barraVideoNuevo.set_sensitive(True)
                self.igu.barraArchivoNuevo.set_sensitive(True)
                self.igu.cer.set_sensitive(True)
                self.igu.proy=self.proyecto.nombre
                self.igu.statusbar.push(0,"Se ha creado con Éxito el proyecto")
            else:
                dialogo.destroy()
                self.igu.statusbar.push(0,"Se ha cancelado la creación del proyecto")
            
    def actualizaArbol(self):
        almacen = gtk.TreeStore(str,str)
        padre=almacen.append(None,[self.proyecto.nombre,gtk.STOCK_FILE])
        f=almacen.append(padre,["Hojas",gtk.STOCK_DND_MULTIPLE])
        i=0
        for d in self.objetos["Hojas"]:
            x=almacen.append(f,[d["objeto"].nombre,gtk.STOCK_DND])
            #h= {"hoja"+str(i):{"propiedades":[d["objeto"].propiedades()],"elementos":[]}}
            for e in self.objetos["Hojas"][i]["hijos"]:
                almacen.append(x,[e["objeto"].nombre,gtk.STOCK_FILE])
            i+=1
        f=almacen.append(padre,["Recursos",gtk.STOCK_DIRECTORY])
        x=almacen.append(f,["Imagenes",gtk.STOCK_OPEN])
        for d in self.objetos["Imagenes"]:
            almacen.append(x,[d,gtk.STOCK_CDROM])
        x=almacen.append(f,["Sonidos",gtk.STOCK_OPEN])
        for d in self.objetos["Sonidos"]:
            almacen.append(x,[d,gtk.STOCK_CDROM])
        x=almacen.append(f,["Videos",gtk.STOCK_OPEN])
        for d in self.objetos["Videos"]:
            almacen.append(x,[d,gtk.STOCK_CDROM])
        x=almacen.append(f,["Archivos",gtk.STOCK_OPEN])
        for d in self.objetos["Archivos"]:
            almacen.append(x,[d,gtk.STOCK_CDROM])

        '''for fila in range(len(self.objetos)):
            x=almacen.append(f,[self.objetos[fila][0].nombre,gtk.STOCK_DND])
            for i in range(len(self.objetos[fila])-1):
                almacen.append(x,[self.objetos[fila][i+1].nombre,gtk.STOCK_FILE])'''
        self.igu.treeview.set_model(almacen)
        self.igu.treeview.expand_all()
    
    def actulizaLienzo(self,tipo=0):
        rutaTemporal=str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre
        marca=""
        pagina="<html><head><script src='"+str(os.path.dirname(os.path.realpath(__file__)))+"/recursos/js/jquery.js'></script><script>$(document).ready(function(){$('.tiempoDiseno').click(function(){document.title='1+'+$(this).attr('id');})})</script></head>"
        if tipo==0:
            i=0
            for d in self.objetos["Hojas"]:
                if self.puntero==i:
                    pagina+=d["objeto"].trazaObjeto(rutaTemporal)
                    for e in self.objetos["Hojas"][i]["hijos"]:
                        if e["objeto"]==self.seleccionado:
                            marca="<div style='position:absolute;font-size:10pt;top:"+str(float(e["objeto"].y)-1)+"%;left:"+str(float(e["objeto"].x)-1)+"%;border:dotted 2px black;width:"+str(float(e["objeto"].ancho)+1.5)+"%;height:"+str(float(e["objeto"].alto)+1.5)+"%'></div>"
                        pagina+= e["objeto"].trazaObjeto(rutaTemporal)
                i+=1
            pagina=pagina+marca+"</body></html>"
            self.igu.lienzo.load_html_string(pagina,"file://"+rutaTemporal+"/")
        elif tipo==1:
            recurso= self.objetos["Imagenes"][self.puntero]
            pagina=pagina+"<img src='"+rutaTemporal+"/recursos/imagenes/"+str(recurso)+"'/>"
        elif tipo==2:
            recurso= self.objetos["Sonidos"][self.puntero]
            pagina=pagina+"<div><audio id='player' autoplay preload><source src='"+rutaTemporal+"/recursos/sonidos/"+str(recurso)+"' type='audio/ogg'   preload><source src='"+rutaTemporal+"/recursos/sonidos/"+str(recurso)+"' type='audio/mpeg'   preload><source src='"+rutaTemporal+"/recursos/sonidos/"+str(recurso)+"' type='audio/wav'   preload></audio></div><h3>"+str(recurso)+"</h3><button onclick=\"document.getElementById('player').play();\">Reproducir</button><button onclick=\"document.getElementById('player').pause();document.getElementById('player').currentTime=0;\">Detener</button><button onclick=\"document.getElementById('player').pause()\">Pausa</button><button onclick=\"document.getElementById(\'player\').volume += 0.1;\">Subir Volumen</button><button onclick=\"document.getElementById(\'player\').volume -= 0.1;\">Bajar Volumen</button>"
        elif tipo==3:
            recurso= self.objetos["Videos"][self.puntero]
            pagina=pagina+"<div style='background-color:black'><video autoplay preload='auto' heigth='75%' width='75%'><source src='"+rutaTemporal+"/recursos/videos/"+str(recurso)+"' type='video/ogg' ><source src='"+rutaTemporal+"/recursos/videos/"+str(recurso)+"' type='video/mp4'><source src='"+rutaTemporal+"/recursos/videos/"+str(recurso)+"' type='video/webm'>No soportado video</video><div style='clear:both'></div></div><h3>"+str(recurso)+"</h3>"
        elif tipo==4:
            recurso= self.objetos["Archivos"][self.puntero]
            pagina=pagina+"<div><style>@font-face{font-family:'fuente';src: url('"+rutaTemporal+"/recursos/archivos/"+str(recurso)+"')}</style></div><h3 style='font-family:fuente'>El niño Simón Bolívar, Tocaba alegre el tambor, en un patio de granados, que siempre estaban en flor</h3><h4 style='font-family:fuente'>Pero un día se hizo grande, el que fue niño Simón y anduvo por America cuando era Libertador</h4>"

        pagina=pagina+"</body></html>"
        self.igu.lienzo.load_html_string(pagina,"file://"+rutaTemporal+"/")
        self.igu.statusbar.push(0,"Vista Diseño")

    def guardarProyecto(self,widget=None):#lista
        #Rutina para Escribir el archivo de Configuracion
        if str(os.name)== "posix":
            parseJSON={"Proyecto":{"ancho":self.proyecto.ancho,"alto":self.proyecto.alto,"maximizado":self.proyecto.maximizado},"Hojas":[],"Imagenes":[],"Sonidos":[],"Videos":[],"Archivos":[]} #hacemos un parseo de objetos a entradas JSON serializables
            print self.objetos["Hojas"]
            i=0
            for d in self.objetos["Hojas"]:
                h= {"hoja"+str(d["objeto"].nombre[4:]):{"propiedades":d["objeto"].propiedades(),"elementos":[]}}
                parseJSON["Hojas"].append(h)
                for e in self.objetos["Hojas"][i]["hijos"]:
                    j={"prop":e["objeto"].propiedades(),"tipo":e["objeto"].tipo(),"id":e["objeto"].ide}
                    parseJSON["Hojas"][i]["hoja"+str(i)]["elementos"].append(j)
                i+=1
            for d in self.objetos["Imagenes"]:
                parseJSON["Imagenes"].append(d)
            for d in self.objetos["Sonidos"]:
                parseJSON["Sonidos"].append(d)
            for d in self.objetos["Videos"]:
                parseJSON["Videos"].append(d)
            for d in self.objetos["Archivos"]:
                parseJSON["Archivos"].append(d)
            rutaTemporal=str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre
            print rutaTemporal
            #creo el archivo de configuracion
            with open(os.path.join(rutaTemporal,"conf/conf.cfg"), 'w') as f:
                f.write(unicode(json.dumps(parseJSON, ensure_ascii=False)))
            #actualizo el tar
            tar = tarfile.open(str(self.proyecto.ruta), "w")
            tar.add(rutaTemporal,self.proyecto.nombre)
            tar.close()
            self.EDITADO=0
            self.igu.barraGua.set_sensitive(False)
            self.igu.barraGuc.set_sensitive(False)
            self.igu.gua.set_sensitive(False)
            self.igu.guc.set_sensitive(False)
            self.igu.statusbar.push(0,"Guardaddo con exito el proyecto")
   
    def cerrarProyecto(self,widget=None,data=None):
        shutil.rmtree(str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre)
        self.igu.proy=None
        self.proyecto=None
        self.seleccionado=None
        self.objetos.clear()
        self.objetos={"Proyecto":{"ancho":640,"alto":480,"maximizado":"Falso"},"Hojas":[],"Imagenes":[],"Sonidos":[],"Videos":[],"Archivos":[]}
        self.EDITADO=0
        self.puntero=-1
        self.nivel=-1
        self.igu.cer.set_sensitive(False)
        ls=self.igu.treeview.get_model()
        if ls!=None:
            ls.clear()
        ls=self.igu.panelPropiedades.get_model()
        if ls!=None:
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
        if self.proyecto!=None:
            self.igu.cuadroMensajes("Proyecto Abierto","Ya hay un Proyecto abierto\n por favor cierrelo antes de abrir otro",gtk.MESSAGE_WARNING,gtk.BUTTONS_OK)
            return
        response=self.igu.cuadroDialogo("Abrir Proyecto",gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        if response[0] == gtk.RESPONSE_OK:
            nmb=response[1].split("/")
            nombre=nmb[len(nmb)-1][0:-4]
            rt=os.path.dirname(os.path.realpath(__file__))
            tar = tarfile.open(str(response[1]), "r")
            tar.extractall(rt)
            tar.close()
            
            #archivo=tar.getmember(nmb[len(nmb)-1][0:-4]+"/conf/conf.cfg")
            with open(os.path.join(rt+"/"+nombre,"conf/conf.cfg")) as conf:    
                parseDIC = json.load(conf)
            self.proyecto=Proyecto(nombre,str(response[1]))
            self.proyecto.alto= parseDIC["Proyecto"]["alto"]
            self.proyecto.ancho= parseDIC["Proyecto"]["ancho"]
            self.proyecto.maximizado= parseDIC["Proyecto"]["maximizado"]
            self.objetos["Proyecto"]["alto"]=self.proyecto.alto
            self.objetos["Proyecto"]["ancho"]=self.proyecto.ancho
            self.objetos["Proyecto"]["maximizado"]=self.proyecto.maximizado
            i=0
            #print parseDIC["Hojas"].keys()
            for d in parseDIC["Hojas"]:
                print d.keys()[0]
                hoja=Escena(d.keys()[0][4:])
                hoja.asignaPropiedades(d[d.keys()[0]]["propiedades"])
                self.objetos["Hojas"].append({"objeto":hoja,"hijos":[],"cuadro":0,"circulo":0,"triangulo":0,"linea":0,"imagen":0,"texto":0,"boton":0,"entrada":0,"lista":0,"check":0,"area":0,"video":0,"sonido":0})
                for e in parseDIC["Hojas"][i][d.keys()[0]]["elementos"]:
                    if e["tipo"]=="cuadro":
                        ob=Cuadro(int(e["id"]))
                        self.objetos["Hojas"][i]["cuadro"]=e["id"]
                    elif e["tipo"]=="circulo":
                        ob=Circulo(int(e["id"]))
                        self.objetos["Hojas"][i]["circulo"]=e["id"]
                    elif e["tipo"]=="triangulo":
                        ob=Triangulo(int(e["id"]))
                        self.objetos["Hojas"][i]["triangulo"]=e["id"]
                    elif e["tipo"]=="linea":
                        ob=Linea(int(e["id"]))
                        self.objetos["Hojas"][i]["linea"]=e["id"]
                    elif e["tipo"]=="imagen":
                        ob=Imagen(int(e["id"]))
                        self.objetos["Hojas"][i]["imagen"]=e["id"]
                    elif e["tipo"]=="texto":
                        ob=Texto(int(e["id"]))
                        self.objetos["Hojas"][i]["texto"]=e["id"]
                    elif e["tipo"]=="boton":
                        ob=Boton(int(e["id"]))
                        self.objetos["Hojas"][i]["boton"]=e["id"]
                    elif e["tipo"]=="entrada":
                        ob=Entrada(int(e["id"]))
                        self.objetos["Hojas"][i]["entrada"]=e["id"]
                    elif e["tipo"]=="lista":
                        ob=Lista(int(e["id"]))
                        self.objetos["Hojas"][i]["lista"]=e["id"]
                    elif e["tipo"]=="check":
                        ob=Check(int(e["id"]))
                        self.objetos["Hojas"][i]["check"]=e["id"]
                    elif e["tipo"]=="area":
                        ob=Area(int(e["id"]))
                        self.objetos["Hojas"][i]["area"]=e["id"]
                    elif e["tipo"]=="sonido":
                        ob=Sonido(int(e["id"]))
                        self.objetos["Hojas"][i]["sonido"]=e["id"]
                    elif e["tipo"]=="video":
                        ob=Video(int(e["id"]))
                        self.objetos["Hojas"][i]["video"]=e["id"]
                    ob.asignaPropiedades(e["prop"])
                    j={"objeto":ob,"tipo":ob.tipo()}
                    self.objetos["Hojas"][i]["hijos"].append(j)
                i+=1
            for d in parseDIC["Imagenes"]:
                self.objetos["Imagenes"].append(d)
            for d in parseDIC["Sonidos"]:
                self.objetos["Sonidos"].append(d)
            for d in parseDIC["Videos"]:
                self.objetos["Videos"].append(d)
            for d in parseDIC["Archivos"]:
                self.objetos["Archivos"].append(d)
            
            self.actualizaArbol()
            self.igu.barraHojaNueva.set_sensitive(True)
            self.igu.barraImagenNuevo.set_sensitive(True)
            self.igu.barraSonidoNuevo.set_sensitive(True)
            self.igu.barraVideoNuevo.set_sensitive(True)
            self.igu.barraArchivoNuevo.set_sensitive(True)
            self.igu.cer.set_sensitive(True)
            self.igu.proy=self.proyecto.nombre
            self.igu.statusbar.push(0,"Proyecto Abierto"+str(self.proyecto.nombre))
        elif response[0] == gtk.RESPONSE_CANCEL:
            self.igu.statusbar.push(0,"Cancelado Abrir Proyecto")
     
    def insertarHoja(self,widget=None,data=None): #LISTA
        #Insertamos una nueva hoja al proyecto
        if self.proyecto!=None:
            n= self.objetos["Hojas"][len(self.objetos["Hojas"])-1]["objeto"].nombre[4:]
            hoja=Escena(int(n)+1)
            self.objetos["Hojas"].append({"objeto":hoja,"hijos":[],"cuadro":0,"circulo":0,"triangulo":0,"linea":0,"imagen":0,"texto":0,"boton":0,"entrada":0,"lista":0,"check":0,"area":0,"video":0,"sonido":0})
            self.actualizaArbol()
            self.igu.barraGua.set_sensitive(True)
            self.igu.barraGuc.set_sensitive(True)
            self.igu.gua.set_sensitive(True)
            self.igu.guc.set_sensitive(True)
            self.proyecto.paginas.append("")
            self.EDITADO=1
        else:
            self.igu.statusbar.push(0,"No hay proyecto para insertar Hojas")
    
    def insertarObjeto(self,w=None,data=None):
        #Insertamos los objetos
        if self.proyecto==None:
            self.igu.statusbar.push(0,"No hay proyecto para insertar objetos")
            return
        if data==None:
            print "sin data"
            return
        elif data=="codigo":
            editorEscritos=Analizador(self.objetos["Hojas"][self.puntero]["hijos"],self.objetos["Hojas"][self.puntero]["objeto"])
            return
        self.objetos["Hojas"][self.puntero][data]+=1
        if data=="cuadro":
            objeto=Cuadro(self.objetos["Hojas"][self.puntero][data])
        elif data=="circulo":
            objeto=Circulo(self.objetos["Hojas"][self.puntero][data])
        elif data=="triangulo":
            objeto=Triangulo(self.objetos["Hojas"][self.puntero][data])
        elif data=="linea":
            objeto=Linea((self.objetos["Hojas"][self.puntero][data]))
        elif data=="imagen":
            objeto=Imagen(self.objetos["Hojas"][self.puntero][data])
        elif data=="texto":
            objeto=Texto(self.objetos["Hojas"][self.puntero][data])
        elif data=="boton":
            objeto=Boton(self.objetos["Hojas"][self.puntero][data])
        elif data=="entrada":
            objeto=Entrada(self.objetos["Hojas"][self.puntero][data])
        elif data=="lista":
            objeto=Lista(self.objetos["Hojas"][self.puntero][data])
        elif data=="check":
            objeto=Check(self.objetos["Hojas"][self.puntero][data])
        elif data=="area":
            objeto=Area(self.objetos["Hojas"][self.puntero][data])
        elif data=="sonido":
            objeto=Sonido(self.objetos["Hojas"][self.puntero][data])
        elif data=="video":
            objeto=Video(self.objetos["Hojas"][self.puntero][data])
        else:
            self.igu.statusbar.push(0,"No se reconoce el tipo de objeto a insertar")
            return
        self.objetos["Hojas"][self.puntero]["hijos"].append({"objeto":objeto,"tipo":objeto.tipo()})
        self.igu.statusbar.push(0,"Insertamos un "+str(objeto.tipo()))
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
            filtro.set_name("Imagenes")
            filtro.add_mime_type("image/png")
            filtro.add_mime_type("image/jpeg")
            filtro.add_mime_type("image/gif")
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
            filtro.add_pattern("*.ogv")
            filtro.add_pattern("*.mp4")
            filtro.add_pattern("*.webm")
        elif data==3:
            filtro.set_name("Archivos")
            filtro.add_pattern("*.*")
        dialog.add_filter(filtro)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            e=dialog.get_filename().split("/")
            archivo=e[len(e)-1]
            tmp=str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre
            if data==0:
                destino=tmp+"/recursos/imagenes/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
                self.objetos["Imagenes"].append(str(archivo))
            elif data==1:
                destino=tmp+"/recursos/sonidos/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
                self.objetos["Sonidos"].append(str(archivo))
            elif data==2:
                destino=tmp+"/recursos/videos/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
                self.objetos["Videos"].append(str(archivo))
            elif data==3:
                destino=tmp+"/recursos/archivos/"+archivo
                origen=dialog.get_filename()
                shutil.copy(origen,destino)
                self.objetos["Archivos"].append(str(archivo))
            self.actualizaArbol()
            #self.guardarProyecto()
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
            self.seleccionado=self.proyecto
        elif len(self.nivel)==2:
            self.seleccionado=None
        elif len(self.nivel)==3:
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
                self.seleccionado=self.objetos["Hojas"][self.nivel[2]]["objeto"]
                self.actulizaLienzo()
            else:
                self.seleccionado=None
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
                self.seleccionado=self.objetos["Hojas"][self.nivel[2]]["hijos"][self.nivel[3]]["objeto"]
                self.actulizaLienzo()
                #self.igu.statusbar.push(0,"Propíedad de los objetos de la hoja"+str(self.nivel[2])+"-"+str(self.nivel))
            if self.nivel[1]==1:
                self.puntero=self.nivel[3]
                self.seleccionado=None
                if self.nivel[2]==0:
                    self.igu.statusbar.push(0,"Imagenes")
                    self.actulizaLienzo(1)
                if self.nivel[2]==1:
                    self.igu.statusbar.push(0,"sonidos")
                    self.actulizaLienzo(2)
                if self.nivel[2]==2:
                    self.igu.statusbar.push(0,"videos")
                    self.actulizaLienzo(3)
                if self.nivel[2]==3:
                    self.igu.statusbar.push(0,"Archivos")
                    self.actulizaLienzo(4)
       
        print "punteroArbol->self.Nivel(1325):"+str(self.nivel)
        print self.seleccionado    
        self.actualizaVistaPropiedades()

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
            for i in self.objetos["Imagenes"]:
                lista.append([i])
        if tipoLista==9:
            lista.append(["Courier"])
            for i in self.objetos["Archivos"]:
                lista.append([i])
        if tipoLista==10:
            lista.append(["None"])
            for i in self.objetos["Sonidos"]:
                lista.append([i])
        if tipoLista==11:
            lista.append(["None"])
            for i in self.objetos["Videos"]:
                lista.append([i])
        if tipoLista==12:
            lista.append(["None"])
            lista.append(["center"])
            lista.append(["left"])
            lista.append(["right"])
            lista.append(["justify"])
        return lista
    
    def actualizaVistaPropiedades(self):
        almacen = gtk.ListStore(str,str,gtk.TreeModel)
        #self.igu.statusbar.push(0,str(objeto.nombre))
        almacen.clear()
        objeto=self.seleccionado

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
            almacen.append(["alineacion",objeto.alineacion,self.llenaListas(12)])
            almacen.append(["parrafo",objeto.parrafo,self.llenaListas(4)])
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
            almacen.append(["borde",objeto.borde,self.llenaListas(6)])
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
        if objeto.__class__==Video:
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["video",objeto.video,self.llenaListas(11)])
            almacen.append(["x",objeto.x,self.llenaListas(5)])
            almacen.append(["y",objeto.y,self.llenaListas(5)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(4)])
            almacen.append(["alto",objeto.alto,self.llenaListas(4)])

        if objeto.__class__==Proyecto:
            almacen.append(["ruta",objeto.ruta,self.llenaListas(4)])
            almacen.append(["nombre",objeto.nombre,self.llenaListas(4)])
            almacen.append(["ancho",objeto.ancho,self.llenaListas(4)])
            almacen.append(["alto",objeto.alto,self.llenaListas(4)])
            almacen.append(["maximizado",objeto.maximizado,self.llenaListas(3)])       
        
        self.igu.panelPropiedades.set_model(almacen)
        if objeto==None:
            ls=self.igu.panelPropiedades.get_model()
            if ls!=None:
                ls.clear()
        #self.actulizaLienzo()
    
    def eliminarObjetos(self,widget):
        if self.proyecto==None:
            self.igu.statusbar.push(0,"¿Qué Intentas Eliminar?")
        elif self.seleccionado==None:
            if len(self.nivel)==4:
                tmp=str(os.path.dirname(os.path.realpath(__file__)))+"/"+self.proyecto.nombre
                if self.nivel[2]==0:
                    os.remove(tmp+"/recursos/imagenes/"+str(self.objetos["Imagenes"][self.nivel[3]]))
                    del self.objetos["Imagenes"][self.nivel[3]]
                    self.igu.statusbar.push(0,"Eliminada la Imagen")
                elif self.nivel[2]==1:
                    os.remove(tmp+"/recursos/sonidos/"+str(self.objetos["Sonidos"][self.nivel[3]]))
                    del self.objetos["Sonidos"][self.nivel[3]]
                    self.igu.statusbar.push(0,"Eliminado el Sonido")
                elif self.nivel[2]==2:
                    os.remove(tmp+"/recursos/videos/"+str(self.objetos["Videos"][self.nivel[3]]))
                    del self.objetos["Videos"][self.nivel[3]]
                    self.igu.statusbar.push(0,"Eliminado el Video")
                elif self.nivel[2]==3:
                    os.remove(tmp+"/recursos/archivos/"+str(self.objetos["Archivos"][self.nivel[3]]))
                    del self.objetos["Archivos"][self.nivel[3]]
                    self.igu.statusbar.push(0,"Eliminado el Archivo")
                else:
                    self.igu.statusbar.push(0,"¿Que desea eliminar?")
            else:
                self.igu.statusbar.push(0,"Selecciona un objeto a eliminar")
        elif self.seleccionado.__class__==Proyecto:
            self.igu.statusbar.push(0,"No se puede eliminar el proyecto!!!!")
        else:
            respuesta=self.igu.cuadroMensajes("Confirmar Eliminar Objeto","Esta Seguro de Eliminar Este Objeto",gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO)
            if respuesta==gtk.RESPONSE_YES:
                if self.seleccionado.__class__==Escena:
                    ob=self.objetos["Hojas"][self.puntero]["objeto"].nombre
                    del self.objetos["Hojas"][self.puntero]
                    self.igu.statusbar.push(0,"Eliminada La Hoja "+str(ob))
                else:
                    ob=self.objetos["Hojas"][self.puntero]["hijos"][self.nivel[3]]["objeto"].nombre
                    del self.objetos["Hojas"][self.puntero]["hijos"][self.nivel[3]]
                    self.igu.statusbar.push(0,"Eliminado el Objeto "+str(ob))

                self.igu.barraGua.set_sensitive(True)
                self.igu.barraGuc.set_sensitive(True)
                self.igu.gua.set_sensitive(True)
                self.igu.guc.set_sensitive(True)
        self.actualizaArbol()

    def _cambiaAtributo( self,widget, fila, valor, columna):#Ajustada y Lista
        modelo = self.igu.panelPropiedades.get_model()
        modelo[fila][columna] = valor
        atributo=modelo[fila][0]
        s=self.seleccionado.__dict__
        s[atributo]=valor
        self.actulizaLienzo()
        self.EDITADO=1
        self.igu.barraGua.set_sensitive(True)
        self.igu.barraGuc.set_sensitive(True)
        self.igu.gua.set_sensitive(True)
        self.igu.guc.set_sensitive(True)
        
