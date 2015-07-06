# -*- coding: utf-8 -*-
import glib
import gtk
import webkit
colores={"defecto":"default","Negro":"#000000","Gris Oscuro":"#696969","Gris":"#808080","Gris Claro":"#A9A9A9","Blanco":"#FFFFFF","Rojo Oscuro":"#8B0000","Rojo":"#FF0000","Rojo Claro":"#FA8072","Rosado Oscuro":"#FF1493","Rosado":"#FF69B4","Rosado Claro":"#FFB6C1","Fucsia Oscuro":"#8A2BE2","Fucsia":"#FF00FF","Fucsia Claro":"#CD5C5C","Marron Oscuro":"#800000","Marron":"#8B4513","Marron Claro":"#A0522D","Naranja Oscuro":"#FF8C00","Naranja":"#FF4500","Naranja Claro":"#FF6347","Purpura Oscuro":"#4B0082","Purupura":"#800080","Purpura Claro":"#EE82EE","Amarillo Oscuro":"#FFD700","Amarillo":"#FFFF00","Amarillo Claro":"#F0E68C","Teal":"#008080","Azul Oscuro":"#000080","Azul":"#0000FF","Azul Claro":"#00BFFF","AguaMarina Oscuro":"#1E90FF","AguaMarina":"#00FFFF","AguaMarina Claro":"#00BFFF","Verde Oscuro":"#006400","Verde":"#008000","Verde Claro":"#3CB371","Lima":"#00FF00","Oliva Oscuro":"#556B2F","Oliva":"#808000","Oliva Claro":"#BDB76B"}
bordes={"punteado":"dotted","discontinuo":"dashed","solido":"solid","doble":"double","acanalado":"groove","corrugado":"ridge","relieve bajo":"inset","relieve alto":"outset"}

class ObjetoPrimario(object):
    def __init__(self):
        self.colorFondo="defecto"
        self.transparencia=1.0
        self.ancho=10
        self.alto=10
        self.x=1
        self.y=1
        self.borde="solido"
        self.colorBorde="Rojo"
        self.anchoBorde=1
        self.sombra="Falso"
        self.rotar=0
        self.oculto="Falso"
        self.etiqueta=None
        self.tip=None

    def trazaObjeto(self):
        a="class='tiempoDiseno' title='"+str(self.tip)+"'etiqueta='"+str(self.etiqueta)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%; border-style:"+str(bordes[self.borde])+";border-color:"+str(colores[self.colorBorde])+"; border-width: "+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg);"
        if self.oculto=="Verdadero":
             a+="display:none;"
        if self.sombra=="Verdadero":
            a+="box-shadow: 2px 2px 2px 2px #000000;"
        return a
        
    def propiedades(self):
        return {"colorFondo":str(self.colorFondo),"transparencia":str(self.transparencia),"ancho":str(self.ancho),"alto":str(self.alto),"x":str(self.x),"y":str(self.y),"borde":str(self.borde),"colorBorde":str(self.colorBorde),"anchoBorde":str(self.anchoBorde),"sombra":str(self.sombra),"rotar":str(self.rotar),"oculto":str(self.oculto),"tip":str(self.tip),"etiqueta":str(self.etiqueta)}

    def asignaPropiedades(self,prop):
        self.colorFondo=prop["colorFondo"]
        self.transparencia=prop["transparencia"]
        self.ancho=prop["ancho"]
        self.alto=prop["alto"]
        self.x=prop["x"]
        self.y=prop["y"]
        self.borde=prop["borde"]
        self.colorBorde=prop["colorBorde"]
        self.anchoBorde=prop["anchoBorde"]
        self.sombra=prop["sombra"]
        self.rotar=prop["rotar"]
        self.oculto=prop["oculto"]
        self.etiqueta=prop["etiqueta"]
        self.tip=prop["tip"]

    
