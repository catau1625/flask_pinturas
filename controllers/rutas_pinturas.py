from crypt import methods
from __init__ import app
from flask import render_template,flash,redirect,session,request
from models import pintura

@app.route('/show/pintura/<int:pintura_id>')
def show_pintura(pintura_id):
    if not 'user_id' in session:
        flash('Debes primero iniciar sesion','error')
        return redirect('/')
    data = {
        "id": pintura_id
    }
    autor = pintura.Pintura.painted_by(data)
    pintura_info = pintura.Pintura.show_pintura_by_id(data)[0]
    return render_template('show_pintura.html',
                           pintura_info = pintura_info,
                           usuarios_suscritos = pintura.Pintura.fans_pintura(data),
                           autor=autor,
                           nombre = session['user_first_name'],
                            apellido = session['user_last_name'],
                            user_id = session['user_id'])

@app.route('/agregar_pintura')
def agregar_pintura():
    if not 'user_id' in session:
        flash('Debes primero iniciar sesion','error')
        return redirect('/')
    return render_template('agregar_pintura.html',
                           nombre = session['user_first_name'],
                            apellido = session['user_last_name'])

@app.route('/agregar_pintura_process',methods=['POST'])
def agregar_pintura_process():
    if not pintura.Pintura.validacion(request.form):
        return redirect('/agregar_pintura')
    data = {
        "autor_id": session['user_id'],
        "titulo": request.form['titulo'],
        "descripcion": request.form['descripcion'],
        "precio": request.form['precio']
    }
    pintura.Pintura.save(data)
    flash('Pintura agregada exitosamente','success')
    return redirect('/inicio_sesion')

@app.route('/agregar/like/<int:pintura_id>')
def agregar_like(pintura_id):
    if not 'user_id' in session:
        flash('Debes primero iniciar sesion','error')
        return redirect('/')
    data = {
        "usuario_id": session['user_id'],
        "pintura_id": pintura_id
    }
    pintura.Pintura.agregar_like(data)
    flash('Like agregado','success')
    return redirect('/inicio_sesion')

@app.route('/editar/pintura/<int:pintura_id>')
def editar_pintura(pintura_id):
    data = {
        "id": pintura_id
    }
    pintura_info = pintura.Pintura.show_pintura_by_id(data)[0]
    return render_template('actualizar_pintura.html',
                           pintura_info=pintura_info,
                           nombre = session['user_first_name'],
                            apellido = session['user_last_name'])

@app.route('/actualizar_pintura_process',methods=['POST'])
def actualizar_pintura_process():
    data = {
        "id": request.form['id'],
        "titulo": request.form['titulo'],
        "descripcion": request.form['descripcion'],
        "precio": request.form['precio']
    }
    pintura.Pintura.update(data)
    flash('Informacion pintura actualizada','success')
    return redirect('/inicio_sesion')

@app.route('/eliminar/pintura/<int:pintura_id>')
def eliminar_pintura(pintura_id):
    data = {
        "id": pintura_id
    }
    pintura.Pintura.delete(data)
    flash('Pintura eliminada','error')
    return redirect('/inicio_sesion')