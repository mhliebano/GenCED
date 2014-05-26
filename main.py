#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acciones import *
from ventana import *

if __name__ == "__main__":
    miventana = Ventana()
    misacciones=Acciones(miventana)
    miventana.hojaBienvenida()
    miventana.main()