class Escena(object):
    def __init__(self,x):
        self._nombre="Hoja"+str(x)
        self.colorFondo="Blanco"
        self.transparencia=1.0
        self.imagen=None
        self.ajusteImagen="Falso"
        self.escritos=""
        self.javascript=""

    def obtenerNombre(self):
        return self._nombre
    
    def trazaObjeto(self,archivo):
        if self.imagen!=None:
            if self.ajusteImagen=="Verdadero":
                a="<body style='background-repeat:no-repeat;background-size:100% 100%;background-image:url("+str(archivo)+"/recursos/imagenes/"+self.imagen+");opacity:"+str(self.transparencia)+";overflow:hidden'>"
            else:
                a="<body style='background-image:url("+str(archivo)+"/recursos/imagenes/"+self.imagen+");background-color:"+str(colores[self.colorFondo])+";overflow:hidden'>"
        else:
            a="<body style='background-color:"+str(colores[self.colorFondo])+";opacity"+str(self.transparencia)+";overflow:hidden'>"
        return a
    
    def propiedades(self):
        return {"colorFondo":str(self.colorFondo),"transparencia":str(self.transparencia),"imagen":str(self.imagen),"ajusteImagen":str(self.ajusteImagen),"escrito":str(self.escritos),"java":str(self.javascript)}
        #return "p\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.imagen)+"\\"+str(self.ajusteImagen)+"\\"+str(self.cuentaObjetos["cuadro"])+","+str(self.cuentaObjetos["circulo"])+","+str(self.cuentaObjetos["triangulo"])+","+str(self.cuentaObjetos["linea"])+","+str(self.cuentaObjetos["imagen"])+","+str(self.cuentaObjetos["texto"])+","+str(self.cuentaObjetos["sonido"])+"\n"
        
    def asignaPropiedades(self,prop):
        self.colorFondo=prop["colorFondo"]
        self.transparencia=prop["transparencia"]
        self.imagen=prop["imagen"]
        self.ajusteImagen=prop["ajusteImagen"]
        self.escritos=prop["escrito"]
        self.javascript=prop["java"]

    nombre = property(obtenerNombre)

