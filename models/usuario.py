from config.mysqlconnection import connectToMySQL
from flask import flash
from models import pintura
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pinturas = []
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre,apellido,email,password,created_at,updated_at) VALUES (%(nombre)s,%(apellido)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('esquema_pinturas').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM usuarios WHERE email = %(email)s;"
        return connectToMySQL('esquema_pinturas').query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE usuarios SET nombre=%(nombre)s,apellido=%(apellido)s,email=%(email)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('esquema_pinturas').query_db(query,data)
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email=%(email)s;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
        user = []
        for datos in results:
            if datos == None:
                return False
            user_data = {
                "id": datos['id'],
                "nombre": datos['nombre'],
                "apellido": datos['apellido'],
                "email": datos['email'],
                "password": datos['password'],
                "created_at": datos['created_at'],
                "updated_at": datos['updated_at']
            }
            user.append(Usuario(user_data))
        return user
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM usuarios WHERE id=%(id)s;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
        user = []
        for datos in results:
            if datos == None:
                return False
            user_data = {
                "id": datos['id'],
                "nombre": datos['nombre'],
                "apellido": datos['apellido'],
                "email": datos['email'],
                "password": datos['password'],
                "created_at": datos['created_at'],
                "updated_at": datos['updated_at']
            }
            user.append(Usuario(user_data))
        return user
    
    @staticmethod
    def validacion_registro(info):
        is_valid = True
        if len(info['first_name']) < 2:
            flash('El nombre debe tener al menos 2 letras','error')
            is_valid = False
        if len(info['last_name']) < 2:
            flash('El apellido debe contener al menos 2 letras','error')
            is_valid = False
        if not EMAIL_REGEX.match(info['email']):
            flash('Correo inválido','error')
            is_valid = False
        if len(info['password']) < 8:
            flash('La contraseña debe contener al menos 8 caracteres','error')
            is_valid = False
        return is_valid
    
    @classmethod
    def pinturas_del_usuario(cls,data):
        query = "SELECT * FROM pinturas WHERE pinturas.autor_id = %(id)s;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
        pinturas = []
        for info in results:
            pintura_data = {
                "id": info['id'],
                "autor_id": info['id'],
                "titulo": info['titulo'],
                "descripcion": info['descripcion'],
                "precio": info['precio'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            pinturas.append(pintura.Pintura(pintura_data))
        return pinturas
    
    @classmethod
    def pinturas_fav_del_usuario(cls,data):
        query = "SELECT * FROM pinturas JOIN pinturas_favoritas ON pinturas.id = pinturas_favoritas.pintura_id JOIN usuarios ON pinturas_favoritas.usuario_id = usuarios.id WHERE usuarios.id = %(id)s;"
        results = connectToMySQL('esquema_pinturas').query_db(query,data)
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
            pinturas.append(pintura.Pintura(pintura_data))
        return pinturas
    
    