from PyQt5 import QtWidgets, QtCore, QtGui
import os
from image_processor import comprimir_imagen  # Importa la función de compresión

class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)  # Señal para indicar que ha terminado
    progress = QtCore.pyqtSignal(int)    # Señal para actualizar el progreso

    def __init__(self, ruta_imagen, carpeta_destino):
        super().__init__()
        self.ruta_imagen = ruta_imagen
        self.carpeta_destino = carpeta_destino

    @QtCore.pyqtSlot()
    def run(self):
        try:
            nombre_archivo = comprimir_imagen(self.ruta_imagen, self.carpeta_destino)

            # Simular el progreso de la compresión
            for i in range(1, 101):
                QtCore.QThread.msleep(50)  # Simula el tiempo de procesamiento
                self.progress.emit(i)  # Emitir el progreso

            self.finished.emit(nombre_archivo)  # Emitir la señal de finalización

        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")  # Emitir el error

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Images Compressor")
        self.setFixedSize(400, 450)  # Establece un tamaño fijo para la ventana

        # Configurar el layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QGridLayout(self.central_widget)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(15)

        # Establecer el fondo semi-transparente
        palette = self.central_widget.palette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(50, 50, 80, 220))  # Fondo más oscuro
        self.central_widget.setAutoFillBackground(True)
        self.central_widget.setPalette(palette)

        # Título
        self.titulo = QtWidgets.QLabel("Compresor de Imágenes", self)
        self.titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #00bcd4;")  # Color moderno
        self.layout.addWidget(self.titulo, 0, 0, 1, 1, alignment=QtCore.Qt.AlignCenter)

        self.layout.addWidget(QtWidgets.QLabel(), 1, 0)  

        # Campo de texto para mostrar la imagen seleccionada
        self.input_imagen = QtWidgets.QLineEdit()
        self.input_imagen.setPlaceholderText("Ninguna imagen seleccionada")
        self.input_imagen.setReadOnly(True)
        self.input_imagen.setStyleSheet(self.campo_estilo())
        self.layout.addWidget(self.input_imagen, 2, 0, 1, 1, alignment=QtCore.Qt.AlignCenter)

        self.btn_cargar_imagen = QtWidgets.QPushButton("Cargar Imagen")
        self.btn_cargar_imagen.setStyleSheet(self.boton_estilo())
        self.btn_cargar_imagen.clicked.connect(self.cargar_imagen)
        self.layout.addWidget(self.btn_cargar_imagen, 3, 0, 1, 1)

        # Campo de texto para la carpeta seleccionada
        self.input_carpeta = QtWidgets.QLineEdit()
        self.input_carpeta.setPlaceholderText("Ninguna carpeta seleccionada")
        self.input_carpeta.setReadOnly(True)
        self.input_carpeta.setStyleSheet(self.campo_estilo())
        self.layout.addWidget(self.input_carpeta, 4, 0, 1, 1, alignment=QtCore.Qt.AlignCenter)

        self.btn_seleccionar_carpeta = QtWidgets.QPushButton("Seleccionar Carpeta de Destino")
        self.btn_seleccionar_carpeta.setStyleSheet(self.boton_estilo())
        self.btn_seleccionar_carpeta.clicked.connect(self.seleccionar_carpeta)
        self.layout.addWidget(self.btn_seleccionar_carpeta, 5, 0, 1, 1)

        # Espaciado adicional entre los botones
        self.layout.addWidget(QtWidgets.QLabel(), 6, 0)  # Espaciador en la fila 5

        self.btn_comprimir_guardar = QtWidgets.QPushButton("Comprimir y Guardar")
        self.btn_comprimir_guardar.setStyleSheet(self.boton_estilo())
        self.btn_comprimir_guardar.clicked.connect(self.comprimir_y_guardar)
        self.btn_comprimir_guardar.setEnabled(False)
        self.layout.addWidget(self.btn_comprimir_guardar, 7, 0, 1, 1)

        # Variables para almacenar las rutas
        self.ruta_imagen = None
        self.carpeta_destino = None

        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(1, 0)
        self.layout.setRowStretch(2, 0)
        self.layout.setRowStretch(3, 0)
        self.layout.setRowStretch(4, 0)
        self.layout.setRowStretch(5, 0)
        self.layout.setRowStretch(6, 0)
        self.layout.setColumnStretch(0, 1)

    def boton_estilo(self):
        return """
            QPushButton {
                background-color: #00bcd4; 
                color: white; 
                border-radius: 8px; 
                font: 16px 'Segoe UI'; 
                padding: 10px;
                min-width: 250px;  
            }
            QPushButton:hover {
                background-color: #0097a7;
            }
        """

    def campo_estilo(self):
        return """
            QLineEdit {
                background-color: white;
                border: 2px solid #00bcd4;
                border-radius: 8px;
                font: 16px 'Segoe UI'; 
                padding: 10px;
                min-width: 250px;  
            }
        """

    def cargar_imagen(self):
        self.ruta_imagen, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Selecciona una imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if self.ruta_imagen:
            self.input_imagen.setText(os.path.basename(self.ruta_imagen))
            self.verificar_selecciones()

    def seleccionar_carpeta(self):
        self.carpeta_destino = QtWidgets.QFileDialog.getExistingDirectory(self, "Selecciona la carpeta de destino")
        if self.carpeta_destino:
            self.input_carpeta.setText(self.carpeta_destino)
        self.verificar_selecciones()

    def verificar_selecciones(self):
        self.btn_comprimir_guardar.setEnabled(bool(self.ruta_imagen and self.carpeta_destino))

    def comprimir_y_guardar(self):
        if not self.ruta_imagen or not self.carpeta_destino:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Debes seleccionar una imagen y una carpeta de destino.")
            return

        # Crear un diálogo para mostrar la barra de progreso
        dialogo_progreso = QtWidgets.QDialog(self)
        dialogo_progreso.setWindowTitle("Compresión en progreso")
        dialogo_progreso.setModal(True)
        dialogo_progreso.setFixedSize(300, 120)

        # Crear la barra de progreso
        barra_progreso = QtWidgets.QProgressBar(dialogo_progreso)
        barra_progreso.setGeometry(20, 30, 260, 30)
        barra_progreso.setValue(0)

        # Estilo para la barra de progreso
        barra_progreso.setStyleSheet("""
            QProgressBar {
                background-color: #e0e0e0; 
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #00bcd4; 
                border-radius: 5px;
            }
        """)

        # Crear un QLabel para mostrar el mensaje de finalización
        self.mensaje_finalizacion = QtWidgets.QLabel("Compresión en curso...", dialogo_progreso)
        self.mensaje_finalizacion.setGeometry(20, 70, 260, 30)
        self.mensaje_finalizacion.setAlignment(QtCore.Qt.AlignCenter)

        dialogo_progreso.show()  # Mostrar el diálogo

        # Crear y ejecutar el hilo de trabajo
        self.worker = Worker(self.ruta_imagen, self.carpeta_destino)
        self.worker.finished.connect(lambda nombre_archivo: self.finalizar_compresion(nombre_archivo, dialogo_progreso))
        self.worker.progress.connect(barra_progreso.setValue)

        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def finalizar_compresion(self, nombre_archivo, dialogo_progreso):
        dialogo_progreso.close()  # Cerrar el diálogo de progreso
        self.thread.quit()  # Terminar el hilo

        if nombre_archivo:
            QtWidgets.QMessageBox.information(self, "Éxito", f"Imagen comprimida y guardada como: {nombre_archivo}")
