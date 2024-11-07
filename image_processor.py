import os
import numpy as np
from PIL import Image

def comprimir_imagen(ruta_imagen, carpeta_destino):
    if not ruta_imagen or not carpeta_destino:
        raise ValueError("Ruta de imagen y carpeta de destino son requeridas.")

    # Cargar imagen directamente en RGB y convertirla a una matriz de numpy
    imagen = Image.open(ruta_imagen).convert("RGB")
    imagen_array = np.array(imagen)

    # Aplicar la Transformada de Fourier directamente a la imagen en color
    transformada_fourier = np.fft.fft2(imagen_array, axes=(0, 1))
    transformada_fourier_shift = np.fft.fftshift(transformada_fourier, axes=(0, 1))

    # Compresión: manteniendo solo frecuencias bajas en la matriz 3D
    factor_compresion = 0.5  # Ajuste para mejorar la calidad
    filas, columnas, _ = transformada_fourier_shift.shape
    centro_filas, centro_columnas = filas // 2, columnas // 2
    ancho = int(filas * factor_compresion)
    altura = int(columnas * factor_compresion)

    # Crear una máscara para mantener solo frecuencias bajas en la imagen en color
    mascara = np.zeros((filas, columnas))
    mascara[centro_filas - ancho:centro_filas + ancho, centro_columnas - altura:centro_columnas + altura] = 1
    transformada_comprimida = transformada_fourier_shift * mascara[:, :, np.newaxis]

    # Realizar la Transformada Inversa para recuperar la imagen comprimida
    imagen_inversa_shift = np.fft.ifftshift(transformada_comprimida, axes=(0, 1))
    imagen_inversa = np.fft.ifft2(imagen_inversa_shift, axes=(0, 1))
    imagen_comprimida = np.abs(imagen_inversa).astype(np.uint8)

    # Crear el nombre del archivo comprimido
    nombre_base, _ = os.path.splitext(os.path.basename(ruta_imagen))
    nombre_archivo = os.path.join(carpeta_destino, f"{nombre_base}_comprimida.jpg")

    # Guardar la imagen comprimida en formato JPG con calidad ajustada
    Image.fromarray(imagen_comprimida).save(nombre_archivo, "JPEG", quality=90)  # Ajustar calidad a 90 para mejorar

    return nombre_archivo
