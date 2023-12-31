# Importación de módulos necesarios
from flask import Flask, request, render_template,redirect,url_for,session,redirect, jsonify, send_from_directory
from flask_uploads import IMAGES, UploadSet, configure_uploads;
from config import connectionBD
from werkzeug.utils import secure_filename
import os
import shutil


# Creación de una instancia de Flask
app = Flask(__name__)

photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "catalogoImg"
configure_uploads(app, photos)

# Define the paths to the source folder (external) and destination folder (static/img)
external_folder = 'catalogoImg'  # Replace with the actual path
destination_folder = 'app/static/img' #Este 'proceso', estará reflejado en la ruta de, /catalogo

# Rutas y Funciones


respuestas = {
    "hola": "¡Hola! ¿En qué puedo ayudarte?",
    "¿qué puedes hacer?": "Te puedo brindar ayuda para:\n<ul><li>Registrarte e ingresar</li><li>Acceder a categorías</li><li>Buscar productos por nombre</li><li>Añadir productos al carrito</li><li>Realizar pagos</li><li>Personalizar tus productos</li></ul> Por favor escribe lo que quieres",
    "¿quién eres?": "Soy un chatbot creado por StreetVibes. Mis desarrolladores son Cristian Arango y Daniel Alarcón.",
    "saludos": "¡Hola! ¿En qué puedo ayudarte?",
    "adios": "¡Hasta luego! Espero vuelvas pronto",
    "chau": "¡Hasta luego!",
    "registrarte e ingresar":"Perfecto, Primero tienes que irte donde Dice (login), Luego das Clic para Registrarte, te registrar y vuelves al login, alli podras iniciar secion para continuar con tus compras",
    "acceder a categoria":"Perfecto, tienes dos Maneras, la primera es en esta pagina principal le das en (catalogo) y apareceran las categorias, tu escoges la de tu gusto y le das click , allí apareceran los productos, la otra es Registrarte y accediendo para que puedas explorar por categorias y añadir productos al carrito",
    "default": "Lo siento, no entiendo esa pregunta."
}

# Definición de múltiples opciones para una misma respuesta
opciones_hola = ["hola", "saludos", "buen día" , "HOLA", "helou","hi", "hola como estas","hellou"]
opciones_adios = ["adios", "chau", "hasta luego", "Hasta pronto","chao", "nos vemos", "hasta la proxima", "See you", "La buena"]
opciones_hacer = ["¿en qué me puedes ayudar?","en que me puedes ayudar","Que puedes hacer","¿qué sabes hacer?","que sabes hacer","¿qué haces?","que haces", "que puedes hacer", "ayuda","necesito ayuda", "ayudame", "me puedes ayudar","'¿me ayudas?"]
opciones_eres = ["quien eres","quien te creo","¿quién te creo","que eres","¿qué eres?","¿que eres?","quien eres?", "que sos"]
opciones_registrar = ["registro","ingresar","quiero ingresar", "quiero registrarme","me quiero registrar","registrarme"]
opciones_categoria = ["ver categorias","quiero ver las categorias", "acceder", "mirar categorias","categorias"]


opciones_hola = [opcion.lower() for opcion in opciones_hola]
opciones_adios = [opcion.lower() for opcion in opciones_adios]
opciones_hacer = [opcion.lower() for opcion in opciones_hacer]
opciones_eres = [opcion.lower() for opcion in opciones_eres]
opciones_registrar = [opcion.lower() for opcion in opciones_registrar]
opciones_categoria = [opcion.lower() for opcion in opciones_categoria]


# Actualización del diccionario de respuestas
respuestas.update({opcion: respuestas["hola"] for opcion in opciones_hola})
respuestas.update({opcion: respuestas["adios"] for opcion in opciones_adios})
respuestas.update({opcion: respuestas["¿qué puedes hacer?"] for opcion in opciones_hacer})
respuestas.update({opcion: respuestas["¿quién eres?"] for opcion in opciones_eres})
respuestas.update({opcion: respuestas["registrarte e ingresar"] for opcion in opciones_registrar})
respuestas.update({opcion: respuestas["acceder a categoria"] for opcion in opciones_categoria})



@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje = data["mensaje"].lower()

    respuesta = respuestas.get(mensaje, respuestas["default"])

    return jsonify({"respuesta": respuesta})

