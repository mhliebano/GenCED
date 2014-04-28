# -*- coding: utf-8 -*-
import gtk
import webkit
colores={"defecto":"default","Negro":"#000000","Gris Oscuro":"#696969","Gris":"#808080","Gris Claro":"#A9A9A9","Blanco":"#FFFFFF","Rojo Oscuro":"#8B0000","Rojo":"#FF0000","Rojo Claro":"#FA8072","Rosado Oscuro":"#FF1493","Rosado":"#FF69B4","Rosado Claro":"#FFB6C1","Fucsia Oscuro":"#8A2BE2","Fucsia":"#FF00FF","Fucsia Claro":"#CD5C5C","Marron Oscuro":"#800000","Marron":"#8B4513","Marron Claro":"#A0522D","Naranja Oscuro":"#FF8C00","Naranja":"#FF4500","Naranja Claro":"#FF6347","Purpura Oscuro":"#4B0082","Purupura":"#800080","Purpura Claro":"#EE82EE","Amarillo Oscuro":"#FFD700","Amarillo":"#FFFF00","Amarillo Claro":"#F0E68C","Teal":"#008080","Azul Oscuro":"#000080","Azul":"#0000FF","Azul Claro":"#00BFFF","AguaMarina Oscuro":"#1E90FF","AguaMarina":"#00FFFF","AguaMarina Claro":"#00BFFF","Verde Oscuro":"#006400","Verde":"#008000","Verde Claro":"#3CB371","Lima":"#00FF00","Oliva Oscuro":"#556B2F","Oliva":"#808000","Oliva Claro":"#BDB76B"}
bordes={"punteado":"dotted","discontinuo":"dashed","solido":"solid","doble":"double","acanalado":"groove","corrugado":"ridge","relieve bajo":"inset","relieve alto":"outset"}

class ObjetoPrimario(object):
    def __init__(self):
        self.colorFondo="Negro"
        self.transparencia=1.0
        self.ancho=10
        self.alto=10
        self.x=1
        self.y=1
        self.borde="solido"
        self.colorBorde="Rojo"
        self.anchoBorde=1
        self.sombra=False
        self.rotar=0
        self.oculto="Falso"

class Escena(object):
    def __init__(self,x):
        self._nombre="Hoja"+str(x)
        self.colorFondo="Blanco"
        self.transparencia=1.0
        self.imagen=None
        self.ajusteImagen="Falso"
        self.cuentaObjetos={"cuadro":0,"circulo":0,"triangulo":0,"linea":0,"imagen":0,"texto":0,"boton":0,"entrada":0,"lista":0,"check":0,"area":0}
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        if self.imagen!=None:
            if self.ajusteImagen=="Verdadero":
                a="<body style='background-repeat:no-repeat;background-size:100% 100%;background-image:url("+str(archivo)+"/recursos/imagenes/"+self.imagen+");opacity:"+str(self.transparencia)+";overflow:hidden'>"
            else:
                a="<body style='background-image:url("+str(archivo)+"/recursos/imagenes/"+self.imagen+");background-color:"+str(colores[self.colorFondo])+";overflow:hidden'>"
        else:
            a="<body style='background-color:"+str(colores[self.colorFondo])+";opacity"+str(self.transparencia)+";overflow:hidden'>"
        return a
    
    def retornaPropiedades(self):
        return "p\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.imagen)+"\\"+str(self.ajusteImagen)+"\\"+str(self.cuentaObjetos["cuadro"])+","+str(self.cuentaObjetos["circulo"])+","+str(self.cuentaObjetos["triangulo"])+","+str(self.cuentaObjetos["linea"])+","+str(self.cuentaObjetos["imagen"])+","+str(self.cuentaObjetos["texto"])+"\n"
        
    
    nombre = property(obtenerNombre)

