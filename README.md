<div align="center">

# 🎯 ClasificaTalento PRO
### Sistema Inteligente de Clasificación de CVs

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8+-orange.svg)](https://tensorflow.org)
[![Flask](https://img.shields.io/badge/Flask-API-red.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Una aplicación de escritorio robusta y moderna para la clasificación automática de currículums mediante Machine Learning y Deep Learning*

[🚀 Características](#-características-principales) • [📋 Instalación](#-instalación) • [💻 Uso](#-uso) • [🔧 Tecnologías](#-tecnologías) • [📖 Documentación](#-documentación)

</div>

---

## 🚀 Características Principales

### 🖥️ **Interfaz Gráfica Moderna**
- Aplicación de escritorio intuitiva construida con **PyQt6**
- Diseño personalizable con temas oscuro y claro
- Navegación fluida entre módulos
- Barra de herramientas integrada con acceso rápido

### 🤖 **Machine Learning Avanzado**
- **Random Forest**: Clasificador de ensamblaje robusto
- **SVM**: Support Vector Machine con kernel RBF
- **Regresión Logística**: Modelo lineal eficiente
- **Naive Bayes**: Clasificador probabilístico optimizado

### 🧠 **Deep Learning de Vanguardia**
- **BERT**: Transformer pre-entrenado en español (`dccuchile/bert-base-spanish-wwm-uncased`)
- **LSTM Bidireccional**: Redes neuronales recurrentes para análisis secuencial
- **CNN**: Redes convolucionales adaptadas para procesamiento de texto
- **Fine-tuning**: Técnicas avanzadas de transferencia de aprendizaje

### 🎓 **Entrenamiento Personalizado**
- Módulo integrado para entrenar modelos personalizados
- Soporte para datasets en formato PDF organizados por categorías
- Validación cruzada y métricas de evaluación
- Exportación e importación de modelos entrenados

### 🌐 **API Web Integrada**
- **Flask API** para gestión de postulaciones
- Panel de administración web
- Formulario de postulación responsive
- Integración con base de datos SQLite

### 📊 **Gestión de Datos**
- Base de datos **SQLite** integrada
- Almacenamiento persistente de resultados
- Exportación de datos en múltiples formatos
- Sistema de notificaciones inteligente

## � Tecnologías

### 🖥️ **Frontend & GUI**
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **PyQt6** | 6.0+ | Interfaz gráfica principal |
| **PyQt6-WebEngine** | 6.0+ | Navegador web integrado |
| **HTML/CSS/JS** | - | Panel web de administración |

### 🤖 **Machine Learning & AI**
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **TensorFlow** | 2.8+ | Framework de Deep Learning |
| **Transformers** | 4.0+ | Modelos BERT y Transformers |
| **Scikit-learn** | 1.0+ | Algoritmos de ML clásicos |
| **NumPy** | 1.21+ | Computación numérica |
| **Pandas** | 1.3+ | Manipulación de datos |

### 🌐 **Backend & API**
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Flask** | 2.0+ | API web y servidor |
| **Flask-CORS** | 3.0+ | Manejo de CORS |
| **SQLite** | 3.0+ | Base de datos integrada |

### 📄 **Procesamiento de Documentos**
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **PyPDF2** | 2.0+ | Extracción de texto PDF |
| **Joblib** | 1.0+ | Serialización de modelos |
| **SciPy** | 1.7+ | Computación científica |

---

## 📂 Arquitectura del Proyecto

```
cv_clasification/
├── 🎯 main_gui.py                    # Punto de entrada principal
├── 📊 db_manager.py                  # Gestión de base de datos
├── 🎵 create_success_sound.py        # Efectos de sonido
│
├── 🖼️ vista_principal/
│   ├── entrenar_vista.py             # Interfaz de entrenamiento
│   ├── vista_centro_accion.py        # Panel de clasificación
│   ├── vista_herramientas.py         # Gestión de modelos
│   ├── vista_importar_exportar.py    # Import/Export
│   └── vistas_contenido.py           # Contenido dinámico
│
├── 🧠 models/                        # Núcleo de IA
│   ├── cv_classifier.py             # Clasificadores ML
│   ├── deep_learning_classifier.py  # Modelos DL
│   └── model_manager.py             # Gestión de modelos
│
├── 🎓 entrenamiento_vistas/          # Módulos de entrenamiento
│   ├── vista_ml_entrenamiento.py    # Entrenamiento ML
│   └── vista_dl_entrenamiento.py    # Entrenamiento DL
│
├── 🌐 page/                          # API Web
│   ├── postulacion_api.py           # Endpoints Flask
│   ├── postulacion_backend.py       # Lógica de backend
│   ├── postulacion_classification_api.py # API de clasificación
│   ├── postulacion_db.py            # Gestión DB web
│   ├── admin_page.html              # Panel admin
│   └── postulacion.html             # Formulario web
│
├── 🔔 notificacion/                  # Sistema de notificaciones
│   ├── notification_manager.py      # Gestor principal
│   └── model_notifications.py       # Notificaciones de modelos
│
├── 🎨 resources/
│   ├── icons/                       # Iconos SVG
│   ├── icons_png/                   # Iconos PNG
│   └── docs/                        # Documentación HTML
│
├── 💾 Almacenamiento/
│   ├── saved_models/                # Modelos ML serializados
│   ├── saved_deep_models/           # Modelos DL y caché
│   └── cache/                       # Archivos temporales
│
└── ⚙️ src/config/                    # Configuración centralizada
```

## � Instalación

### 📋 **Requisitos del Sistema**

| Componente | Requisito Mínimo | Recomendado |
|------------|------------------|-------------|
| **Python** | 3.8+ | 3.9+ |
| **RAM** | 8 GB | 16 GB+ |
| **CPU** | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| **GPU** | - | NVIDIA GTX 1060+ (CUDA) |
| **Almacenamiento** | 5 GB | 10 GB+ |

### 🚀 **Instalación Rápida**

```bash
# 1. Clonar el repositorio
git clone https://github.com/yonsn76/clsificacion_cv.git
cd clsificacion_cv

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. (Opcional) Instalar herramientas de desarrollo
pip install -r requirements-dev.txt
```

### 🔧 **Configuración GPU (Opcional)**

Para acelerar el entrenamiento de modelos de Deep Learning:

```bash
# Instalar TensorFlow con soporte GPU
pip install tensorflow-gpu

# Verificar instalación GPU
python -c "import tensorflow as tf; print('GPU disponible:', tf.config.list_physical_devices('GPU'))"
```

## 💻 Uso

### 🖥️ **Aplicación de Escritorio**

```bash
# Iniciar la aplicación principal
python main_gui.py
```

**Funcionalidades principales:**
- 🏠 **Inicio**: Panel de bienvenida y estadísticas
- 🎓 **Entrenamiento**: Crear y entrenar modelos personalizados
- 🧠 **Modelos**: Gestionar modelos guardados
- 📄 **Clasificar CV**: Analizar currículums individuales
- 🔄 **Import/Export**: Transferir modelos entre sistemas

### 🌐 **API Web**

```bash
# Iniciar servidor Flask
python page/postulacion_api.py
```

**Endpoints disponibles:**
- 📝 **Formulario**: `http://localhost:5000/page/postulacion.html`
- 👨‍💼 **Panel Admin**: `http://localhost:5000/page/admin_page.html`
- 🔗 **API REST**: `http://localhost:5000/api/`

### ⚙️ **Variables de Configuración**

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `API_PORT` | Puerto del servidor Flask | `5000` |
| `DB_PATH` | Ruta de la base de datos | `./database.db` |
| `MODEL_PATH` | Directorio de modelos | `./saved_models/` |
| `UPLOAD_FOLDER` | Carpeta de uploads | `./uploads/` |

```bash
# Ejemplo de configuración
export API_PORT=8080
export DB_PATH="/custom/path/database.db"
python page/postulacion_api.py
```

---

## 📖 Documentación

### 📚 **Documentación Técnica**
La documentación completa está disponible en formato HTML interactivo:

```bash
# Abrir documentación desde la aplicación
# Ir a: Barra de herramientas → Documentación
```

O acceder directamente al archivo: `resources/docs/documentation.html`

### 🎯 **Guía de Entrenamiento**

#### **Preparar Dataset**
```
dataset/
├── Ingenieria_Software/
│   ├── cv_001.pdf
│   ├── cv_002.pdf
│   └── ...
├── Diseno_UX/
│   ├── cv_001.pdf
│   └── ...
└── Marketing_Digital/
    └── ...
```

#### **Entrenar Modelo**
1. Abrir la aplicación
2. Ir a **Entrenamiento**
3. Seleccionar tipo de modelo (ML/DL)
4. Configurar parámetros
5. Iniciar entrenamiento

### 🔧 **API Reference**

#### **Clasificar CV**
```python
import requests

# Clasificar un CV
response = requests.post('http://localhost:5000/api/classify',
                        files={'cv': open('curriculum.pdf', 'rb')})
result = response.json()
print(f"Categoría: {result['category']}")
print(f"Confianza: {result['confidence']:.2f}")
```

#### **Obtener Modelos Disponibles**
```python
response = requests.get('http://localhost:5000/api/models')
models = response.json()
for model in models:
    print(f"Modelo: {model['name']} - Precisión: {model['accuracy']:.2f}")
```

---

## 🤝 Contribución

### 🐛 **Reportar Bugs**
1. Verificar que el bug no haya sido reportado
2. Crear un issue detallado
3. Incluir pasos para reproducir
4. Adjuntar logs si es posible

### 💡 **Sugerir Mejoras**
1. Abrir un issue con la etiqueta `enhancement`
2. Describir la funcionalidad propuesta
3. Explicar el caso de uso
4. Proporcionar mockups si aplica

### 🔧 **Desarrollo**
```bash
# Fork del repositorio
git clone https://github.com/tu-usuario/clsificacion_cv.git
cd clsificacion_cv

# Crear rama para feature
git checkout -b feature/nueva-funcionalidad

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
python -m pytest tests/

# Commit y push
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

---


### ⭐ Si este proyecto te fue útil, ¡dale una estrella!

[![GitHub stars](https://img.shields.io/github/stars/yonsn76/clsificacion_cv.svg?style=social&label=Star)](https://github.com/yonsn76/clsificacion_cv)
[![GitHub forks](https://img.shields.io/github/forks/yonsn76/clsificacion_cv.svg?style=social&label=Fork)](https://github.com/yonsn76/clsificacion_cv/fork)

**¡Gracias por usar ClasificaTalento PRO!** 🚀

</div>