@app.route('/guardar-imagen', methods=['POST'])
def guardar_imagen():
    data = request.get_json()
    image_data = data.get('image_data')  # Obtener los datos de la imagen
    # Aquí deberías guardar la imagen_data en el servidor en la ruta deseada
    # Ejemplo: 
    with open('static/img/', 'wb') as img_file:
            img_file.write(image_data.encode())
    return jsonify({'message': 'Imagen guardada exitosamente'})

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'usuario' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtiene los valores del formulario de inicio de sesión
        session.clear()

        usuario = request.form['usuario']
        password = request.form['password']
        credenciales_validas, es_admin = verificar_credenciales(usuario, password)

        # Realiza la consulta para verificar las credenciales en la base de datos

        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE usuario = %s AND passw = %s", (usuario, password))
        user = cursor.fetchone()  # Obtén una fila de resultados

        if user and password:
            # Si las credenciales son correctas, inicia una sesión para el usuario
            session['usuario'] = usuario
            session['name'] = user['nomClie']  # Supongamos que el nombre del usuario está en la columna 'nomClie'
            return redirect(url_for('products'))  # Redirigir a la página de administrador

        if usuario == 'ADMIN' and password == '12345':
            session['usuario'] = usuario
            return redirect(url_for('adminLogged'))
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            error_msg = 'Usuario o contraseña incorrectos'
            return render_template('login.html', error=error_msg)

    # Si la solicitud es GET o cualquier otra, simplemente muestra la página de inicio de sesión
    return render_template('login.html')

    
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Limpiar la sesión
    return redirect(url_for('principal'))  # Redirigir a la página de inicio de sesión
# Ruta raíz que muestra una página principal
@app.route('/')
def principal():
    return render_template("principal.html")

@app.route('/Pagar')
@login_required
def pagar():
    return render_template("Pagar.html")

@app.route('/admin')
@login_required

def pantallaAdmin():
    return render_template("PantallaAdmin.html")

@app.route('/metodopago')
@login_required

def metodo():
    return render_template("Metodo_pago.html")
    
@app.route('/davivienda')
@login_required

def metododavi():
    return render_template("pagardavi.html")
# Ruta para mostrar el formulario de categorías
@app.route('/formulariodecategoria')
@login_required

def inicioww():
    return render_template('index.html')


# IMGs
def get_imagenes():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    imagenes = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT img FROM referencias"  #
        cursor.execute(sql)  
        imagenes = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return imagenes

# Ruta para registrar una nueva categoría
@app.route('/form', methods=['GET', 'POST'])
@login_required

def registrar_categoria():
    msg = ""  # Variable para almacenar mensajes de respuesta
    if request.method == 'POST':
        nomCate = request.form['nomCate']  # Obtiene el valor del campo 'nomCate' del formulario
        conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos

        if conexion_MySQLdb:
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            # Crea una con  sulta SQL para insertar una nueva categoría en la base de datos
            sql = "INSERT INTO categorias (nomCate) VALUES (%s)"
            valores = (nomCate,)  # Valores a insertar
            cursor.execute(sql, valores)  # Ejecuta la consulta
            conexion_MySQLdb.commit()  # Confirma los cambios en la base de datos
            cursor.close()  # Cierra el cursor
            conexion_MySQLdb.close()  # Cierra la conexión a la base de datos
            msg = 'Registro con éxito'  # Mensaje de éxito
            print(cursor.rowcount, "registro insertado")  # Imprime la cantidad de registros insertados
            print("1 registro insertado, id", cursor.lastrowid)  # Imprime el ID del último registro insertado
        else:
            msg = 'Error en la conexión a la base de datos'  # Mensaje de error en la conexión

        return render_template('index.html', msg='Exitosamente')  # vuelve la plantilla 'index.html' con un mensaje de éxito
    else:
        return render_template('index.html', msg='Método HTTP incorrecto')  # Renderiza la plantilla 'index.html' con un mensaje de error de método HTTP

# Ruta para mostrar el formulario de registro de clientes

@app.route('/formulario_cliente')
@login_required

def inicio_clie():
    return render_template('login.html')

