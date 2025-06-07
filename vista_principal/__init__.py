"""Paquete con las vistas principales de la interfaz"""

from .entrenar_vista import seleccion
from .vista_centro_accion import VistaCentroAccion
from .vista_herramientas import VistaHerramientas
from .vista_importar_exportar import VistaImportarExportar

__all__ = [
    "seleccion",
    "VistaCentroAccion",
    "VistaHerramientas",
    "VistaImportarExportar",
]
