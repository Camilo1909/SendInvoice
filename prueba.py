import os

from PIL import Image


def redimensionar_para_whatsapp(imagen, formato="cuadrada", calidad=85):
    """
    Redimensiona una imagen según los requisitos de WhatsApp Business API
    Args:
        ruta_imagen: Ruta del archivo de imagen
        formato: 'cuadrada' (1080x1080) o 'horizontal' (1200x628)
        calidad: Calidad de compresión (1-100, default 85)
    Returns:
        Ruta del archivo generado
    """

    # Dimensiones según formato
    dimensiones = {"cuadrada": (1080, 1080), "horizontal": (1200, 628)}

    if formato not in dimensiones:
        raise ValueError("Formato debe ser 'cuadrada' o 'horizontal'")

    # Abrir imagen original
    img = Image.open(imagen)

    # Convertir a RGB si es necesario (para PNGs con transparencia)
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = background

    # Obtener dimensiones objetivo
    ancho_objetivo, alto_objetivo = dimensiones[formato]

    # Calcular proporciones
    ratio_original = img.width / img.height
    ratio_objetivo = ancho_objetivo / alto_objetivo

    # Redimensionar manteniendo proporción COMPLETA (sin recortar)
    if ratio_original > ratio_objetivo:
        # Imagen más ancha que el objetivo, ajustar por ancho
        nuevo_ancho = ancho_objetivo
        nuevo_alto = int(ancho_objetivo / ratio_original)
    else:
        # Imagen más alta que el objetivo, ajustar por alto
        nuevo_alto = alto_objetivo
        nuevo_ancho = int(alto_objetivo * ratio_original)

    # Redimensionar la imagen
    img_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    # Crear lienzo del tamaño objetivo con fondo blanco
    img_final = Image.new("RGB", (ancho_objetivo, alto_objetivo), (255, 255, 255))

    # Centrar la imagen redimensionada en el lienzo
    pos_x = (ancho_objetivo - nuevo_ancho) // 2
    pos_y = (alto_objetivo - nuevo_alto) // 2
    img_final.paste(img_redimensionada, (pos_x, pos_y))

    # Generar nombre de archivo de salida
    nombre_base, extension = os.path.splitext(imagen)
    ruta_salida = f"{nombre_base}_whatsapp_{formato}.jpg"

    # Guardar optimizada
    img_final.save(ruta_salida, "JPEG", quality=calidad, optimize=True)

    # Mostrar información
    tamaño_kb = os.path.getsize(ruta_salida) / 1024
    print(f"✅ Imagen procesada: {ruta_salida}")
    print(f"   Dimensiones: {img_final.width}x{img_final.height}")
    print(f"   Tamaño: {tamaño_kb:.2f} KB")

    return ruta_salida


# Ejemplo de uso
if __name__ == "__main__":
    redimensionar_para_whatsapp(calidad=85)