# Ruta para registrar un nuevo cliente
@app.route('/registrarclie', methods=['GET', 'POST'])
def registrar_cliente():
    msg = ""  # Variable para almacenar mensajes de respuesta
    if request.method == 'POST':
        # Obtiene los valores del formulario para registrar un cliente
        nomClie = request.form['nomClie']
        apellidoClie = request.form['apellidoClie']
        email = request.form['email']
        telClie = request.form['telClie']
        usuario = request.form['usuario']
        passw = request.form['password']

        conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos

        if conexion_MySQLdb and nomClie and apellidoClie and email and telClie and usuario and passw:
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            sql = "INSERT INTO clientes (nomClie, apellidoCli, email, telClie, usuario, passw) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (nomClie, apellidoClie, email, telClie, usuario, passw)  # Valores a insertar
            cursor.execute(sql, valores)  
            conexion_MySQLdb.commit()
            cursor.close() 
            conexion_MySQLdb.close()  
            msg = 'Registro con éxito'
            print(cursor.rowcount, "registro insertado")  # Imprime la cantidad de registros insertados
            print("1 registro insertado, id", cursor.lastrowid)  # Imprime el ID del último registro insertado
        else:
            msg = 'Error en la conexión a la base de datos'

        return render_template('login.html', msg='Exitosamente')  # Renderiza la plantilla 'formulario_cliente.html' con un mensaje de éxito
    else:
        return render_template('login.html', msg='Método HTTP incorrecto')  # Renderiza la plantilla 'formulario_cliente.html' con un mensaje de error de método HTTP

# Función para obtener categorías desde la base de datos
def get_categorias():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    categorias = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idCate, nomCate FROM categorias"  #
        cursor.execute(sql)  
        categorias = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return categorias

# Función para obtener telas desde la base de datos
def get_telas():
    conexion_MySQLdb = connectionBD()  
    telas = []  # Lista para almacenar telas
    
    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idTela, nomTela FROM tela"  
        cursor.execute(sql)  
        telas = cursor.fetchall()  # Obtiene todas las filas de telas
        cursor.close()  
        conexion_MySQLdb.close()  
        
    return telas  # Devuelve la lista de telas

#Función de prueba
def get_referencias():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    referencias = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idRef, idCate, code, nomRef, precioRef, descripcionRef, idTela, img FROM referencias"  #
        cursor.execute(sql)  
        referencias = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return referencias

def get_referencias1():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    referencias1 = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idRef, idCate, code, nomRef, precioRef, descripcionRef, idTela, img FROM referencias WHERE idCate = 1"  #
        cursor.execute(sql)  
        referencias1 = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return referencias1

#Función de prueba
def get_referencias2():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    referencias2 = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idRef, idCate, code, nomRef, precioRef, descripcionRef, idTela, img FROM referencias WHERE idCate = 2"  #
        cursor.execute(sql)  
        referencias2 = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return referencias2

#Función de prueba
def get_referencias3():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    referencias3 = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idRef, idCate, code,nomRef, precioRef, descripcionRef, idTela, img FROM referencias WHERE idCate = 3"  #
        cursor.execute(sql)  
        referencias3 = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return referencias3

#Función de prueba
def get_referencias4():
    conexion_MySQLdb = connectionBD()  # Establece una conexión a la base de datos
    referencias4 = []  # Lista para almacenar categorías

    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = "SELECT idRef, idCate, code, nomRef, precioRef, descripcionRef, idTela, img FROM referencias WHERE idCate = 4"  #
        cursor.execute(sql)  
        referencias4 = cursor.fetchall()  # Obtiene todas las filas de categorías
        cursor.close()  
        conexion_MySQLdb.close() 

    return referencias4


# Ruta para registrar referencias
@app.route('/refere', methods=['GET', 'POST'])
@login_required

def referencias():
    if request.method == 'POST':
        idCate = request.form['idCate']
        code = request.form['code']
        nomRef = request.form['nomRef']
        precioRef = request.form['precioRef']
        descripcionRef = request.form['descripcionRef']
        idTela = request.form['idTela']

        img = None  # Initialize img_filename to None

        if 'img' in request.files:
            img_file = request.files['img']
            if img_file:
                # Generate a secure filename
                img_filename = secure_filename(img_file.filename)
                print("Image Filename:", img_filename)  # Add this line to check the filename
                # Save the image in the configured folder
                img_path = os.path.join(app.config["UPLOADED_PHOTOS_DEST"], img_filename)
                img_file.save(img_path)
                img = img_filename  # Store the filename in the img variable

        conexion_MySQLdb = connectionBD()

        if conexion_MySQLdb:
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            sql = "INSERT INTO referencias (idCate, code, nomRef, precioRef, descripcionRef, idTela, img) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (idCate, code, nomRef, precioRef, descripcionRef, idTela, img)
            cursor.execute(sql, valores)
            conexion_MySQLdb.commit()
            cursor.close()
            conexion_MySQLdb.close()
            msg = 'Referencia registrada con éxito'
            print(cursor.rowcount, "registro insertado")
            print("1 registro insertado, id", cursor.lastrowid)
        else:
            return 'Error en la conexión a la base de datos'

    else:
        img_filename = None  # Set img_filename to None if the request method is not POST

    # Obtener categorías y telas desde las funciones definidas anteriormente
    categorias = get_categorias()
    telas = get_telas()

    # Renderiza la plantilla 'ref.html' con las categorías, telas y un mensaje de éxito o error
    return render_template('ref.html', categorias=categorias, telas=telas, msg='Well done!')


