# -*- coding: utf-8 -*-
import gtk
import pango
import re
import os
ruta= os.path.dirname(os.path.realpath(__file__))

class Analizador():
    def __init__(self,objetos,recursos):
        eventosEscena=["alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        eventosObjetos=["click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"]
        window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title("editor de escritos")
        window.set_size_request(600,600)
        window.set_resizable(False)
        window.set_modal(True)
        self.barraEstado = gtk.Statusbar()
        color = gtk.gdk.color_parse('#ffffff')
        window.modify_bg(gtk.STATE_NORMAL, color)
        barra = gtk.Toolbar()
        barra.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        barra.set_style(gtk.TOOLBAR_ICONS)
        barra.set_border_width(1)
        barra.set_icon_size(gtk.ICON_SIZE_MENU)
        icoNue=gtk.Image()
        icoNue.set_from_file(os.path.join(ruta,'iconos/proyecto.png'))
        barraSCAN = gtk.ToolButton(icoNue)
        barra.insert(barraSCAN,0)
        caja=gtk.VBox(False)
        txtScript=gtk.TextView()
        cntScript=txtScript.get_buffer()
        txtScript.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 24)
        txtScript.connect("expose-event", self._pintaNumeros,cntScript,txtScript)
        #txtScript.connect("key-press-event",self.analizador,cntScript,objetos)
        cntScript.set_text(objetos[0].escritos)
        barraSCAN.connect("clicked",self.analizador,cntScript,objetos,recursos)
        lista=gtk.TreeStore(str,gtk.gdk.Pixbuf)
        padre=lista.append(None,["Sistema",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/sistema.png'))])
        f=lista.append(padre,["cicloSistema",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/ciclo.png'))])
        f=lista.append(padre,["cronometroSistema",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/ciclo.png'))])
        for i in range(len(objetos)):
            if i==0:
                padre=lista.append(None,[objetos[i].nombre,gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/hoja.png'))])
                for n in range(len(eventosEscena)):
                    f=lista.append(padre,[eventosEscena[n],gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/evento.png'))])
            else:
                padre=lista.append(None,[objetos[i].nombre,gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/objeto.png'))])
                for n in range(len(eventosObjetos)):
                    f=lista.append(padre,[eventosObjetos[n],gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/evento.png'))])
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
        padre=listaIzquierda.append(None,["Variables",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/sistema.png'))])
        f=listaIzquierda.append(padre,["general",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/variable.png'))])
        f=listaIzquierda.append(padre,["local",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/variable.png'))])
        padre=listaIzquierda.append(None,["Funciones",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/sistema.png'))])
        f=listaIzquierda.append(padre,["funcion",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/funcion.png'))])
        padre=listaIzquierda.append(None,["Metodos",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/sistema.png'))])
        f=listaIzquierda.append(padre,["propiedad",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["mostrar",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["ocultar",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["mover",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["redimensionar",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["rotar",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["mensaje",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["confirmacion",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["entrada",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["insertarObjeto",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["inc",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["dec",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["hoja",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["escribirDato",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["leerDato",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["tecla",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        padre=listaIzquierda.append(None,["Controles de Flujo",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/sistema.png'))])
        f=listaIzquierda.append(padre,["Si",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/if.png'))])
        f=listaIzquierda.append(padre,["Mientras",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/if.png'))])
        f=listaIzquierda.append(padre,["Desde-Hasta",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/if.png'))])
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
        sep.set_size_request(400, 20)
        scroll.set_size_request(300,180)
        scroll2.set_size_request(300,180)
        scrolles=gtk.HBox(False)
        scrolles.pack_start(scroll,True,True,10)
        scrolles.pack_start(scroll2,True,True,10)
        caja.pack_start(scrolles,False,False,0)
        caja.pack_start(sep,False,True)
        caja.pack_start(txtScript,True)
        caja.pack_end(self.barraEstado,False,True)
        window.add(caja)
        window.show_all()

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
    
    def muestraAtributos(self,treeview,itera, path, fila,escrito):
        (mod,ite)= fila.get_selected_rows()
        iterador= ite[0]
        if len(iterador)==2:
            if mod[ite[0]][0]=="cicloSistema":
                self.barraEstado.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(100)")
                linea=str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(100):"
            elif mod[ite[0]][0]=="cronometroSistema":
                self.barraEstado.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(500)")
                linea=str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+"(500):"
            else:
                self.barraEstado.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0]))
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
                lineaCodigo= "\t"+str(mod[ite[0]][0])+"()\n\tfin->"+str(mod[ite[0]][0])+"\n"
            base=base + lineaCodigo
            self.barraEstado.push(0,str(mod[ite[0]][0])+"->"+str(mod[iterador[0]][0])+":"+str(iterador[0]))
            escrito.set_text(base)
    
    def analizador(self,widget,data=None,objetos=None,recursos=None):
        eventosValidos=["cronometroSistema","cicloSistema","alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        eventosObjetos=["click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"]
        elementosBloque=["\tpropiedad","\tmostrar","\tocultar","\trotar","\tmover","\tredimensionar","\tmensaje","\tconfirmacion","\tentrada","\tmostrarPantalla","\tinc","\tdec","\tsonido","\thoja","\tSi","\tescribirDato","\tleerDato","\ttecla","\tesperar","\tcronometro"]
        variablesValidas=["varg","\tvarl","\tvarg"]
        variablesDeclaradas=[]
        colores={"defecto":"default","Negro":"#000000","Gris Oscuro":"#696969","Gris":"#808080","Gris Claro":"#A9A9A9","Blanco":"#FFFFFF","Rojo Oscuro":"#8B0000","Rojo":"#FF0000","Rojo Claro":"#FA8072","Rosado Oscuro":"#FF1493","Rosado":"#FF69B4","Rosado Claro":"#FFB6C1","Fucsia Oscuro":"#8A2BE2","Fucsia":"#FF00FF","Fucsia Claro":"#CD5C5C","Marron Oscuro":"#800000","Marron":"#8B4513","Marron Claro":"#A0522D","Naranja Oscuro":"#FF8C00","Naranja":"#FF4500","Naranja Claro":"#FF6347","Purpura Oscuro":"#4B0082","Purupura":"#800080","Purpura Claro":"#EE82EE","Amarillo Oscuro":"#FFD700","Amarillo":"#FFFF00","Amarillo Claro":"#F0E68C","Teal":"#008080","Azul Oscuro":"#000080","Azul":"#0000FF","Azul Claro":"#00BFFF","AguaMarina Oscuro":"#1E90FF","AguaMarina":"#00FFFF","AguaMarina Claro":"#00BFFF","Verde Oscuro":"#006400","Verde":"#008000","Verde Claro":"#3CB371","Lima":"#00FF00","Oliva Oscuro":"#556B2F","Oliva":"#808000","Oliva Claro":"#BDB76B"}
        bordes={"punteado":"dotted","discontinuo":"dashed","solido":"solid","doble":"double","acanalado":"groove","corrugado":"ridge","relieve bajo":"inset","relieve alto":"outset"}
        atributosOb={"colorFondo":"background-color","transparencia":"transparency","ancho":"width","alto":"height","x":"left","y":"top","borde":"border-style","colorBorde":"borderTopColor","anchoBorde":"border-width","sombra":"shadow","rotar":"-webkit-transform:rotate","oculto":"hidden","texto":"text","imagen":"src"}
        obje=objetos
        recu=recursos
        
        ini,fin=data.get_bounds()
        lineas=data.get_line_count()+1
        #variables de control (banderas)
        inicioLinea=True
        declaracionVariables=True
        variablesLocales=True
        abiertoBloque=""
        condicional=""
        teclas=False
        cierraTecla=False
        descrError="Ok todo Bien"
        cron=0
        script="$( document ).ready(function() { wh= parseInt(document.body.clientWidth);hh= parseInt(document.body.clientHeight);"
        for i in range(lineas-1):
            p1=data.get_iter_at_line(i)
            ncr=p1.get_chars_in_line()-1
            if ncr>0:#esto es para evitar el molestoso aborto de gtk cuando las linea esta vacia
                p2=data.get_iter_at_line_offset(i,ncr)
                linea = data.get_text(p1,p2)
                #print "linea "+str(i+1)+": "+linea
                #inicioLinea=true
                if inicioLinea:
                    if re.search("^\t",linea):
                        descrError= "ERROR en la linea "+str(i+1)+"=> La linea no Admite 'tab' al inicio"
                        break
                    else:
                        if re.search("->",linea):
                            token=linea.split("->")[0]
                            nombre=linea.split("->")[1]
                            #es una variable?
                            if token in variablesValidas:
                                #esta asignada?
                                if re.search("=",nombre):
                                    variable=nombre.split("=")[0]
                                    asignacion=nombre.split("=")[1]
                                    #contiene solo letras minusculas?
                                    if re.search("^[a-z]*$",variable):
                                        #Puedo declarar variables aqui?
                                        if declaracionVariables:
                                            #Ya fue declarada?
                                            if nombre in variablesDeclaradas:
                                                descrError="ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" ya fue declarada"
                                                break
                                            #No ha sido declarada
                                            else:
                                                variablesDeclaradas.append(variable)
                                                #esta vacia la asignacion
                                                if asignacion=="":
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" requiere de una asignacion (=) no vacia"
                                                    break
                                                #es una variable numerica?
                                                elif re.search("^[0-9]*.[0-9]*$",asignacion):
                                                    #print "posible numero"
                                                    script=script+"var "+variable+" = "+asignacion+";"
                                                #es una variable de texto
                                                elif re.search("^\"*.*\"$",asignacion):
                                                    #print "posible cadena"
                                                    script=script+"var "+variable+" = '"+asignacion+"';"
                                                elif asignacion.split("(")[0]=="aritmetica":
                                                        atr=asignacion.split("(")[1]
                                                        atr=atr[0:len(atr)-1]
                                                        script=script+"var "+variable+"="+str(atr)+";"
                                                elif asignacion.split("(")[0]=="leerDato":
                                                        atr=asignacion.split("(")[1]
                                                        atr=atr[0:len(atr)-1]
                                                        script=script+str(variable)+"=sessionStorage."+str(atr)+";"
                                                #ninguna de las anteriores
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" no se le puede asignar ese valor"
                                                    break
                                        #estoy fuera de la declaracion de variables
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" no se puede declarar en este contexto"
                                            break
                                    #no tiene solo letras minusculas
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" solo puede contener letras minusculas"
                                        break
                                #No esta asignada
                                else:
                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" requiere de una asignacion (=)"
                                    break
                            #es un evento de Hoja o de sistema?
                            elif token in eventosValidos:
                                declaracionVariables=False
                                inicioLinea=False
                                #es el nombre Sistema?
                                if re.search("^Sistema",nombre):
                                    #termina en :?
                                    if nombre[-1]==":":
                                        #Se abrio (?:
                                        if nombre[7]=="(":
                                            #se cerro el )?
                                            if nombre[-2]==")":
                                                #el argumento es un numero entero?
                                                if nombre[8:-2].isdigit():
                                                    #es mayor de 100?
                                                    if int(nombre[8:-2])>99:
                                                        #Que tipo evento de sistema es?
                                                        if token==eventosValidos[0]:
                                                            #print "Ok evento de sistema tipo cronometro"
                                                            script=script+ "var crono"+str(cron)+" = $.timer(function() {"
                                                            abiertoBloque="cronometroSistema"
                                                            cron+=1
                                                        else:
                                                            #Ya hay un ciclo de sistema?
                                                            if "ciclo" in variablesDeclaradas:
                                                                descrError= "ERROR en la linea "+str(i+1)+"=> Solo se puede declarar un solo cicloSistema"
                                                                break
                                                            else:
                                                                variablesDeclaradas.append("ciclo")
                                                                abiertoBloque="cicloSistema"
                                                                script=script +"var timer = $.timer(function() {"
                                                                #print "Ok evento de sistema tipo ciclo"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El argumento del ciclo debe ser mayor a 50"
                                                        break
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El argumento del ciclo debe ser un numero entero"
                                                    break
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El argumento debe finalizar con )"
                                                break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El argumento iniciar con ("
                                            break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> La linea debe terminar en :"
                                        break
                                #Es el nombre Hoja?
                                elif re.search("^Hoja",nombre):
                                    #Es la hoja correcta?
                                    if nombre[0:len(nombre)-1]==str(obje[0].nombre):
                                        #Termina la linea con :
                                        if nombre[-1]==":":
                                            #Ya se ha declarado el evento de hoja?
                                            if token in variablesDeclaradas:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El evento de Hoja ya fue declarado"
                                                break
                                            else:
                                                variablesDeclaradas.append(token)
                                                abiertoBloque=str(token)
                                                #print "Ok es un evento de hoja correcto"
                                                #"alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"
                                                if token=="alAbrir":
                                                    script=script+ "$(window).load(function(){;"
                                                elif token=="alCerrar":
                                                    script=script+ "$(window).unload(function(){"
                                                elif token =="alPresionarTecla":
                                                    script=script+ "$(document).keypress(function(e){"
                                                elif token =="alSoltarTecla":
                                                    script=script+ "$(window).keyup(function(e){"
                                                elif token =="alPulsarTecla":
                                                    script=script+ "$(document).keydown(function(e){"
                                                    teclas=True
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Estas Funciones aun no estan implementadas"
                                                    break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> La linea debe terminar en :"
                                            break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> Esta hoja no existe"
                                else:
                                    descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(nombre[-1])+" No existe"
                                    break
                            #es un evento de Objeto?
                            elif token in eventosObjetos:
                                declaracionVariables=False
                                inicioLinea=False
                                nm=False
                                #el objeto existe realmente?
                                for i in range(len(obje)):
                                    if nombre[0:-1] == obje[i].nombre:
                                        print nombre[0:-1]
                                        nm=True
                                        break
                                if nm==True:
                                    #termina la linea con :?
                                    if nombre[-1] == ":":
                                        #Tiene algun caracter extraño?
                                        print nombre[0:-1]
                                        if re.search("^[a-zA-Z0-9]*$",nombre[0:-1]):
                                            #termina con un numero?
                                            if re.search("[0-9]$",nombre[0:-1]):
                                                #empieza con una letra Mayuscula?
                                                if re.search("^[A-Z]",nombre[0:-1]):
                                                    #el resto es minusculas?
                                                    if re.search("^[A-Z].[^A-Z]",nombre[0:-1]):
                                                        #print "Ok el objeto es correcto"
                                                        #"click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"
                                                        abiertoBloque=token
                                                        if token=="click":
                                                            script=script+ "$('#"+str(nombre[0:-1])+"').click(function(){"
                                                        elif token=="dobleClick":
                                                            script=script+ "$('#"+str(nombre[0:-1])+"').dblclick(function(){"
                                                        elif token=="ratonSobre":
                                                            script=script+ "$('#"+str(nombre[0:-1])+"').mouseover(function(){"
                                                        elif token=="ratonFuera":
                                                            script=script+ "$('#"+str(nombre[0:-1])+"').mouseout(function(){"
                                                        elif token=="ratonPresionado":
                                                            script=script+ "$('#"+str(nombre[0:-1])+"').mousedown(function(){"
                                                        elif token=="ratonLiberado":
                                                            script=script+ "$('#"+str(nombre[0:-1])+"').mouseup(function(){"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El nombre del objeto "+str(nombre[-1])+" solo de contener la primera letra en Mayuscula"
                                                        break
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El nombre del objeto "+str(nombre[-1])+" debe iniciar con letra mayuscula"
                                                    break
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El nombre del objeto "+str(nombre[-1])+" debe culminar en un numero"
                                                break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El nombre del objeto "+str(nombre[-1])+" no debe contener caracteres especiales"
                                            break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> La linea debe terminar en :"
                                        break
                                else:
                                    descrError= "ERROR en la linea "+str(i+1)+"=> El objeto NO EXISTE"
                                    break
                            #es una funcion?
                            elif token=="func":
                                print "Posblimente una funcion"
                            #ninguna de las anteriores?
                            else:
                                descrError= "ERROR en la linea "+str(i+1)+"=> el inicio de linea no se reconoce"
                                break
                        else:
                            descrError= "ERROR en la linea "+str(i+1)+"=> falta apuntador '->'"
                            break
                #inicioLinea false
                else:
                    #comienza con un tab?
                    if re.search("^\t",linea):
                        #tiene el apuntador?
                        if re.search("->",linea):
                            token=linea.split("->")[0]
                            nombre=linea.split("->")[1]
                            #es una variable valida?
                            print str(token)+" dentro de un bloque"
                            if token in variablesValidas:
                                #es una variable local?
                                if re.search("^\tvarl",linea):
                                    #esta asignada?
                                    if re.search("=",nombre):
                                        variable=nombre.split("=")[0]
                                        asignacion=nombre.split("=")[1]
                                        #contiene solo letras minusculas?
                                        if re.search("^[a-z]*$",variable):
                                            #Ya fue declarada?
                                            if nombre in variablesDeclaradas:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> Esta variable ya fue declarada"
                                                break
                                            #No ha sido declarada
                                            else:
                                                v=nombre.split("=")
                                                variablesDeclaradas.append(v[0])
                                                #esta vacia la asignacion
                                                if asignacion=="":
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" requiere de una asignacion (=) no vacia"
                                                    break
                                                #es una variable numerica?
                                                elif re.search("^[0-9]*.[0-9]*$",asignacion):
                                                    #print "posible numero"
                                                    script=script+"var "+variable+" = "+asignacion+";"
                                                #es una variable de texto
                                                elif re.search("^\"*.*\"$",asignacion):
                                                    #print "posible cadena"
                                                    script=script+"var "+variable+" = "+asignacion+";"
                                                #asignacion de algun metodo o funcion?
                                                elif "\t"+asignacion.split("(")[0] in elementosBloque:
                                                    #solo las permitidas que retornan valores
                                                    if asignacion.split("(")[0]=="propiedad":
                                                        #print "asignada retorna propiedad"
                                                        param=asignacion.split("(")
                                                        param=param[1].split(",")
                                                        #retorna el valor de la propiedad
                                                        if len(param)==2:
                                                            ob=False
                                                            obt=0
                                                            #buscamos el objeto
                                                            for i in range(0,len(obje)):
                                                                if(obje[i].nombre == param[0]):
                                                                    atributos= obje[i].__dict__
                                                                    ob=True
                                                                    obt=i
                                                                    break
                                                            #No existe?
                                                            if ob==False:
                                                                descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[1])+" No existe"
                                                                break
                                                            #Si existe?
                                                            else:
                                                                atr=param[1]
                                                                atr=atr[0:len(atr)-1]
                                                                if atr in atributos:
                                                                    if atr=="colorFondo":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('background-color');"
                                                                    elif atr=="transparencia":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('opacity');"
                                                                    elif atr=="ancho":
                                                                        script=script+"var "+str(variable)+"=(parseInt($('#"+str(param[0])+"').css('width'))/parseInt(wh))*100;"
                                                                    elif atr=="alto":
                                                                        script=script+"var "+str(variable)+"=(parseInt($('#"+str(param[0])+"').css('height'))/parseInt(hh))*100;"
                                                                    elif atr=="x":
                                                                        script=script+"var "+str(variable)+"=(parseInt($('#"+str(param[0])+"').css('left'))/parseInt(wh))*100;"
                                                                    elif atr=="y":
                                                                        script=script+"var "+str(variable)+"=(parseInt($('#"+str(param[0])+"').css('top'))/parseInt(hh))*100;"
                                                                    elif atr=="borde":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('border-style');"
                                                                    elif atr=="colorBorde":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('border-color');"
                                                                    elif atr=="anchoBorde":
                                                                        script=script+"var "+str(variable)+"=parseInt($('#"+str(param[0])+"').css('border-width'));"
                                                                    elif atr=="sombra":
                                                                        script=script+"var "+str(variable)+"='"+str(obje[obt].sombra)+"';"
                                                                    elif atr=="rotar":
                                                                        script=script+"var "+str(variable)+"='"+str(obje[obt].rotar)+"';"
                                                                    elif atr=="oculto":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('display');"
                                                                    elif atr=="radio":
                                                                        script=script+"var "+str(variable)+"='"+str(obje[obt].radio)+"';"
                                                                    elif atr=="imagen":
                                                                        script=script+"var "+str(variable)+"='$('#"+str(param[0])+"').attr('src');"
                                                                    elif atr=="texto":
                                                                        script=script+"var "+str(variable)+"='$('#"+str(param[0])+"').text();"
                                                                    elif atr=="tamanoTexto":
                                                                        script=script+"var "+str(variable)+"=parseInt($('#"+str(param[0])+"').css('font-size'));"
                                                                    elif atr=="colorTexto":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('color');"
                                                                    elif atr=="fuente":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('font-family');"
                                                                    elif atr=="alineacion":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').css('align');"
                                                                    elif atr=="lista":
                                                                        script=script+"var "+str(variable)+"='"+str(obje[obt].lista)+"';"
                                                                    elif atr=="valor":
                                                                        script=script+"var "+str(variable)+"=$('#"+str(param[0])+"').val();"
                                                                    else:
                                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" no tiene la propiedad "+str(param[1])
                                                                        break
                                                                else:
                                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" no tiene la propiedad "+str(param[1])
                                                                    break
                                                        else:
                                                            descrError= "ERROR en la linea "+str(i+1)+"=> propiedad admite solo 2 argumentos en este contexto"
                                                            break
                                                    elif asignacion.split("(")[0]=="confirmacion":
                                                        #print "asignada confirmacion"
                                                        atr=asignacion.split("(")[1]
                                                        atr=atr[0:len(atr)-1]
                                                        script=script+"var "+variable+"=confirm('"+atr+"');"
                                                    elif asignacion.split("(")[0]=="entrada":
                                                        #print "entrada"
                                                        atr=asignacion.split("(")[1]
                                                        atr=atr[0:len(atr)-1]
                                                        script=script+"var "+variable+"=prompt('"+atr+"');"
                                                    elif asignacion.split("(")[0]=="leerDato":
                                                        atr=asignacion.split("(")[1]
                                                        atr=atr[0:len(atr)-1]
                                                        script=script+str(variable)+"=sessionStorage."+str(atr)+";"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" no se le puede asignar valor" 
                                                        break
                                                #ninguna de las anteriores
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" no se le puede asignar ese valor"
                                                    break
                                        elif asignacion.split("(")[0]=="aritmetica":
                                            #print aritmetica
                                            atr=asignacion.split("(")[1]
                                            atr=atr[0:len(atr)-1]
                                            script=script+"var "+variable+"=parseFloat("+str(atr)+");"
                                        
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" solo puede contener letras minusculas"
                                            break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" requiere de una asignacion (=)"
                                        break
                                # es una variable general?
                                elif re.search("^\tvarg",linea):
                                    #tiene asignacion?
                                    if re.search("=",nombre):
                                        variable=nombre.split("=")[0]
                                        asignacion=nombre.split("=")[1]
                                        #contiene solo letras minusculas?
                                        if re.search("^[a-z]*$",variable):
                                            #Ya fue declarada?
                                            if variable not in variablesDeclaradas:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" No ha sido declarada"
                                                break
                                            #Ya ha sido declarada
                                            else:
                                                #esta vacia la asignacion
                                                if asignacion=="":
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" requiere de una asignacion (=) no vacia"
                                                    break
                                                #es una variable numerica?
                                                elif re.search("^[0-9]*.[0-9]*$",asignacion):
                                                    #print "posible numero"
                                                    script=script+" "+variable+" = "+asignacion+";"
                                                #es una variable de texto
                                                elif re.search("^\"*.*\"$",asignacion):
                                                    #print "posible cadena"
                                                    script=script+" "+variable+" = '"+asignacion+"';"
                                                #asignacion de algun metodo o funcion?
                                                elif "\t"+asignacion.split("(")[0] in elementosBloque:
                                                    #solo las permitidas que retornan valores
                                                    if asignacion.split("(")[0]=="propiedad":
                                                        print "asignada retorna propiedad"
                                                        #print "asignada retorna propiedad"
                                                        param=asignacion.split("(")
                                                        param=param[1].split(",")
                                                        #retorna el valor de la propiedad
                                                        if len(param)==2:
                                                            ob=False
                                                            obt=0
                                                            #buscamos el objeto
                                                            for i in range(0,len(obje)):
                                                                if(obje[i].nombre == param[0]):
                                                                    atributos= obje[i].__dict__
                                                                    ob=True
                                                                    obt=i
                                                                    break
                                                            #No existe?
                                                            if ob==False:
                                                                descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[1])+" No existe"
                                                                break
                                                            #Si existe?
                                                            else:
                                                                atr=param[1]
                                                                atr=atr[0:len(atr)-1]
                                                                if atr in atributos:
                                                                    if atr=="colorFondo":
                                                                        script=script+" "+str(variable)+"=$('#"+str(param[0])+"').css('background-color');"
                                                                    elif atr=="transparencia":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].transparencia)+"';"
                                                                    elif atr=="ancho":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].ancho)+"';"
                                                                    elif atr=="alto":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].alto)+"';"
                                                                    elif atr=="x":
                                                                       script=script+"var "+str(variable)+"=(parseInt($('#"+str(param[0])+"').css('left'))/parseInt(wh))*100;"
                                                                    elif atr=="y":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].y)+"';"
                                                                    elif atr=="borde":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].borde)+"';"
                                                                    elif atr=="colorBorde":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].colorBorde)+"';"
                                                                    elif atr=="anchoBorde":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].anchoBorde)+"';"
                                                                    elif atr=="sombra":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].sombra)+"';"
                                                                    elif atr=="rotar":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].rotar)+"';"
                                                                    elif atr=="oculto":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].oculto)+"';"
                                                                    elif atr=="radio":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].radio)+"';"
                                                                    elif atr=="imagen":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].imagen)+"';"
                                                                    elif atr=="texto":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].texto)+"';"
                                                                    elif atr=="tamanoTexto":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].tamanoTexto)+"';"
                                                                    elif atr=="colorTexto":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].colorTexto)+"';"
                                                                    elif atr=="fuente":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].fuente)+"';"
                                                                    elif atr=="alineacion":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].alineacion)+"';"
                                                                    elif atr=="lista":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].lista)+"';"
                                                                    elif atr=="valor":
                                                                        script=script+" "+str(variable)+"='"+str(obje[obt].valor)+"';"
                                                                    else:
                                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" no tiene la propiedad "+str(param[1])
                                                                        break
                                                                else:
                                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" no tiene la propiedad "+str(param[1])
                                                                    break
                                                        else:
                                                            descrError= "ERROR en la linea "+str(i+1)+"=> propiedad admite solo 2 argumentos en este contexto"
                                                            break
                                                    elif asignacion.split("(")[0]=="confirmacion":
                                                        print "asignada confirmacion"
                                                    elif asignacion.split("(")[0]=="entrada":
                                                        print "entrada"
                                                    elif asignacion.split("(")[0]=="leerDato":
                                                        atr=asignacion.split("(")[1]
                                                        atr=atr[0:len(atr)-1]
                                                        script=script+str(variable)+"=sessionStorage."+str(atr)+";"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo no retorna valores"
                                                        break
                                                elif asignacion.split("(")[0]=="aritmetica":
                                                    #print aritmetica
                                                    atr=asignacion.split("(")[1]
                                                    atr=atr[0:len(atr)-1]
                                                    script=script+" "+variable+"=parseFloat("+str(atr)+");"
                                                #ninguna de las anteriores
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" no se le puede asignar ese valor"
                                                    break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" solo puede contener letras minusculas"
                                            break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" requiere de una asignacion (=) no vacia"
                                        break
                                # no es un variable
                                else:
                                    descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" No ha sido declarada"
                                    break
                            elif token.split("\t")[1] in eventosObjetos:
                                descrError= "ERROR en la linea "+str(i+1)+"=> No puede colocar un evento de objeto dentro de otro"
                                break
                            elif token.split("\t")[1] in eventosValidos:
                                descrError= "ERROR en la linea "+str(i+1)+"=> No puede colocar un evento dentro de un evento de objeto"
                                break
                            elif re.search("^\tfin",token):
                                if nombre.split("(")[0]=="Si":
                                    script=script+"};"
                                    condicional=""
                                elif nombre.split("(")[0]=="tecla":
                                    script=script+"};"
                                    cierraTecla=False
                            else:
                                descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(nombre)+" No tiene validez"
                                break
                        else:
                            #No tiene apuntador
                            variablesLocales=False
                            #Probamos con elementos de bloque
                            token=linea.split("(")[0]
                            parametro=linea.split("(")[1]
                            print token
                            #es un elemento de bloque?
                            if token in elementosBloque:
                                #cual elemento es?
                                if token=="\tpropiedad":
                                    param=parametro.split(",")
                                    #retorna el valor de la propiedad
                                    if len(param)==2:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> No se asigno propiedad a una variable"
                                    #asigna valor a la propiedad
                                    elif len(param)==3:
                                        ob=False
                                        #buscamos el objeto
                                        for i in range(0,len(obje)):
                                            if(obje[i].nombre == param[0]):
                                                atributos= obje[i].__dict__
                                                ob=True
                                                break
                                        #No existe?
                                        if ob==False:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" No existe"
                                            break
                                        #Si existe?
                                        else:
                                            atr=param[1]
                                            if atr in atributos:
                                                valor=param[2]
                                                valor=valor[0:len(valor)-1]
                                                #print "Ok asignamos el valor "+valor[0:len(valor)-1]
                                                if atr=="colorFondo":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('background-color',"+str(valor)+");"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('background-color','"+str(colores[valor])+"');"
                                                elif atr=="transparencia":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('opacity',"+str(valor)+");"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('opacity','"+str(valor)+"');"
                                                elif atr=="ancho":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('width',"+str(valor)+"+'%');"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('width','"+str(valor)+"%');"
                                                elif atr=="alto":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('height',"+str(valor)+"+'%');"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('height','"+str(valor)+"%');"
                                                elif atr=="x":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('left',"+str(valor)+"+'%');"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('left','"+str(valor)+"%');"
                                                elif atr=="y":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('top',"+str(valor)+"+'%');"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('top','"+str(valor)+"%');"
                                                elif atr=="borde":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('border-style',"+str(valor)+");"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('border-style','"+str(bordes[valor])+"');"
                                                elif atr=="colorBorde":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('border-color',"+str(valor)+");"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('border-color','"+str(colores[valor])+"');"
                                                elif atr=="anchoBorde":
                                                    if valor in variablesDeclaradas:
                                                        script=script+"$('#"+str(param[0])+"').css('border-width',"+str(valor)+"'px');"
                                                    else:
                                                        script=script+"$('#"+str(param[0])+"').css('border-width','"+str(valor)+"px');"
                                                elif atr=="sombra":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].sombra)+"';"
                                                elif atr=="rotar":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].rotar)+"';"
                                                elif atr=="oculto":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].oculto)+"';"
                                                elif atr=="radio":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].radio)+"';"
                                                elif atr=="imagen":
                                                    script=script+"$('#"+str(param[0])+"').attr('src','"+str(atributos['rt'])+str(valor)+"');"
                                                elif atr=="texto":
                                                     script=script+"$('#"+str(param[0])+"').text("+str(valor)+");"
                                                elif atr=="tamanoTexto":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].tamanoTexto)+"';"
                                                elif atr=="colorTexto":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].colorTexto)+"';"
                                                elif atr=="fuente":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].fuente)+"';"
                                                elif atr=="alineacion":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].alineacion)+"';"
                                                elif atr=="lista":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].lista)+"';"
                                                elif atr=="valor":
                                                    script=script+"var "+str(variable)+"='"+str(obje[obt].valor)+"';"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" no tiene la propiedad "+str(param[1])
                                                    break
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" No tiene la propiedad "+str(param[1])
                                                break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> propiedad debe tener 2 o 3 parametros"
                                        break
                                elif token=="\tmostrar":
                                    param=parametro.split(",")
                                    if len(param)==2:
                                        ob=False
                                        #buscamos el objeto
                                        for i in range(0,len(obje)):
                                            if(obje[i].nombre == param[0]):
                                                ob=True
                                                break
                                        #No existe?
                                        if ob==False:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[1])+" No existe"
                                            break
                                        #Si existe?
                                        else:
                                            atr=param[1]
                                            atr=atr[0:len(atr)-1]
                                            if atr == "Si":
                                                print "ok mostramos con efecto"
                                                script=script+"$('#"+param[0]+"').show('slow');"
                                            elif atr == "No":
                                                print "ok mostramos sin efecto"
                                                script=script+"$('#"+param[0]+"').show();"
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el segundo parametro sea (Si o No)"
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere dos parametros"
                                        break
                                elif token=="\tocultar":
                                    param=parametro.split(",")
                                    if len(param)==2:
                                        ob=False
                                        #buscamos el objeto
                                        for i in range(0,len(obje)):
                                            if(obje[i].nombre == param[0]):
                                                ob=True
                                                break
                                        #No existe?
                                        if ob==False:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[1])+" No existe"
                                            break
                                        #Si existe?
                                        else:
                                            atr=param[1]
                                            atr=atr[0:len(atr)-1]
                                            if atr == "Si":
                                                print "ok ocultamos con efecto"
                                                script=script+"$('#"+param[0]+"').hide('slow');"
                                            elif atr == "No":
                                                print "ok ocultamos sin efecto"
                                                script=script+"$('#"+param[0]+"').hide();"
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el segundo parametro sea (Si o No)"
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere dos parametros"
                                        break
                                elif token=="\trotar":
                                    param=parametro.split(",")
                                    if len(param)==3:
                                        ob=False
                                        #buscamos el objeto
                                        for i in range(0,len(obje)):
                                            if(obje[i].nombre == param[0]):
                                                ob=True
                                                break
                                        #No existe?
                                        if ob==False:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[1])+" No existe"
                                            break
                                        #Si existe?
                                        else:
                                            atr=param[1]
                                            if atr == "Si":
                                                valor=param[2]
                                                valor=valor[0:len(valor)-1]
                                                if valor[0:len(valor)-1].isdigit():
                                                    script+="$('#"+param[0]+"').css({WebkitTransform: 'rotate("+str(valor)+"deg)'});"
                                                    print "ok rotamos con efecto" +valor[0:len(valor)-1]
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El parametro 3 debe ser un digito"
                                                    break
                                            elif atr == "No":
                                                valor=param[2]
                                                if valor[0:len(valor)-1].isdigit():
                                                    print "ok rotamos sin efecto" +valor[0:len(valor)-1]
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El parametro 3 debe ser un digito"
                                                    break
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el segundo parametro sea (Si o No)"
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere tres parametros"
                                        break
                                elif token=="\tmover":
                                    param=parametro.split(",")
                                    if len(param)==4:
                                        ob=False
                                        #buscamos el objeto
                                        for i in range(0,len(obje)):
                                            if(obje[i].nombre == param[0]):
                                                ob=True
                                                break
                                        #No existe?
                                        if ob==False:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[0])+" No existe"
                                            break
                                        #Si existe?
                                        else:
                                            if param[1].isdigit():
                                                if param[2].isdigit():
                                                    atr=param[3]
                                                    atr=atr[0:len(atr)-1]
                                                    print atr
                                                    if atr=="Si":
                                                        script+="$('#"+param[0]+"').animate({left:'"+str(param[1])+"%',top:'"+str(param[2])+"%'},'slow');"
                                                    elif atr=="No":
                                                        script+="$('#"+param[0]+"').css({left:'"+str(param[1])+"%',top:'"+str(param[2])+"%'});"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el cuarto parametro sea (Si o No)"
                                                        break
                                                elif param[2] in variablesDeclaradas:
                                                    atr=param[3]
                                                    atr=atr[0:len(atr)-1]
                                                    print atr
                                                    if atr=="Si":
                                                        script+="$('#"+param[0]+"').animate({left:'"+str(param[1])+"%',top:"+str(param[2])+"+'%'},'slow');"
                                                    elif atr=="No":
                                                        script+="$('#"+param[0]+"').css({left:'"+str(param[1])+"%',top:"+str(param[2])+"+'%'});"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el cuarto parametro sea (Si o No)"
                                                        break
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El tercer argumento debe ser un entero o una variable"
                                                    break
                                            elif param[1] in variablesDeclaradas:
                                                if param[2].isdigit():
                                                    atr=param[3]
                                                    atr=atr[0:len(atr)-1]
                                                    print atr
                                                    if atr=="Si":
                                                        script+="$('#"+param[0]+"').animate({left:"+str(param[1])+"+'%',top:'"+str(param[2])+"%'},'slow');"
                                                    elif atr=="No":
                                                        script+="$('#"+param[0]+"').css({left:"+str(param[1])+"+'%',top:'"+str(param[2])+"%'});"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el cuarto parametro sea (Si o No)"
                                                        break
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El segundo argumento debe ser un entero o una variable"
                                                break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere cuatro parametros"
                                        break
                                elif token=="\tredimensionar":
                                    param=parametro.split(",")
                                    if len(param)==4:
                                        ob=False
                                        #buscamos el objeto
                                        for i in range(0,len(obje)):
                                            if(obje[i].nombre == param[0]):
                                                ob=True
                                                break
                                        #No existe?
                                        if ob==False:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El objeto "+str(param[1])+" No existe"
                                            break
                                        #Si existe?
                                        else:
                                            if param[2].isdigit():
                                                if param[1].isdigit():
                                                    atr=param[3]
                                                    atr=atr[0:len(atr)-1]
                                                    if atr == "Si":
                                                        script+="$('#"+param[0]+"').animate({width:'"+str(param[1])+"%',height:'"+str(param[2])+"%'},'slow');"
                                                    elif atr == "No":
                                                        script+="$('#"+param[0]+"').css({width:'"+str(param[1])+"%',height:'"+str(param[2])+"%'});"
                                                    else:
                                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere que el cuarto parametro sea (Si o No)"
                                                        break
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> El tercer argumento debe ser un entero"
                                                    break
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El segundo argumento debe ser un entero"
                                                break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere cuatro parametros"
                                        break
                                elif token=="\tmensaje":
                                    parametro=parametro[0:len(parametro)-1]
                                    if parametro in variablesDeclaradas:
                                        script=script+"alert("+parametro+");"
                                    else:
                                        script=script+"alert('"+parametro+"');"
                                elif token=="\tconfirmacion":
                                    descrError= "ERROR en la linea "+str(i+1)+"=> Este metodo debe ser asignado"
                                    break
                                elif token=="\tentrada":
                                    descrError= "ERROR en la linea "+str(i+1)+"=> Este metodo debe ser asignado"
                                    break
                                elif token=="\insertarObjeto":
                                    parametro=parametro[0:len(parametro)-1]
                                    print variablesDeclaradas
                                    if parametro in variablesDeclaradas:
                                        script=script+"$(document.body).append("+parametro+");"
                                    else:
                                        script=script+"$(document.body).append('"+parametro+"');"
                                elif token=="\tinc":
                                    param=parametro.split(",")
                                    if len(param)==2:
                                        parametro=param[0]
                                        atr=param[1]
                                        atr=atr[0:len(param[1])-1]
                                        if parametro in variablesDeclaradas:
                                            if atr.isdigit():
                                                script=script+str(parametro)+"="+str(parametro)+"+"+str(atr)+";"
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El segundo argumento debe ser un entero"
                                                break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(parametro)+" no existe"
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere dos parametros"
                                        break
                                elif token=="\tdec":
                                    param=parametro.split(",")
                                    if len(param)==2:
                                        parametro=param[0]
                                        atr=param[1]
                                        atr=atr[0:len(param[1])-1]
                                        if parametro in variablesDeclaradas:
                                            if atr.isdigit():
                                                script=script+str(parametro)+"="+str(parametro)+"-"+str(atr)+";"
                                            else:
                                                descrError= "ERROR en la linea "+str(i+1)+"=> El segundo argumento debe ser un entero"
                                                break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> La variable "+str(parametro)+" no existe"
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere dos parametros"
                                elif token=="\tsonido":
                                    parametro=parametro[0:len(parametro)-1]
                                    param=parametro.split(",")
                                    if len(param)==2:
                                        parametro=parametro[0:len(parametro)-1]
                                        if param[1]=="pausa":
                                            script=script+"document.getElementById('"+param[0]+"').pause();"
                                        elif param[1]=="detener":
                                            script=script+"document.getElementById('"+param[0]+"').pause();document.getElementById('"+param[0]+"').currentTime=0;"
                                        elif param[1]=="volumen+":
                                            script=script+"document.getElementById('"+param[0]+"').volume += 0.1;"
                                        elif param[1]=="volumen-":
                                            script=script+"document.getElementById('"+param[0]+"').volume -= 0.1;"
                                        elif param[1]=="ciclo":
                                            script=script+"document.getElementById('"+param[0]+"').loop=true;document.getElementById('"+param[0]+"').play();"
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> El segundo parametro de sonido no se reconoce"
                                            break
                                    else:
                                        script=script+"document.getElementById('"+parametro+"').play();"
                                elif token=="\thoja":
                                    parametro=parametro[0:len(parametro)-1]
                                    script=script+"$(document).prop('title','"+parametro+"');"
                                elif token=="\tescribirDato":
                                    param=parametro.split(",")
                                    if len(param)==2:
                                        parametro=param[0]
                                        atr=param[1]
                                        atr=atr[0:len(param[1])-1]
                                        script=script+"sessionStorage."+str(parametro)+"="+str(atr)+";"
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> El metodo requiere dos parametros"
                                        break
                                elif token=="\ttecla":
                                    if teclas:
                                        parametro=parametro[0:len(parametro)-1]
                                        script=script+"if(e.keyCode=="+str(parametro)+"){"
                                        cierraTecla=True
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> Este Metodo solo puede ser usado con el evento de Hoja PulsarTecla, SoltarTecla"
                                        break
                                elif token=="\tcronometro":
                                    parametro=parametro[0:len(parametro)-1]
                                    script=script+"crono0.play();"
                                elif token=="\tesperar":
                                    parametro=parametro[0:len(parametro)-1]
                                    script=script+"espera("+str(parametro)+");"
                                elif token=="\tSi":
                                    parametro=parametro[0:len(parametro)-1]
                                    if parametro==None:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> Debe indicar los criterios de comparacion"
                                        break
                                    elif re.search("=",parametro):
                                        if parametro.split("=")[0] in variablesDeclaradas:
                                            if parametro.split("=")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split("=")[0])+"=="+str(parametro.split("=")[1])+"){"
                                            else:
                                                if re.search("^[0-9]*.[0-9]*$",parametro.split("=")[1]):
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split("=")[0])+"=="+str(parametro.split("=")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        elif re.search("^[0-9]*.[0-9]*$",parametro.split("=")[0]):
                                            if parametro.split("=")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split("=")[0])+"=="+str(parametro.split("=")[1])+"){"
                                            else:
                                                if parametro.split("=")[0] in variablesDeclaradas:
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split("=")[0])+"=="+str(parametro.split("=")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                            break
                                    elif re.search(">",parametro):
                                        if parametro.split(">")[0] in variablesDeclaradas:
                                            if parametro.split(">")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split(">")[0])+">"+str(parametro.split(">")[1])+"){"
                                            else:
                                                if re.search("^[0-9]*.[0-9]*$",parametro.split(">")[1]):
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split(">")[0])+">"+str(parametro.split(">")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        elif re.search("^[0-9]*.[0-9]*$",parametro.split(">")[0]):
                                            if parametro.split(">")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split(">")[0])+">"+str(parametro.split(">")[1])+"){"
                                            else:
                                                if parametro.split(">")[0] in variablesDeclaradas:
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split(">")[0])+">"+str(parametro.split(">")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                            break
                                    elif re.search("<",parametro):
                                        if parametro.split("<")[0] in variablesDeclaradas:
                                            if parametro.split("<")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split("<")[0])+"<"+str(parametro.split("<")[1])+"){"
                                            else:
                                                if re.search("^[0-9]*.[0-9]*$",parametro.split("<")[1]):
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split("<")[0])+"<"+str(parametro.split("<")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        elif re.search("^[0-9]*.[0-9]*$",parametro.split("<")[0]):
                                            if parametro.split("<")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split("<")[0])+"<"+str(parametro.split("<")[1])+"){"
                                            else:
                                                if parametro.split("<")[0] in variablesDeclaradas:
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split("=")[0])+"<"+str(parametro.split("<")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                            break
                                    elif re.search("!",parametro):
                                        if parametro.split("!")[0] in variablesDeclaradas:
                                            if parametro.split("!")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split("!")[0])+"!="+str(parametro.split("!")[1])+"){"
                                            else:
                                                if re.search("^[0-9]*.[0-9]*$",parametro.split("!")[1]):
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split("!")[0])+"!="+str(parametro.split("!")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        elif re.search("^[0-9]*.[0-9]*$",parametro.split("!")[0]):
                                            if parametro.split("!")[1] in variablesDeclaradas:
                                                condicional="Si"
                                                script=script+"if("+str(parametro.split("!")[0])+"!="+str(parametro.split("!")[1])+"){"
                                            else:
                                                if parametro.split("!")[0] in variablesDeclaradas:
                                                    condicional="Si"
                                                    script=script+"if("+str(parametro.split("!")[0])+"!="+str(parametro.split("!")[1])+"){"
                                                else:
                                                    descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                                    break
                                        else:
                                            descrError= "ERROR en la linea "+str(i+1)+"=> Los parametros de comparacion deben ser una variable o un valor numerico"
                                            break
                                    else:
                                        descrError= "ERROR en la linea "+str(i+1)+"=> Se requiere de un operador de comparacion (=,<,>,!)"
                                        break
                                else:
                                    descrError= "ERROR en la linea "+str(i+1)+"=> No se conoce la accion"
                                    break
                            else:
                                descrError= "ERROR en la linea "+str(i+1)+"=> No se conoce la accion"
                                break
                    #empieza por fin->?
                    elif re.search("^fin->",linea):
                        if condicional!="":
                            descrError= "ERROR en la linea "+str(i+1)+"=> El bloque del Condicional debe cerrarse (fin->)"
                            break
                        #Cierra el bloque abierto?
                        if linea.split("->")[1]==abiertoBloque:
                            if abiertoBloque=="cicloSistema":
                                script=script+"});timer.set({ time : 100, autostart : true });"
                            elif abiertoBloque=="cronometroSistema":
                                script=script+"});crono"+str(cron-1)+".set({ time : 500, autostart : false });"
                            else:
                                script=script+"});"
                            inicioLinea=True
                            abiertoBloque=""
                            variablesLocales=True
                            teclas=False
                        else:
                            descrError= "ERROR en la linea "+str(i+1)+"=> El bloque de evento debe cerrarse (fin->)"
                        if cierraTecla:
                            descrError= "ERROR en la linea "+str(i+1)+"=> El bloque de la Tecla debe cerrarse (fin->)"
                            break
                    else:
                        descrError= "ERROR en la linea "+str(i+1)+"=> Dentro del bloque debe inciar con 'tab'"
                        break
            else:
                linea=""
                continue
        script=script+"function espera(ms){var ini=new Date().getTime();for(i=0;i<1e7;i++){if((new Date().getTime()-ini)>ms){break}}}});"
        obje[0].javascript=""
        obje[0].escritos=""
        print script
        obje[0].javascript="<script>"+script+"</script>"
        obje[0].escritos=data.get_text(*data.get_bounds())
        self.barraEstado.push(0,descrError)
