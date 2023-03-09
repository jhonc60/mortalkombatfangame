from flask import Flask, render_template, jsonify
from config import config
from flask_mysqldb import MySQL




#------ Instaciamiento de flask
app = Flask(__name__)
# conexion= MySQL(
#     MYSQL_HOST="localhost",
#     MYSQL_USER="root",
#     MYSQL_PASSWORD="",
#     MYSQL_DB="luisplat_juegos",
#     MYSQL_CURSORCLASS="cursor"
# )


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'nuevo-usuario'
app.config['MYSQL_PASSWORD'] = '3004210519'
app.config['MYSQL_DB'] = 'luisplat_juegos'
mysql = MySQL()
mysql.init_app(app)

# Selección de base de datos
#conexion.connection.select_db("MYSQL_DB")

#Ruta de principal
@app.route("/")
def index():
    return render_template('index.html')
    

    
#Ruta de gráficos
@app.route('/graphics')

def graphics():
 def get_data():
        try:
            # Conexión a la base de datos
            conn = mysql.connect()
            cursor = conn.cursor()
            # Consulta SQL para obtener los datos necesarios
            cursor.execute('SELECT COUNT(*) FROM scores WHERE score > 50')
            count1 = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM scores WHERE score <= 50')
            count2 = cursor.fetchone()[0]
            # Se construye el diccionario de datos en formato JSON
            data = {
                'labels': ['Mayores a 50', 'Menores o iguales a 50'],
                'values': [count1, count2]
            }
            # Se cierra la conexión a la base de datos
            cursor.close()
            conn.close()
            # Se retorna los datos en formato JSON
            return jsonify(data)
        except Exception as ex:
            # Si ocurre algún error se retorna un mensaje de error
            return jsonify({'error': str(ex)}), 500
        
 return render_template("graphics/index.html", datos=get_data())

@app.route('/additem')
def additem():
    return render_template('item/index.html')
    # conexion=mysql.connect()
    # cursor=conexion.cursor()
    # cursor.execute("INSERT INTO `user_email`(ID) ")
    # conexion.commit()
    

#404 error
@app.errorhandler(404)
def page_not_found(erreor):
    # note that we set the 404 status explicitly
    return render_template('/404.html'), 404

if __name__ == "__main__":
    app.config.from_object(config["develoment"])
    app.register_error_handler(404,page_not_found)
    app.run()