@app.route('/editar-Referencias')
@login_required

def editarReferencias():
    return render_template('editarRef.html')





#Testing Shopping-cart
@app.route('/shopping-cart')

def products():
    conexion_MySQLdb = connectionBD()
    referencias = get_referencias()
    categorias = get_categorias()
 
    cursor = conexion_MySQLdb.cursor(dictionary=True)
    sql = "SELECT * FROM referencias"
    cursor.execute(sql)

    rows = cursor.fetchall()
    return render_template('holi.html', products=rows, referencias=referencias, categorias=categorias)
 
@app.route('/add', methods=['POST'])
def add_product_to_cart():
        
        _quantity = int(request.form['quantity'])
        _code = request.form['code']

        if _quantity and _code and request.method == 'POST':
            conexion_MySQLdb = connectionBD()

            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute('SELECT * FROM referencias WHERE code = %s', (_code,))
            row = cursor.fetchone()

            itemArray = {
                    row['code']: {
                        'nomRef': row['nomRef'],
                        'code': row['code'],
                        'quantity': _quantity,
                        'precioRef': row['precioRef'],
                        'img': row['img'],
                        'total_price': _quantity * row['precioRef']
                    }
                }

            if 'cart_item' not in session:
                session['cart_item'] = {}

            if _code in session['cart_item']:
                session['cart_item'][_code]['quantity'] += _quantity
                session['cart_item'][_code]['total_price'] = (
                    session['cart_item'][_code]['quantity'] * row['precioRef']
                )
            else:
                session['cart_item'] = array_merge(session['cart_item'], itemArray)

            all_total_quantity = sum(
                int(item['quantity']) for item in session['cart_item'].values()
            )
            all_total_price = sum(
                float(item['total_price']) for item in session['cart_item'].values()
            )

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            return redirect(url_for('products'))
        else:
            return 'Error: Invalid quantity or product ID'
 
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)
 
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
         
        for item in session['cart_item'].items():
            if item[0] == code:    
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
         
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
             
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)
 
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False





#CATALOGO - DAN
@app.route('/catalogo')
def catalogo():
    categorias = get_categorias()

    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through files in the external folder and copy them to the destination folder
    for filename in os.listdir(external_folder):
        src_path = os.path.join(external_folder, filename)
        dst_path = os.path.join(destination_folder, filename)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)

    return render_template('catalogo.html',categorias=categorias)


@app.route('/customize')
@login_required
def personalizarArticulos():
    referencias = get_referencias()
    return render_template('customize.html',referencias=referencias)

def buzosOver():
    referencias = get_referencias1()
    categorias = get_categorias()
    return render_template('4BuzosOver/buzosOver.html',referencias=referencias,categorias=categorias)


def buzosOver2():
    referencias = get_referencias1()
    categorias = get_categorias()
    return render_template('holi.html',referencias=referencias,categorias=categorias)


def camisetasOversized():
    referencias = get_referencias2()
    categorias = get_categorias()
    return render_template('2CamisetasOversized/camisetasOversized.html',referencias=referencias,categorias=categorias)

def camisetasOversized2():
    referencias = get_referencias2()
    categorias = get_categorias()
    return render_template('holi.html',referencias=referencias,categorias=categorias)

def camibuzos():
    referencias = get_referencias3()
    categorias = get_categorias()
    return render_template('3Camibuzos/camiBuzos.html',referencias=referencias,categorias=categorias)

def camibuzos2():
    referencias = get_referencias3()
    categorias = get_categorias()
    return render_template('holi.html',referencias=referencias,categorias=categorias)

def buzosBasicos():
    referencias = get_referencias4()
    categorias = get_categorias()
    return render_template('1BuzosBásicos/buzosBasicos.html',referencias=referencias,categorias=categorias)

def buzosBasicos2():
    referencias = get_referencias4()
    categorias = get_categorias()
    return render_template('holi.html',referencias=referencias,categorias=categorias)