class Cuadro(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Cuadrado"+str(x)
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<div id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border:"+str(bordes[self.borde])+" "+str(colores[self.colorBorde])+" "+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'></div>"
        return a
    
    def retornaPropiedades(self):
        return "c\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\n"
    
    nombre = property(obtenerNombre)

class Circulo(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Circulos"+str(x)
        self.radio=120
    
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<div id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border:"+str(bordes[self.borde])+" "+str(colores[self.colorBorde])+" "+str(self.anchoBorde) +"pt;-webkit-border-radius:"+str(self.radio)+"px' onclick='send(this.id)'></div>"
        return a
    
    def retornaPropiedades(self):
        return "o\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.radio)+"\n"
    
    nombre = property(obtenerNombre)

class Triangulo(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Triangulo"+str(x)
    
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<div id='"+str(self._nombre)+"' style='width:0;height:0;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-bottom:"+str(self.alto)+"pt solid "+str(colores[self.colorFondo])+"; border-left:"+str(self.ancho)+"pt solid transparent;    border-right: "+str(self.ancho)+"pt solid transparent;line-height: 0;font-size:0;-webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'></div>"
        return a
    
    def retornaPropiedades(self):
        return "t\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.oculto)+"\\"+str(self.rotar)+"\n"
    
    nombre = property(obtenerNombre)

class Linea(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Linea"+str(x)

    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<div id='"+str(self._nombre)+"' style='width:"+str(self.ancho)+"%;height:0%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-top:"+str(bordes[self.borde])+" "+str(self.anchoBorde)+"px "+str(colores[self.colorBorde])+"; -webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'></div>"
        return a
    
    def retornaPropiedades(self):
        return "l\\"+str(self.ancho)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\n"
    
    nombre = property(obtenerNombre)


class Imagen(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Imagen"+str(x)
        self.imagen=None
        self.clip=0
        
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        if self.clip==0:
            a="<img id='"+str(self._nombre)+"' src='"+str(archivo)+"/recursos/imagenes/"+str(self.imagen)+"' width='"+str(self.ancho)+"%' height='"+str(self.alto)+"%' style='position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border:"+str(bordes[self.borde])+" "+str(colores[self.colorBorde])+" "+str(self.anchoBorde)+"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'/></div>"
        else:
            a="<img id='"+str(self._nombre)+"' src='"+str(archivo)+"/recursos/imagenes/"+str(self.imagen)+"' width='"+str(self.ancho)+"%' height='"+str(self.alto)+"%' style='position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border:"+str(bordes[self.borde])+" "+str(colores[self.colorBorde])+" "+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg);clip("+str(self.clip)+")' onclick='send(this.id)'></div>"
        return a
    
    def retornaPropiedades(self):
        return "i\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.imagen)+"\\"+str(self.clip)+"\n"
    
    nombre = property(obtenerNombre)

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
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        if self.parrafo=="Falso":
            a="<style>@font-face{font-family:'fuente';src: url('"+str(archivo)+"/recursos/archivos/"+str(self.fuente)+"')}</style><div id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border:"+str(bordes[self.borde])+" "+str(colores[self.colorBorde])+" "+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg);font-family:fuente;color:"+str(colores[self.colorTexto])+";font-size:"+str(self.tamanoTexto)+"%;text-align:"+str(self.alineacion)+"' onclick='send(this.id)'>"+str(self.texto)+"</div>"
        else:
            a="<style>@font-face{font-family:'fuente';src: url('"+str(archivo)+"/recursos/archivos/"+str(self.fuente)+"')}</style><div id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border:"+str(bordes[self.borde])+" "+str(colores[self.colorBorde])+" "+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg);font-family:fuente;color:"+str(colores[self.colorTexto])+";font-size:"+str(self.tamanoTexto)+"%;text-align:"+str(self.alineacion)+";overflow-y:visible;overflow-x:hidden;' onclick='send(this.id)'>"+str(self.texto)+"</div>"
        return a
    
    def retornaPropiedades(self):
        return "x\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.texto)+"\\"+str(self.tamanoTexto)+"\\"+str(self.colorTexto)+"\\"+str(self.fuente)+"\\"+str(self.alineacion)+"\\"+str(self.parrafo)+"\n"
    
    nombre = property(obtenerNombre)

class Boton(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Boton"+str(x)
        self.texto="Boton"
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=5
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<button id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-color:"+str(colores[self.colorBorde])+"; border-width:"+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'>"+str(self.texto)+"</button>"
        return a
    
    def retornaPropiedades(self):
        return "b\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.texto)+"\n"
    
    nombre = property(obtenerNombre)

class Entrada(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Entrada"+str(x)
        self.texto="Entrada de Texto"
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=3
        self.ancho=15
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<input id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-color:"+str(colores[self.colorBorde])+"; border-width:"+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' type='text' value='"+str(self.texto)+"' onclick='send(this.id)'/>"
        return a
    
    def retornaPropiedades(self):
        return "e\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.texto)+"\n"
    
    nombre = property(obtenerNombre)

class Lista(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Lista"+str(x)
        self.lista=""
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=3
        self.ancho=15
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<select id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-color:"+str(colores[self.colorBorde])+"; border-width:"+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'>"
        op=self.lista.split(",")
        for i in range(len(op)):
            a=a+str("<option value='"+str(op[i])+"'>"+str(op[i])+"</option>")
        a=a+str("</select>")
        return a
    
    def retornaPropiedades(self):
        return "s\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.lista)+"\n"
    
    nombre = property(obtenerNombre)

class Check(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Check"+str(x)
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=3
        self.ancho=15
        self.valor="0"
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<input id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-color:"+str(colores[self.colorBorde])+"; border-width:"+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' type='checkbox' value='"+str(self.valor)+"' onclick='send(this.id)'/>"
        return a
    
    def retornaPropiedades(self):
        return "k\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.valor)+"\n"
    
    nombre = property(obtenerNombre)

class Area(ObjetoPrimario):
    def __init__(self,x):
        ObjetoPrimario.__init__(self)
        self._nombre="Area"+str(x)
        self.texto="Entrada de Texto"
        self.colorFondo="defecto"
        self.colorBorde="defecto"
        self.alto=20
        self.ancho=15
    def obtenerNombre(self):
        return self._nombre
    
    def actualizaCadena(self,archivo):
        a="<textarea id='"+str(self._nombre)+"' style='background-color:"+str(colores[self.colorFondo])+";width:"+str(self.ancho)+"%;height:"+str(self.alto)+"%;position:absolute;top:"+str(self.y)+"%;left:"+str(self.x)+"%;border-color:"+str(colores[self.colorBorde])+"; border-width:"+str(self.anchoBorde) +"pt;-webkit-transform:rotate("+str(self.rotar)+"deg)' onclick='send(this.id)'>"+str(self.texto)+"</textarea>"
        return a
    
    def retornaPropiedades(self):
        return "r\\"+str(self.colorFondo)+"\\"+str(self.transparencia)+"\\"+str(self.ancho)+"\\"+str(self.alto)+"\\"+str(self.x)+"\\"+str(self.y)+"\\"+str(self.borde)+"\\"+str(self.colorBorde)+"\\"+str(self.anchoBorde)+"\\"+str(self.sombra)+"\\"+str(self.rotar)+"\\"+str(self.oculto)+"\\"+str(self.texto)+"\n"
    
    nombre = property(obtenerNombre)

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
        self.window.set_title(titulo)
        if titulo=="Circulos0":
            self.lienzo.load_html_string(self.paginas[1],"file://"+self.ruta+"/")
    
    def obtenerNombre(self):
        return self._nombre    
    def obtenerRuta(self):
        return self._ruta    
    
    def destroy(self, widget):
        pass
    
    nombre = property(obtenerNombre)
    ruta=property(obtenerRuta)

class Sonido(object):
    def __init__(self):
        pass
