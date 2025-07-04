# vista_herramientas.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QGridLayout,
                             QMessageBox, QMenu, QFileDialog, QDialog,
                             QTextEdit, QInputDialog, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QColor
import os
import zipfile
import json
import datetime
import shutil
from models.cv_classifier import CVClassifier
from models.deep_learning_classifier import DeepLearningClassifier
from notificacion.notification_manager import (show_success, show_error,
                                                  show_info, show_question)


class ModelInfoDialog(QDialog):
    """Ventana personalizada para mostrar información detallada del modelo"""

    def __init__(self, model_data, parent=None):
        super().__init__(parent)
        self.model_data = model_data
        self.setWindowTitle("Información del Modelo")
        self.setObjectName("ModelInfoDialog")
        self.setFixedSize(500, 600)
        self.setModal(True)

        # Obtener colores del tema principal si está disponible
        main_window = self.window()
        if hasattr(main_window, 'color_accent_red'):
            self.accent_red = main_window.color_accent_red
            self.accent_blue = main_window.color_accent_blue
            self.text_light = main_window.color_text_light
            self.text_medium = main_window.color_text_medium
            self.groupbox_border = main_window.color_groupbox_border
            self.dialog_bg_start = main_window.color_dialog_bg_start
            self.dialog_bg_end = main_window.color_dialog_bg_end
        else:
            # Colores por defecto si no hay ventana principal
            self.accent_red = "#E74C3C"
            self.accent_blue = "#3498DB"
            self.text_light = "#E0E0E0"
            self.text_medium = "#BDC3C7"
            self.groupbox_border = "#4A5568"
            self.dialog_bg_start = "#2C3E50"
            self.dialog_bg_end = "#34495E"

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de la ventana"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header con icono y nombre
        header_frame = QFrame()
        header_frame.setObjectName("InfoCard")
        header_layout = QHBoxLayout(header_frame)

        # Icono grande
        is_dl = self.model_data.get('is_deep_learning', False)
        icon_text = "🧠" if is_dl else "🤖"
        icon_color = self.accent_red if is_dl else self.accent_blue

        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"font-size: 48px; color: {icon_color}; padding: 10px;")

        # Información principal
        info_layout = QVBoxLayout()

        name_label = QLabel(self.model_data.get('display_name', 'Modelo Sin Nombre'))
        name_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {self.text_light};")

        type_label = QLabel(f"Tipo: {self.model_data.get('model_type', 'Desconocido')}")
        type_label.setStyleSheet(f"font-size: 14px; color: {self.text_medium};")

        info_layout.addWidget(name_label)
        info_layout.addWidget(type_label)
        info_layout.addStretch()

        header_layout.addWidget(icon_label)
        header_layout.addLayout(info_layout)
        layout.addWidget(header_frame)

        # Detalles del modelo
        details_frame = QFrame()
        details_frame.setObjectName("InfoCard")
        details_layout = QVBoxLayout(details_frame)

        details_title = QLabel("📊 Detalles del Modelo")
        details_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {self.text_light}; margin-bottom: 10px;")
        details_layout.addWidget(details_title)

        # Información detallada
        details_info = [
            ("📅 Fecha de creación", self.model_data.get('creation_date', 'Desconocida')),
            ("🎯 Profesiones", str(self.model_data.get('num_professions', 0))),
            ("📁 Formato", self.model_data.get('model_format', 'Desconocido')),
            ("🔧 Características", str(self.model_data.get('num_features', 'N/A')))
        ]

        for label, value in details_info:
            detail_layout = QHBoxLayout()
            detail_label = QLabel(label)
            detail_label.setStyleSheet(f"font-weight: bold; color: {self.text_light};")
            detail_value = QLabel(str(value))
            detail_value.setStyleSheet(f"color: {self.text_medium};")

            detail_layout.addWidget(detail_label)
            detail_layout.addStretch()
            detail_layout.addWidget(detail_value)
            details_layout.addLayout(detail_layout)

        layout.addWidget(details_frame)

        # Profesiones disponibles
        if 'professions' in self.model_data and self.model_data['professions']:
            professions_frame = QFrame()
            professions_frame.setObjectName("InfoCard")
            professions_layout = QVBoxLayout(professions_frame)

            prof_title = QLabel("👥 Profesiones Disponibles")
            prof_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {self.text_light}; margin-bottom: 10px;")
            professions_layout.addWidget(prof_title)

            # Mostrar profesiones en texto scrolleable
            prof_text = QTextEdit()
            prof_text.setMaximumHeight(120)
            prof_text.setReadOnly(True)
            prof_text.setStyleSheet(f"""
                QTextEdit {{
                    background-color: transparent;
                    color: {self.text_medium};
                    border: 1px solid {self.groupbox_border};
                    border-radius: 5px;
                }}
            """)
            
            professions_text = "\n".join([f"• {prof}" for prof in self.model_data['professions']])
            prof_text.setPlainText(professions_text)

            professions_layout.addWidget(prof_text)
            layout.addWidget(professions_frame)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.text_medium};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {self.text_light};
            }}
        """)

        load_btn = QPushButton("Cargar Modelo")
        load_btn.clicked.connect(self.load_model)
        load_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_blue};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {QColor(self.accent_blue).lighter(115).name()};
            }}
        """)

        export_btn = QPushButton("Exportar")
        export_btn.clicked.connect(self.export_model)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_red};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {QColor(self.accent_red).lighter(115).name()};
            }}
        """)

        buttons_layout.addWidget(close_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(load_btn)
        buttons_layout.addWidget(export_btn)

        layout.addLayout(buttons_layout)

        # Aplicar estilo al diálogo
        self.setStyleSheet(f"""
            QDialog#ModelInfoDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.dialog_bg_start},
                    stop:1 {self.dialog_bg_end}
                );
                border-radius: 10px;
            }}
            QFrame#InfoCard {{
                background-color: {QColor(self.dialog_bg_end).lighter(105).name() if QColor(self.dialog_bg_end).lightnessF() < 0.5 else QColor(self.dialog_bg_end).darker(105).name()};
                border: 1px solid {self.groupbox_border};
                border-radius: 8px;
                padding: 15px;
            }}
        """)

    def load_model(self):
        """Carga el modelo desde la ventana de información"""
        self.accept()
        # Emitir señal para que la vista principal maneje la carga
        if hasattr(self.parent(), 'load_model'):
            self.parent().load_model(self.model_data)

    def export_model(self):
        """Exporta el modelo desde la ventana de información"""
        self.accept()
        # Emitir señal para que la vista principal maneje la exportación
        if hasattr(self.parent(), 'export_model'):
            self.parent().export_model(self.model_data)


class ModelCard(QFrame):
    """Tarjeta de modelo con diseño unificado"""
    model_selected = pyqtSignal(dict)

    def __init__(self, model_data, parent=None):
        super().__init__(parent)
        self.model_data = model_data
        self.setObjectName("TrainingOptionCard")  # Usar el mismo objectName que TrainingOptionCard
        self.setFixedSize(280, 200)  # Mantener el tamaño original
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Obtener colores del tema principal si está disponible
        main_window = self.window()
        if hasattr(main_window, 'color_accent_red'):
            self.accent_red = main_window.color_accent_red
            self.accent_blue = main_window.color_accent_blue
            self.text_light = main_window.color_text_light
            self.text_medium = main_window.color_text_medium
        else:
            self.accent_red = "#E74C3C"
            self.accent_blue = "#3498DB"
            self.text_light = "#E0E0E0"
            self.text_medium = "#BDC3C7"

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de la tarjeta"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Mantener márgenes originales
        layout.setSpacing(15)  # Mantener espaciado original

        # Contenedor de icono para centrarlo bien
        icon_container = QFrame()
        icon_container.setFixedHeight(80)  # Mantener altura original
        icon_container.setStyleSheet("background-color: transparent; border: none;")
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        # Determinar icono según tipo de modelo
        is_dl = self.model_data.get('is_deep_learning', False)
        icon_text = "🧠" if is_dl else "🤖"
        icon_color = self.accent_red if is_dl else self.accent_blue
        
        self.icon_label = QLabel(icon_text)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet(f"font-size: 48px; color: {icon_color};")  # Mantener tamaño original

        icon_layout.addWidget(self.icon_label)
        layout.addWidget(icon_container)

        # Nombre del modelo
        self.name_label = QLabel(self.model_data.get('display_name', 'Modelo Sin Nombre'))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {self.text_light};")
        layout.addWidget(self.name_label)

        # Información adicional
        info_text = f"{self.model_data.get('model_type', 'Desconocido')}"
        if 'num_professions' in self.model_data:
            info_text += f" • {self.model_data['num_professions']} profesiones"

        self.info_label = QLabel(info_text)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet(f"font-size: 11px; color: {self.text_medium};")
        layout.addWidget(self.info_label)

        layout.addStretch()

    def mousePressEvent(self, event):
        """Maneja el clic en la tarjeta"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.model_selected.emit(self.model_data)
        super().mousePressEvent(event)