@app.route('/catalogo2')
def catalogo2():
    referencias = get_referencias()
    categorias = get_categorias()
    return render_template('hola.html',referencias=referencias,categorias=categorias)


# DIRECCIONES PARA CADA CATEGORÍA
@app.route('/category/<int:category_id>')
def category(category_id):
    # Determine the template name based on the category ID
    categorias = get_categorias()
    template_name = None
    
    if category_id == 1:
        return buzosOver()
    elif category_id == 2:
        return camisetasOversized() 
    elif category_id == 3:
        return camibuzos()
    elif category_id == 4:
        return buzosBasicos()
    
    if template_name is None:
        # Handle the case where the category ID is not recognized
        return "Category not found", 404
    
    referencias = obtener_referencias_por_categoria(category_id)
    
    # Render the selected template
    return render_template(template_name, category_id=category_id, categorias=categorias, referencias=referencias)



# DIRECCIONES PARA CADA CATEGORÍA2
@app.route('/category2/<int:category_id>')
def category2(category_id):
    # Determine the template name based on the category ID
    categorias = get_categorias()
    template_name = None
    
    if category_id == 1:
        return buzosOver2()
    elif category_id == 2:
        return camisetasOversized2() 
    elif category_id == 3:
        return camibuzos2()
    elif category_id == 4:
        return buzosBasicos2()
    
    if template_name is None:
        # Handle the case where the category ID is not recognized
        return "Category not found", 404
    
    referencias = obtener_referencias_por_categoria(category_id)
    
    # Render the selected template
    return render_template(template_name, category_id=category_id, categorias=categorias, referencias=referencias)




def obtener_informacion_de_imagen(image):
    # Supongamos que 'referencias' es una lista de diccionarios
    conexion = connectionBD()
    imagenSeleccionada = []

    try:
        with conexion.cursor() as cursor:
            sql = "SELECT img FROM referencias WHERE idRef = %s"
            cursor.execute(sql, (image,))
            result = cursor.fetchall()  # Retrieve all rows of products
            if result:
                imagenSeleccionada = result[0]
            cursor.close()
    finally:
        conexion.close()  # Cierra la conexión a la base de datos

    return imagenSeleccionada

@app.route('/customize/<string:image>')
@login_required

def customize_image(image):
    # Aquí, debes buscar la información de la imagen con el nombre recibido
    # y pasarla a la plantilla de la página de personalización
    imagenSeleccionada = obtener_informacion_de_imagen(image)
    return render_template('customize.html', imagenSeleccionada=imagenSeleccionada)


def obtener_referencias_por_categoria(category_id):
    # Establece una conexión a la base de datos (ajusta los parámetros de conexión)
    conexion = connectionBD()
    referenciasPorCategoria = []

    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM referencias WHERE idCate = %s"
            cursor.execute(sql, (category_id,))
            referenciasPorCategoria = cursor.fetchall()  # Retrieve all rows of products
            cursor.close()
    finally:
        conexion.close()  # Cierra la conexión a la base de datos

    return referenciasPorCategoria



#login
app.secret_key = "tu_clave_secreta"  # Configura una clave secreta para la gestión de sesiones

@app.route('/Administrador')
@login_required

def adminLogged():
    return render_template('PantallaAdmin.html')
@app.route('/cliente')
@login_required

def viewcliente():
    return render_template('VistaCliente.html')



def verificar_credenciales(usuario, password):
    # Lógica para verificar las credenciales aquí
    # Supongamos que tienes una variable booleana isAdmin que verifica si el usuario es un administrador
    if usuario == "ADMIN" and password == "3116176355":
        return True, True  # Usuario y contraseña de administrador correctos
    elif usuario == "usuario_normal" and password == "contraseña_usuario":
        return True, False  # Usuario y contraseña de usuario normal correctos
    else:
        return False, False  # Credenciales incorrectas



@app.route("/listar")
@login_required
def listar():
    conexion_MySQLdb = connectionBD()
    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)

        # Ejecuta una consulta SQL para obtener todos los clientes
        sql = "SELECT * FROM clientes"
        cursor.execute(sql)

        # Recupera todos los registros de la base de datos
        clientes = cursor.fetchall()

        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        conexion_MySQLdb.close()

        # Renderiza la plantilla HTML para mostrar los clientes
        return render_template('listarC.html', clientes=clientes)
    else:
        return "Error en la conexión a la base de datos"
    
#Eliminar Referencia
@app.route('/eliminarReferencia/<int:referencia_id>', methods=['GET', 'POST'])
@login_required

