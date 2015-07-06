# -*- coding: utf-8 -*-
import glib
import gtk
import pango
import re
import os
ruta= os.path.dirname(os.path.realpath(__file__))

class Analizador():
    def __init__(self,objetos,escena):
        self.__objetos=objetos
        self.__escena=escena
        eventosEscena=["alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        eventosObjetos=["click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"]
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("editor de escritos")
        self.window.set_size_request(600,600)
        self.window.set_resizable(False)
        self.window.set_modal(True)
        self.barraEstado = gtk.Statusbar()
        color = gtk.gdk.color_parse('#ffffff')
        self.window.modify_bg(gtk.STATE_NORMAL, color)
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
        cntScript.set_text(escena.escritos)
        barraSCAN.connect("clicked",self.analizador,cntScript)
        lista=gtk.TreeStore(str,gtk.gdk.Pixbuf)
        padre=lista.append(None,["Sistema",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/sistema.png'))])
        f=lista.append(padre,["cicloSistema",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/ciclo.png'))])
        f=lista.append(padre,["cronometroSistema",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/ciclo.png'))])
        padre=lista.append(None,[escena.nombre,gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/hoja.png'))])
        for n in range(len(eventosEscena)):
            f=lista.append(padre,[eventosEscena[n],gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/evento.png'))])
        for i in range(len(objetos)):
            padre=lista.append(None,[objetos[i]["objeto"].nombre,gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/objeto.png'))])
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
        f=listaIzquierda.append(padre,["sonido",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
        f=listaIzquierda.append(padre,["video",gtk.gdk.pixbuf_new_from_file(os.path.join(ruta,'iconos/metodo.png'))])
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
        self.window.connect("delete_event",self.cerrar)
        self.window.add(caja)
        self.window.show_all()

    def cerrar(self,widget,data=None):
        return True

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

    def __tipoLinea(self,linea):
        eventosValidos=["cronometroSistema","cicloSistema","alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        eventosObjetos=["click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"]
        variablesValidas=["varg","\tvarl","\tvarg"]
        if re.search("^\t",linea):
            resultado= (0,1,"Elemento de bloque")
        else:
            token=linea.split("->")[0]
            nombre=linea.split("->")[1]
            if token in variablesValidas:
                resultado=self.__analisaVarible(token,nombre,"fuera")
            elif token in eventosValidos:
                pass
            elif token in eventosObjetos:
                pass
            elif token=="func":
                pass
            else:
                resultado= (0,0,None)
        return resultado
            
    def __analisaVarible(self,token,nombre,contexto):
        #tiene asignacion explicita?
        if re.search("=",nombre):
            print nombre
            variable=nombre.split("=")[0]
            asignacion=nombre.split("=")[1]
            #contiene solo letras minusculas?
            if re.search("^[a-z]*$",variable):
                #esta vacia la asignacion
                if asignacion==None:
                    return (0,1,None)
                #es una variable numerica?
                elif re.search("^[0-9]*.[0-9]*$",asignacion):
                    #print "posible numero"
                    if contexto=="fuera":
                        t="var "+variable+" = "+asignacion+";"
                    else:
                        t=variable+" = "+asignacion+";"
                #es una variable de texto
                elif re.search("^\"*.*\"$",asignacion):
                    #print "posible cadena"
                    if contexto=="fuera":
                        t="var "+variable+" = '"+asignacion+"';"
                    else:
                        t=variable+" = '"+asignacion+"';"
                elif asignacion.split("(")[0]=="aritmetica":
                        atr=asignacion.split("(")[1]
                        atr=atr[0:len(atr)-1]
                        if contexto=="fuera":
                            t="var "+variable+"="+str(atr)+";"
                        else:
                            t=variable+"="+str(atr)+";"
                elif asignacion.split("(")[0]=="arreglo":
                    atr=asignacion.split("(")[1]
                    atr=atr[0:len(atr)-1]
                    if len(atr)==0:
                        if contexto=="fuera":
                            t="var "+variable+"=new Array();"
                        else:
                            t=variable+"=new Array();"
                    else:
                        if contexto=="fuera":
                            t="var "+variable+"=new Array("+str(atr)+");"
                        else:
                            t=variable+"=new Array("+str(atr)+");"
                elif asignacion.split("(")[0]=="aleatorio":
                    atr=asignacion.split("(")[1]
                    atr=atr[0:len(atr)-1]
                    if contexto=="fuera":
                        t="var "+variable+"=Math.floor((Math.random() * "+str(atr)+") + 1);"
                    else:
                        t=variable+"=Math.floor((Math.random() * "+str(atr)+") + 1);"
                elif asignacion.split("(")[0]=="leerDato":
                    atr=asignacion.split("(")[1]
                    atr=atr[0:len(atr)-1]
                    if contexto=="fuera":
                        t="var "+str(variable)+"=sessionStorage."+str(atr)+";"
                    else:
                        t=str(variable)+"=sessionStorage."+str(atr)+";"
                #ninguna de las anteriores
                else:
                    return (0,2,None)
                return (1,0,t) 
            #es una variable de arreglo?
            elif re.search("^[a-z]+\[\d+\]",variable):
                if variable.split("[")[0] in variablesDeclaradas:
                    #es una variable numerica?
                    if re.search("^[0-9]*.[0-9]*$",asignacion):
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
                    elif asignacion.split("(")[0]=="arreglo":
                        atr=asignacion.split("(")[1]
                        atr=atr[0:len(atr)-1]
                        if len(atr)==0:
                            script+="var "+variable+"=new Array();"
                        else:
                            script+="var "+variable+"=new Array("+str(atr)+");"
                    elif asignacion.split("(")[0]=="aleatorio":
                        atr=asignacion.split("(")[1]
                        atr=atr[0:len(atr)-1]
                        script=script+" "+variable+"=Math.floor((Math.random() * "+str(atr)+") + 1);"
                    elif asignacion.split("(")[0]=="leerDato":
                        atr=asignacion.split("(")[1]
                        atr=atr[0:len(atr)-1]
                        script=script+str(variable)+"=sessionStorage."+str(atr)+";"
                    #ninguna de las anteriores
                    else:
                        descrError= "ERROR en la linea "+str(i+1)+" (311)> Al arreglo "+str(nombre)+" no se le puede asignar ese valor"
                else:
                    descrError= "ERROR en la linea "+str(i+1)+" (314)=> La asignacion "+str(nombre)+" no pertenece a un arreglo"
            #no tiene solo letras minusculas
            else:
                return (0,4,None)
        #No esta asignada
        else:
            return (0,3,None)
            

    def analizador(self,widget,data=None):
        errores=["No se Reconoce la linea",
        "La variable requiere de una asignacion (=) no vacia",
        "La variable no se le puede asignar ese valor",
        "La variable requiere de una asignacion (=)",
        "La variable solo puede contener letras minusculas"]
        tipoLinea=["variable"]
        eventosValidos=["cronometroSistema","cicloSistema","alAbrir","alCerrar","alPresionarTecla","alSoltarTecla","alPulsarTecla","alArrastrar","alFinArrastrar"]
        eventosObjetos=["click","dobleClick","ratonSobre","ratonFuera","ratonPresionado","ratonLiberado"]
        elementosBloque=["\tpropiedad","\tmostrar","\tocultar","\trotar","\tmover","\tredimensionar","\tmensaje","\tconfirmacion","\tentrada","\tmostrarPantalla","\tinc","\tdec","\tsonido","\tvideo","\thoja","\tSi","\tescribirDato","\tleerDato","\ttecla","\tesperar","\tcronometro","\tarreglo"]
        variablesValidas=["varg","\tvarl","\tvarg"]
        variablesDeclaradas=[]
        funcionesDeclaradas=[]
        colores={"defecto":"default","Negro":"#000000","Gris Oscuro":"#696969","Gris":"#808080","Gris Claro":"#A9A9A9","Blanco":"#FFFFFF","Rojo Oscuro":"#8B0000","Rojo":"#FF0000","Rojo Claro":"#FA8072","Rosado Oscuro":"#FF1493","Rosado":"#FF69B4","Rosado Claro":"#FFB6C1","Fucsia Oscuro":"#8A2BE2","Fucsia":"#FF00FF","Fucsia Claro":"#CD5C5C","Marron Oscuro":"#800000","Marron":"#8B4513","Marron Claro":"#A0522D","Naranja Oscuro":"#FF8C00","Naranja":"#FF4500","Naranja Claro":"#FF6347","Purpura Oscuro":"#4B0082","Purupura":"#800080","Purpura Claro":"#EE82EE","Amarillo Oscuro":"#FFD700","Amarillo":"#FFFF00","Amarillo Claro":"#F0E68C","Teal":"#008080","Azul Oscuro":"#000080","Azul":"#0000FF","Azul Claro":"#00BFFF","AguaMarina Oscuro":"#1E90FF","AguaMarina":"#00FFFF","AguaMarina Claro":"#00BFFF","Verde Oscuro":"#006400","Verde":"#008000","Verde Claro":"#3CB371","Lima":"#00FF00","Oliva Oscuro":"#556B2F","Oliva":"#808000","Oliva Claro":"#BDB76B"}
        bordes={"punteado":"dotted","discontinuo":"dashed","solido":"solid","doble":"double","acanalado":"groove","corrugado":"ridge","relieve bajo":"inset","relieve alto":"outset"}
        atributosOb={"colorFondo":"background-color","transparencia":"transparency","ancho":"width","alto":"height","x":"left","y":"top","borde":"border-style","colorBorde":"borderTopColor","anchoBorde":"border-width","sombra":"shadow","rotar":"-webkit-transform:rotate","oculto":"hidden","texto":"text","imagen":"src"}
        obje=self.__objetos
        esce=self.__escena
        
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
        descrError="Ok"
        funcionAbierta=False
        cron=0
        t=0
        script="$( document ).ready(function() { wh= parseInt(document.body.clientWidth);hh= parseInt(document.body.clientHeight);"
        for i in range(lineas-1):
            p1=data.get_iter_at_line(i)
            ncr=p1.get_chars_in_line()-1
            if ncr>0:#esto es para evitar el molestoso aborto de gtk cuando las linea esta vacia
                p2=data.get_iter_at_line_offset(i,ncr)
                linea = data.get_text(p1,p2)
                if linea!="":
                    print "linea "+str(i+1)+": "+linea
                    r=self.__tipoLinea(linea)
                    if r[0]==0:
                        print errores[r[1]]
                    else:
                        print "Tipo Linea:"+tipoLinea[r[1]]
                        print "Traduccion:"+r[2]
            else:
                linea=""
                continue
        '''else:
            script=script+"function espera(ms){var ini=new Date().getTime();for(i=0;i<1e7;i++){if((new Date().getTime()-ini)>ms){break}}}alert('"+str(descrError)+"')});"'''
                
        self.barraEstado.push(0,errores[r[1]])
        '''obje[0].javascript=""
        obje[0].escritos=""
        print script
        obje[0].javascript="<script>"+script+"</script>"
        obje[0].escritos=data.get_text(*data.get_bounds())
        '''
