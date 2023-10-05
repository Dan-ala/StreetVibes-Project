# Importación del módulo mysql.connector que permite trabajar con bases de datos MySQL
import mysql.connector

# Definición de la función connectionBD() que retorna una conexión a la base de datos
def connectionBD():
    try:
        # Intenta establecer una conexión a la base de datos MySQL con los siguientes parámetros:
        mydb = mysql.connector.connect(
            host="localhost",                   
            user="root",                        
            passwd="",                          
            database="proyecto_personalizacion_articulos"
        )
        
        # Si la conexión se establece con éxito, imprime un mensaje de éxito
        print("Conexion exitosa")
        
        # Retorna el objeto de conexión (mydb) para que pueda ser utilizado por otras partes del código
        return mydb
    except mysql.connector.Error as err:
        # Si ocurre un error al conectar, imprime un mensaje de error y retorna None (indicando que la conexión falló)
        print("Error en la conexion a BD:", err)
        return None