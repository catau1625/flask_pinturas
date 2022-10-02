from config.mysqlconnection import connectToMySQL
from flask import flash
from models import usuario

class Pintura:
    def __init__(self,data):
        self.id = data['id']
        self.autor_id = data['autor_id']
        self.titulo = data['titulo']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuarios = []
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO pinturas (autor_id,titulo,descripcion,precio,created_at,updated_at) VALUES (%(autor_id)s,%(titulo)s,%(descripcion)s,%(precio)s,NOW(),NOW());"
        return connectToMySQL('esquema_pinturas').query_db(query,data)
    
    @classmethod
    def show_all(cls):
        query = "SELECT * FROM pinturas;"
        results = connectToMySQL('esquema_pinturas').query_db(query)
        pinturas = []
        for info in results:
            pintura_data = {
                "id": info['id'],
                "autor_id": info['autor_id'],
                "titulo": info['titulo'],
                "descripcion": info['descripcion'],
                "precio": info['precio'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            pinturas.append(Pintura(pintura_data))
        return pinturas
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM pinturas_favoritas WHERE pinturas_favoritas.pintura_id = %(id)s;"
        connectToMySQL('esquema_pinturas').query_db(query,data)
        query2 = "DELETE FROM pinturas WHERE id = %(id)s;"
        return connectToMySQL('esquema_pinturas').query_db(query2,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE pinturas SET titulo=%(titulo)s,descripcion=%(descripcion)s,precio=%(precio)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('esquema_pinturas').query_db(query,data)
    
    @classmethod
    def agregar_like(cls,data):
        query = "INSERT INTO pinturas_favoritas (usuario_id,pintura_id) VALUES (%(usuario_id)s,%(pintura_id)s);"
        return connectToMySQL('esquema_pinturas').query_db(query,data)
    
    @classmethod
    def fans_pintura(cls,data):
        query = "SELECT usuarios.id,usuarios.nombre,usuarios.apellido,usuarios.email,usuarios.password,usuarios.created_at,usuarios.updated_at FROM usuarios JOIN pinturas_favoritas ON usuarios.id = pinturas_favoritas.usuario_id JOIN pinturas ON pinturas_favoritas.pintura_id = pinturas.id WHERE pinturas.id=%(id)s GROUP BY usuarios.id;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
        usuarios = []
        for info in results:
            user_data = {
                "id": info['id'],
                "nombre": info['nombre'],
                "apellido": info['apellido'],
                "email": info['email'],
                "password": info['password'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            usuarios.append(usuario.Usuario(user_data))
        return usuarios
    
    @staticmethod
    def validacion(info):
        is_valid = True
        if len(info['titulo']) < 0:
            flash('El nombre de la pintua debe contener al menos 1 caracter','error')
            is_valid = False
        if len(info['descripcion']) < 10:
            flash('La descripción debe contener al menos 3 caracteres','error')
            is_valid = False
        if int(info['precio']) < 0:
            flash('El precio debe ser mayor a $0','error')
            is_valid = False
        return is_valid
    
    @classmethod
    def show_pintura_by_id(cls,data):
        query = "SELECT * FROM pinturas WHERE id=%(id)s;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
        pintura = []
        if not results:
            flash('La pintura solicitada no existe, intente de nuevo','error')
            return False
        for info in results:
            pintura_data = {
                "id": info['id'],
                "autor_id": info['autor_id'],
                "titulo": info['titulo'],
                "descripcion": info['descripcion'],
                "precio": info['precio'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            pintura.append(Pintura(pintura_data))
        print(pintura[0])
        return pintura
    
    @classmethod
    def painted_by(cls,data):
        query = "SELECT * FROM usuarios JOIN pinturas ON usuarios.id = pinturas.autor_id WHERE pinturas.id = %(id)s;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
        autor = []
        for info in results:
            datos_autor = {
                "id": info['id'],
                "nombre": info['nombre'],
                "apellido": info['apellido'],
                "email": info['email'],
                "password": info['password'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            autor.append(usuario.Usuario(datos_autor))
        return autor[0]
    
    @classmethod
    def pinturas_con_autor(cls):
        query = "SELECT pinturas.id,CONCAT(usuarios.nombre,' ',usuarios.apellido) as autor,pinturas.titulo,pinturas.descripcion,pinturas.precio FROM pinturas JOIN usuarios ON pinturas.autor_id = usuarios.id;"
        results = connectToMySQL('esquema_pinturas').query_db(query)
        pinturas = []
        for info in results:
            pinturas_data = {
                "id": info['id'],
                "autor": info['autor'],
                "titulo": info['titulo'],
                "descripcion": info['descripcion'],
                "precio": info['precio']
            }
            pinturas.append(pinturas_data)
        print(pinturas)
        return pinturas