class VistaHerramientas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("VistaHerramientas")

        # Inicializar clasificadores para obtener modelos reales
        self.ml_classifier = CVClassifier()
        self.dl_classifier = DeepLearningClassifier()

        self.setup_ui()
        self.load_models()

        # Aceptar drops para importación de modelos
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """Maneja el inicio del drag de archivos"""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                valid_extensions = ['.zip', '.senati', '.mlmodel', '.aimodel', '.ctpro']
                if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        """Permite el movimiento del drag sobre el widget"""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                valid_extensions = ['.zip', '.senati', '.mlmodel', '.aimodel', '.ctpro']
                if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        """Maneja el drop de archivos"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            valid_extensions = ['.zip', '.senati', '.mlmodel', '.aimodel', '.ctpro']
            if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                self.import_model(file_path)
                event.acceptProposedAction()

    def decrypt_data(self, data):
        """Desencripta los datos usando un método simple (para demostración)"""
        from itertools import cycle
        key = b'ClasificaTalentoPRO'  # Debe ser la misma clave que en ExportWorker
        return bytes(a ^ b for a, b in zip(data, cycle(key)))

    def import_model(self, file_path=None):
        """Importa un modelo desde archivo"""
        if not file_path:
            formats = "Archivos de Modelo (*.zip *.senati *.mlmodel *.aimodel *.ctpro);;Todos los archivos (*)"
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Importar Modelo", 
                "", 
                formats
            )

        if not file_path:
            return

        try:
            if not zipfile.is_zipfile(file_path):
                show_error("Error de Formato", "El archivo no es un formato de modelo válido", parent=self)
                return

            with zipfile.ZipFile(file_path, 'r') as zipf:
                # Verificar metadatos
                metadata_file = 'package_info.json' if 'package_info.json' in zipf.namelist() else 'senati_info.json'
                if metadata_file not in zipf.namelist():
                    show_error("Error de Formato", "El archivo no contiene metadatos válidos", parent=self)
                    return

                # Leer información del modelo
                package_info = json.loads(zipf.read(metadata_file).decode('utf-8'))
                model_type = package_info.get('model_type', 'unknown')
                original_name = package_info.get('model_name', 'imported_model')
                format_version = package_info.get('format_version', '1.0')
                
                # Obtener información de protección si existe
                protection_info = package_info.get('protection', {
                    'enabled': False,
                    'level': 'none',
                    'format': '.zip'
                })

                new_name, ok = QInputDialog.getText(
                    self, 
                    "Nombre del Modelo", 
                    f"Nombre para el modelo importado:\n(Original: {original_name})", 
                    text=original_name
                )
                if not ok or not new_name.strip():
                    return

                final_model_name = new_name.strip()
                target_dir = os.path.join('saved_deep_models' if model_type == 'dl' else 'saved_models', final_model_name)
                
                if model_type not in ['ml', 'dl']:
                    show_error("Error de Tipo", f"Tipo de modelo desconocido: {model_type}", parent=self)
                    return

                if os.path.exists(target_dir):
                    reply = QMessageBox.question(
                        self, 
                        "Modelo Existente", 
                        f"Ya existe un modelo con el nombre '{final_model_name}'.\n¿Deseas sobrescribirlo?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.No:
                        return
                    shutil.rmtree(target_dir)

                os.makedirs(target_dir, exist_ok=True)

                # Procesar cada archivo
                for file_info in zipf.filelist:
                    if file_info.filename not in ['package_info.json', 'senati_info.json']:
                        # Leer el contenido del archivo
                        file_data = zipf.read(file_info.filename)
                        
                        # Desencriptar si es necesario
                        if protection_info['enabled']:
                            try:
                                file_data = self.decrypt_data(file_data)
                            except Exception as e:
                                show_error("Error de Desencriptación", f"Error al desencriptar {file_info.filename}: {str(e)}", parent=self)
                                return

                        # Escribir el archivo
                        target_path = os.path.join(target_dir, file_info.filename)
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with open(target_path, 'wb') as f:
                            f.write(file_data)

                show_success(
                    "Modelo Importado", 
                    f"El modelo '{final_model_name}' se ha importado correctamente.\nTipo: {model_type.upper()}, Versión: {format_version}", 
                    parent=self
                )
                self.load_models()

        except Exception as e:
            show_error("Error de Importación", f"Error importando modelo: {str(e)}", parent=self)

    def setup_ui(self):
        """Configura la interfaz principal"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(20)

        # Header con título y botones de acción
        header_layout = QHBoxLayout()

        title_label = QLabel("🤖 Gestión de Modelos de IA")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        import_btn = QPushButton("📥 Importar Modelo")
        import_btn.setFixedSize(140, 35)
        import_btn.clicked.connect(self.import_model)

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedSize(120, 35)
        refresh_btn.clicked.connect(self.load_models)

        buttons_layout.addWidget(import_btn)
        buttons_layout.addWidget(refresh_btn)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addLayout(buttons_layout)
        main_layout.addLayout(header_layout)

        # Área de scroll para las tarjetas de modelos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Widget contenedor para las tarjetas
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setContentsMargins(10, 10, 10, 10)

        # Mensaje cuando no hay modelos
        self.no_models_label = QLabel("📭 No hay modelos disponibles")
        self.no_models_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_models_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 50px; border: 2px dashed; border-radius: 15px;")
        self.no_models_label.hide()

        scroll_area.setWidget(self.cards_container)
        main_layout.addWidget(scroll_area)

        # Agregar el label de "no hay modelos" al layout principal para que sea visible
        main_layout.addWidget(self.no_models_label)

    def load_models(self):
        """Carga los modelos disponibles y crea las tarjetas"""
        try:
            # Limpiar tarjetas existentes
            self.clear_cards()

            # Obtener modelos disponibles
            models = self.ml_classifier.list_available_models()

            if not models:
                self.show_no_models_message()
                return

            self.hide_no_models_message()

            # Crear tarjetas para cada modelo
            row, col, max_cols = 0, 0, 3
            for model_data in models:
                card = ModelCard(model_data)
                card.model_selected.connect(self.on_model_selected)
                self.cards_layout.addWidget(card, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            # Agregar stretch para empujar las tarjetas hacia arriba
            self.cards_layout.setRowStretch(row + 1, 1)

        except Exception as e:
            self.show_error_message(f"Error cargando modelos: {str(e)}")

    def clear_cards(self):
        """Limpia todas las tarjetas del layout"""
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_no_models_message(self):
        """Muestra el mensaje de no hay modelos"""
        self.cards_container.hide()
        self.no_models_label.show()

    def hide_no_models_message(self):
        """Oculta el mensaje de no hay modelos"""
        self.no_models_label.hide()
        self.cards_container.show()

    def show_error_message(self, message):
        """Muestra un mensaje de error"""
        self.no_models_label.setText(f"❌ {message}")
        self.show_no_models_message()

    def on_model_selected(self, model_data):
        """Maneja la selección de un modelo"""
        menu = QMenu(self)
        info_action = menu.addAction("ℹ️ Ver Información")
        menu.addSeparator()
        load_action = menu.addAction("📂 Cargar Modelo")
        test_action = menu.addAction("🧪 Probar Modelo")
        menu.addSeparator()
        export_action = menu.addAction("📤 Exportar")
        delete_action = menu.addAction("🗑️ Eliminar")
        
        action = menu.exec(QCursor.pos())

        if action == info_action:
            self.show_model_info(model_data)
        elif action == load_action:
            self.load_model(model_data)
        elif action == test_action:
            self.test_model(model_data)
        elif action == export_action:
            self.export_model(model_data)
        elif action == delete_action:
            self.delete_model(model_data)

    def show_model_info(self, model_data):
        """Muestra información detallada del modelo en ventana personalizada"""
        dialog = ModelInfoDialog(model_data, self)
        dialog.exec()

    def load_model(self, model_data):
        """Carga el modelo seleccionado"""
        model_name = model_data.get('name', '')
        display_name = model_data.get('display_name', model_name)
        is_dl = model_data.get('is_deep_learning', False)

        try:
            classifier = self.dl_classifier if is_dl else self.ml_classifier
            success = classifier.load_model(model_name)

            if success:
                show_success("Modelo Cargado", f"El modelo '{display_name}' se ha cargado correctamente.", parent=self)
            else:
                show_error("Error al Cargar", f"No se pudo cargar el modelo '{display_name}'.", parent=self)
        except Exception as e:
            show_error("Error al Cargar", f"Error cargando '{display_name}': {str(e)}", parent=self)

    def test_model(self, _):
        """Prueba el modelo con datos de ejemplo"""
        show_info(
            "Función en Desarrollo",
            "La función de prueba de modelos estará disponible próximamente.",
            duration=4000,
            parent=self
        )

    def export_model(self, model_data):
        """Exporta el modelo seleccionado en formato .senati"""
        model_name = model_data.get('name', '')
        display_name = model_data.get('display_name', model_name)

        if not model_name:
            return

        suggested_filename = f"{model_name}.senati"
        file_path, _ = QFileDialog.getSaveFileName(
            self, f"Exportar {display_name}", suggested_filename,
            "Archivos SENATI (*.senati)"
        )

        if file_path:
            if not file_path.lower().endswith('.senati'):
                file_path += '.senati'
            try:
                is_dl = model_data.get('is_deep_learning', False)
                source_dir = os.path.join('saved_deep_models' if is_dl else 'saved_models', model_name)

                if not os.path.exists(source_dir):
                    QMessageBox.critical(self, "Error", f"No se encontró el directorio del modelo: {source_dir}")
                    return

                with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    senati_info = {
                        'format_version': '1.0', 'model_type': 'dl' if is_dl else 'ml',
                        'model_name': model_name, 'exported_by': 'ClasificaTalento PRO',
                        'export_date': datetime.datetime.now().isoformat()
                    }
                    zipf.writestr('senati_info.json', json.dumps(senati_info, indent=2))
                    for root, _, files in os.walk(source_dir):
                        for file in files:
                            full_path = os.path.join(root, file)
                            arcname = os.path.relpath(full_path, source_dir)
                            zipf.write(full_path, arcname)

                show_success("Modelo Exportado", f"'{display_name}' se ha exportado correctamente.", parent=self)
            except Exception as e:
                show_error("Error de Exportación", f"No se pudo exportar '{display_name}': {str(e)}", parent=self)

    def delete_model(self, model_data):
        """Elimina el modelo seleccionado"""
        model_name = model_data.get('name', '')
        display_name = model_data.get('display_name', model_name)

        if not model_name:
            show_error("Error", "No se pudo obtener el nombre del modelo", parent=self)
            return

        notification = show_question(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar '{display_name}'? Esta acción no se puede deshacer.",
            actions=[("Eliminar", "confirm_delete"), ("Cancelar", "cancel_delete")],
            parent=self
        )
        notification.action_clicked.connect(lambda action_id: self.handle_delete_confirmation(action_id, model_data))

    def handle_delete_confirmation(self, action_id, model_data):
        """Maneja la confirmación de eliminación"""
        if action_id == "confirm_delete":
            self.perform_model_deletion(model_data)

    def perform_model_deletion(self, model_data):
        """Realiza la eliminación del modelo"""
        model_name = model_data.get('name', '')
        display_name = model_data.get('display_name', model_name)
        is_dl = model_data.get('is_deep_learning', False)

        try:
            model_dir = os.path.join('saved_deep_models' if is_dl else 'saved_models', model_name)

            if not os.path.exists(model_dir):
                show_error("Error al Eliminar", f"No se encontró el directorio del modelo: {model_dir}", parent=self)
                return
            
            shutil.rmtree(model_dir)
            show_success("Modelo Eliminado", f"El modelo '{display_name}' ha sido eliminado correctamente.", parent=self)
            self.load_models()

        except Exception as e:
            show_error("Error al Eliminar", f"Error eliminando '{display_name}': {str(e)}", parent=self)