class Cuadro(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Cuadrado"+str(x)
        self._ide=x

    def tipo(self):
        return "cuadro"

    def obtenerId(self):
        return self._ide
        
    def obtenerNombre(self):
        return self._nombre
    
    def trazaObjeto(self,archivo):
        return "<div id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"' ></div>"
    
    def propiedades(self):
        return ObjetoPrimario.propiedades(self)

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        
    nombre = property(obtenerNombre)
    ide= property(obtenerId)
    
class Circulo(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Circulos"+str(x)
        self._ide=x
        self.radio=120

    def tipo(self):
        return "circulo"
        
    def obtenerNombre(self):
        return self._nombre

    def obtenerId(self):
        return self._ide
    
    def trazaObjeto(self,archivo):
        return "<div id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"-webkit-border-radius:"+str(self.radio)+"px' ></div>"
        
    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.radio=prop["radio"]

    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["radio"]=str(self.radio)
        return p
    
    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Triangulo(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Triangulo"+str(x)
        self._ide=x

    def tipo(self):
        return "triangulo"

    def obtenerId(self):
        return self._ide
        
    def obtenerNombre(self):
        return self._nombre

    def trazaObjeto(self,archivo):
        return "<div id='"+str(self._nombre)+"' style='width:0;height:0;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-bottom:"+str(self.alto)+"pt solid "+str(colores[self.colorFondo])+"; border-left:"+str(self.ancho)+"pt solid transparent;    border-right: "+str(self.ancho)+"pt solid transparent;line-height: 0;font-size:0;-webkit-transform:rotate("+str(self.rotar)+"deg)'   ></div>"
    
    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)

    def propiedades(self):
        return ObjetoPrimario.propiedades(self)
        
    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Linea(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Linea"+str(x)
        self.alto=0
        self._ide=x

    def tipo(self):
        return "linea"

    def obtenerId(self):
        return self._ide
        
    def obtenerNombre(self):
        return self._nombre

    def trazaObjeto(self,archivo):
        return "<div id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"' ></div>"
    
    def propiedades(self):
        return ObjetoPrimario.propiedades(self)

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.alto=0

    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Imagen(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Imagen"+str(x)
        self.imagen=None
        self.clip=0
        self.rt=None
        self._ide=x

    def tipo(self):
        return "imagen"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre
    
    def trazaObjeto(self,archivo):
        self.rt=str(archivo)+"/recursos/imagenes/"
        return "<img id='"+str(self._nombre)+"' src='"+str(archivo)+"/recursos/imagenes/"+str(self.imagen)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"' />"

    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["imagen"]=str(self.imagen)
        p["clip"]=str(self.clip)
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.imagen=prop["imagen"]
        self.clip=prop["clip"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Texto(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Texto"+str(x)
        self.texto="Texto de prueba"
        self.tamanoTexto="10"
        self.colorTexto="Negro"
        self.fuente="Arial"
        self.alineacion="center"
        self.parrafo="Falso"
        self._ide=x

    def tipo(self):
        return "texto"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre

    def trazaObjeto(self,archivo):
        if self.parrafo=="Falso":
            return "<style>@font-face{font-family:'fuente';src: url('"+str(archivo)+"/recursos/archivos/"+str(self.fuente)+"')}</style><div id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"font-family:fuente;color:"+str(colores[self.colorTexto])+";font-size:"+str(self.tamanoTexto)+"pt;text-align:"+str(self.alineacion)+"' >"+str(self.texto)+"</div>"
        else:
            return "<style>@font-face{font-family:'fuente';src: url('"+str(archivo)+"/recursos/archivos/"+str(self.fuente)+"')}</style><textarea disabled id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"font-family:fuente;color:"+str(colores[self.colorTexto])+";font-size:"+str(self.tamanoTexto)+"pt;text-align:"+str(self.alineacion)+"' >"+str(self.texto)+"</textarea>"

    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["texto"]=self.texto
        p["tamanoTexto"]=self.tamanoTexto
        p["colorTexto"]=self.colorTexto
        p["fuente"]=self.fuente
        p["alineacion"]=self.alineacion
        p["parrafo"]=self.parrafo
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.texto=prop["texto"]
        self.tamanoTexto=prop["tamanoTexto"]
        self.colorTexto=prop["colorTexto"]
        self.fuente=prop["fuente"]
        self.alineacion=prop["alineacion"]
        self.parrafo=prop["parrafo"]


    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Boton(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Boton"+str(x)
        self.texto="Boton"+str(x)
        self.alto=5
        self.sombra="Verdadero"
        self._ide=x

    def tipo(self):
        return "boton"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre
    
    def trazaObjeto(self,archivo):
        return "<button id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"' >"+str(self.texto)+"</button>"
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["texto"]=self.texto
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.texto=prop["texto"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)


class Entrada(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Entrada"+str(x)
        self.texto="Entrada de Texto"
        self.alto=3
        self.ancho=15
        self._ide=x

    def tipo(self):
        return "entrada"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre
        
    def trazaObjeto(self,archivo):
        return "<input id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"' type='text' value='"+str(self.texto)+"'  />"
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["texto"]=self.texto
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.texto=prop["texto"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Lista(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Lista"+str(x)
        self.lista=""
        self.alto=3
        self.ancho=15
        self._ide=x

    def tipo(self):
        return "lista"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre
    def trazaObjeto(self,archivo):
        a="<select id='"+str(self._nombre)+"'"+str(ObjetoPrimario.trazaObjeto(self))+" '   >"
        op=self.lista.split(",")
        for i in range(len(op)):
            a=a+str("<option value='"+str(op[i])+"'>"+str(op[i])+"</option>")
        a=a+str("</select>")
        return a
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["lista"]=self.lista
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.lista=prop["lista"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)


class Check(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Check"+str(x)
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=3
        self.ancho=15
        self.valor="0"
        self._ide=x

    def tipo(self):
        return "check"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre

    def trazaObjeto(self,archivo):
        return "<input id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"' type='checkbox' value='"+str(self.valor)+"'  />"
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["valor"]=self.valor
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.valor=prop["valor"]
    nombre = property(obtenerNombre)
    ide= property(obtenerId)
    
class Area(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Area"+str(x)
        self.texto="Entrada de Texto"
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=20
        self.ancho=15
        self._ide=x

    def tipo(self):
        return "area"

    def obtenerId(self):
        return self._ide

    def obtenerNombre(self):
        return self._nombre
    
    def trazaObjeto(self,archivo):
     return "<textarea id='"+str(self._nombre)+"'"+str(ObjetoPrimario.trazaObjeto(self))+"'  >"+str(self.texto)+"</textarea>"
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["texto"]=self.texto
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.texto=prop["texto"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)


class Proyecto(object):
    def __init__(self,nom,rut):
        self._ruta=rut
        self._nombre=nom
        self.ancho=640
        self.alto=480
        self.maximizado="Falso"
        self.paginas=[]
    def ejecutar(self):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Vista Previa de "+str(self.nombre))
        self.window.set_size_request(int(self.ancho), int(self.alto))
        if self.maximizado=="Verdadero":
            self.window.maximize()
        self.window.set_resizable(False)
        self.window.set_modal(True)
        color = gtk.gdk.color_parse('#ffffff')
        self.window.modify_bg(gtk.STATE_NORMAL, color)
        self.window.connect("destroy",self.destroy)
        self.lienzo= webkit.WebView()
        self.lienzo.set_view_source_mode(False)
        self.lienzo.load_html_string(self.paginas[0],"file://"+self.ruta+"/")
        self.lienzo.connect('title-changed',self.cambiaTitulo)
        self.window.add(self.lienzo)
        self.window.show_all()
    
    def cambiaTitulo(self,widget,web,titulo):
        self.lienzo.load_html_string(self.paginas[int(titulo)],"file://"+self.ruta+"/")
       
       
    
    def obtenerNombre(self):
        return self._nombre    
    def obtenerRuta(self):
        return self._ruta    
    
    def destroy(self, widget):
        pass
    
    nombre = property(obtenerNombre)
    ruta=property(obtenerRuta)

class Sonido(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Sonido"+str(x)
        self.sonido=None
        self._ide=x

    def tipo(self):
        return "sonido"

    def obtenerId(self):
        return self._ide  

    def obtenerNombre(self):
        return self._nombre
    
    def trazaObjeto(self,archivo):
       return "<audio id='"+str(self._nombre)+"' "+str(ObjetoPrimario.trazaObjeto(self))+"><source src='"+str(archivo)+"/recursos/sonidos/"+str(self.sonido)+"' type='audio/ogg'   preload><source src='"+str(archivo)+"/recursos/sonidos/"+str(self.sonido)+"' type='audio/mpeg'   preload><source src='"+str(archivo)+"/recursos/sonidos/"+str(self.sonido)+"' type='audio/wav'   preload></audio>"
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["sonido"]=str(self.sonido)
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.sonido=prop["sonido"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)

class Video(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Video"+str(x)
        self.video=None
        self.ancho=25
        self.alto=25
        self._ide=x

    def tipo(self):
        return "video"

    def obtenerId(self):
        return self._ide  

    def obtenerNombre(self):
        return self._nombre

    def trazaObjeto(self,archivo):
       return "<video id='"+str(self._nombre)+"' class='tiempoDiseno' style='position:absolute;background-color:black;top:"+str(self.y)+"%;left:"+str(self.x)+"%' width='"+str(self.ancho)+"%' height='"+str(self.alto)+"%'><source src='"+str(archivo)+"/recursos/videos/"+str(self.video)+"' type='video/ogg'   preload><source src='"+str(archivo)+"/recursos/videos/"+str(self.video)+"' type='audio/mp4'   preload><source src='"+str(archivo)+"/recursos/videos/"+str(self.video)+"' type='video/webm'   preload></video>"
    
    def propiedades(self):
        p=ObjetoPrimario.propiedades(self)
        p["video"]=str(self.video)
        return p

    def asignaPropiedades(self,prop):
        ObjetoPrimario.asignaPropiedades(self,prop)
        self.video=prop["video"]

    nombre = property(obtenerNombre)
    ide= property(obtenerId)
