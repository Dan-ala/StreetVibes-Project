import qrcode
numeroWhattsap="3116176355"
mensaje = '¡Holaa 😊, Necesito ayuda con mi personalización, Gracias 😁!'
enlacedenumero=f"https://api.whatsapp.com/send?phone={numeroWhattsap}&text={mensaje}"

codigo_qr = qrcode.QRCode(
    version=10,  # Tamaño del código QR (1 es el más pequeño)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
    box_size=10,  # Tamaño de los módulos del código QR
    border=4,  # Margen alrededor del código QR
)
codigo_qr.add_data(enlacedenumero)
codigo_qr.make(fit=True)

# Crea una imagen del código QR (puedes personalizar el nombre de archivo y el formato)
imagen_codigo_qr = codigo_qr.make_image(fill_color="black", back_color="white")

# Guarda la imagen del código QR
imagen_codigo_qr.save("codigo_qr_whatsapp22.png")

# Imprime un mensaje para confirmar
print("Se ha generado el código QR y se ha guardado como 'codigo_qr_whatsapp.png'.")