def eliminarRef(referencia_id):
    conexion_MySQLdb = connectionBD()
    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)

        # Ejecuta una consulta SQL para eliminar el cliente
        sql = "DELETE FROM referencias WHERE idRef = %s"
        cursor.execute(sql, (referencia_id,))  # Debes pasar cliente_id como una tupla

        # Confirma la transacción y cierra la conexión
        conexion_MySQLdb.commit()
        cursor.close()
        conexion_MySQLdb.close()

        success = True  # Set success to True after successful deletion

        # Redirige a la página de listar clientes después de eliminar
        return redirect(request.referrer)
    

@app.route('/editarReferencia/<int:referencia_id>', methods=['GET', 'POST'])
@login_required

def editarReferencia (referencia_id):
    conexion_MySQLdb = connectionBD()
    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)

        if request.method == 'POST':
            # Obtiene los datos del formulario de edición
            idCate = request.form['idCate']
            nomRef = request.form['nomRef']
            precioRef = request.form['precioRef']
            descripcionRef = request.form['descripcionRef']
            idTela = request.form['idTela']


            # Ejecuta una consulta SQL para actualizar la referencia
            sql = "UPDATE referencias SET idCate=%s, nomRef=%s, precioRef=%s, descripcionRef=%s, idTela=%s WHERE idRef=%s"
            cursor.execute(sql, (idCate, nomRef, precioRef, descripcionRef, idTela, referencia_id))

            # Confirma la transacción y cierra la conexión
            conexion_MySQLdb.commit()
            cursor.close()
            conexion_MySQLdb.close()

            msg='Referencia editada correctamente'

            # Redirect to the appropriate page after updating
            return redirect(request.referrer)
        else:
            # Obtiene los datos de la referencia a editar
            sql = "SELECT * FROM referencias WHERE idRef=%s"
            cursor.execute(sql, (referencia_id,))
            referencia = cursor.fetchone()


            categorias = get_categorias()
            telas = get_telas()

            return render_template('editarRef.html', referencia_id=referencia_id, referencia=referencia, categorias=categorias, telas=telas, msg="Well done!")


@app.route('/eliminarCliente/<int:cliente_id>', methods=['GET', 'POST'])
@login_required

def eliminar(cliente_id):
    conexion_MySQLdb = connectionBD()
    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)

        # Ejecuta una consulta SQL para eliminar el cliente
        sql = "DELETE FROM clientes WHERE idClie = %s"
        cursor.execute(sql, (cliente_id,))  # Debes pasar cliente_id como una tupla

        # Confirma la transacción y cierra la conexión
        conexion_MySQLdb.commit()
        cursor.close()
        conexion_MySQLdb.close()

        # Redirige a la página de listar clientes después de eliminar
        return redirect(url_for('listar'))
        



@app.route('/editarCliente/<int:cliente_id>', methods=['GET', 'POST'])
@login_required

def editar(cliente_id):
    conexion_MySQLdb = connectionBD()
    if conexion_MySQLdb:
        cursor = conexion_MySQLdb.cursor(dictionary=True)

        if request.method == 'POST':
            # Obtiene los datos del formulario de edición
            nuevo_nombre = request.form['nomClie']
            nuevo_apellidoClie = request.form['apellidoClie']
            nuevo_email = request.form['email']
            nuevo_telClie = request.form['telClie']
            nuevo_usuario = request.form['usuario']
            nuevo_password = request.form['password']


            # Ejecuta una consulta SQL para actualizar el cliente
            sql = "UPDATE clientes SET nomClie=%s,apellidoCli=%s, email=%s,telClie=%s,usuario=%s,passw=%s WHERE idClie=%s"
            cursor.execute(sql, (nuevo_nombre,nuevo_apellidoClie, nuevo_email,nuevo_telClie,nuevo_usuario,nuevo_password, cliente_id))

            # Confirma la transacción y cierra la conexión
            conexion_MySQLdb.commit()
            cursor.close()
            conexion_MySQLdb.close()

            # Redirige a la página de listar clientes después de editar

            return redirect(url_for('listar'))
        else:
            # Obtiene los datos del cliente a editar
            sql = "SELECT * FROM clientes WHERE idClie = %s"
            cursor.execute(sql, (cliente_id,))
            cliente = cursor.fetchone()

            return render_template('Formulario_Editar_cliente.html',cliente_id=cliente_id, cliente=cliente)
        


if __name__ == '__main__':
    app.run(debug=True, port=8000)
