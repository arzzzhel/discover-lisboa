from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Content
from utils import save_uploaded_file, get_media_type
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial"""
    # Obter alguns conteúdos em destaque
    featured_contents = Content.query.order_by(Content.created_at.desc()).limit(6).all()
    return render_template('index.html', featured_contents=featured_contents)


# @main_bp.route('/map')
# def map_view():
#     """Mapa público com todos os conteúdos"""
#     contents = Content.query.filter(
#         Content.latitude.isnot(None),
#         Content.longitude.isnot(None)
#     ).all()
#     return render_template('map.html', contents=contents)

@main_bp.route('/map')
def map_view():
    contents = Content.query.filter(
        Content.latitude.isnot(None),
        Content.longitude.isnot(None)
    ).all()

    contents_json = [c.to_dict() for c in contents]
    return render_template('map.html', contents=contents_json)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do utilizador"""
    # Conteúdos do utilizador
    user_contents = Content.query.filter_by(user_id=current_user.id)\
        .order_by(Content.created_at.desc()).all()
    
    return render_template('dashboard.html', contents=user_contents)


@main_bp.route('/content/new', methods=['GET', 'POST'])
@login_required
def new_content():
    """Criar novo conteúdo"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        location_name = request.form.get('location_name', '').strip()
        
        # Validações
        if not title or not description or not category:
            flash('Título, descrição e categoria são obrigatórios.', 'error')
            return render_template('content_form.html')
        
        # Upload de ficheiro
        media_filename = None
        media_type = None
        
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename:
                media_filename = save_uploaded_file(file)
                if media_filename:
                    media_type = get_media_type(media_filename)
                else:
                    flash('Tipo de ficheiro não permitido.', 'error')
                    return render_template('content_form.html')
        
        if not media_type:
            flash('É obrigatório carregar um ficheiro multimédia.', 'error')
            return render_template('content_form.html')
        
        # Converter coordenadas
        lat = float(latitude) if latitude else None
        lon = float(longitude) if longitude else None
        
        # Criar conteúdo
        content = Content(
            title=title,
            description=description,
            category=category,
            media_type=media_type,
            media_filename=media_filename,
            latitude=lat,
            longitude=lon,
            location_name=location_name,
            user_id=current_user.id
        )
        
        db.session.add(content)
        db.session.commit()
        
        flash('Conteúdo criado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('content_form.html', content=None)


@main_bp.route('/content/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_content(id):
    """Editar conteúdo existente"""
    content = Content.query.get_or_404(id)
    
    # Verificar se o utilizador é o autor
    if content.user_id != current_user.id:
        flash('Não tens permissão para editar este conteúdo.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        content.title = request.form.get('title', '').strip()
        content.description = request.form.get('description', '').strip()
        content.category = request.form.get('category', '').strip()
        content.location_name = request.form.get('location_name', '').strip()
        
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        content.latitude = float(latitude) if latitude else None
        content.longitude = float(longitude) if longitude else None
        
        # Upload de novo ficheiro (opcional)
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename:
                # Remover ficheiro antigo
                if content.media_filename:
                    old_file = os.path.join('static/uploads', content.media_filename)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                # Guardar novo ficheiro
                media_filename = save_uploaded_file(file)
                if media_filename:
                    content.media_filename = media_filename
                    content.media_type = get_media_type(media_filename)
        
        db.session.commit()
        flash('Conteúdo atualizado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('content_form.html', content=content)


@main_bp.route('/content/<int:id>/delete', methods=['POST'])
@login_required
def delete_content(id):
    """Eliminar conteúdo"""
    content = Content.query.get_or_404(id)
    
    # Verificar se o utilizador é o autor
    if content.user_id != current_user.id:
        flash('Não tens permissão para eliminar este conteúdo.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Remover ficheiro
    if content.media_filename:
        file_path = os.path.join('static/uploads', content.media_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(content)
    db.session.commit()
    
    flash('Conteúdo eliminado com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/api/contents')
def api_contents():
    """API para obter todos os conteúdos (para o mapa)"""
    contents = Content.query.filter(
        Content.latitude.isnot(None),
        Content.longitude.isnot(None)
    ).all()
    
    return jsonify([content.to_dict() for content in contents])


@main_bp.route('/api/search-location')
def api_search_location():
    """API para pesquisar localização via Nominatim"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Query vazia'}), 400
    
    # Esta rota será usada pelo frontend para chamar a API Nominatim
    # O frontend faz a chamada diretamente ao Nominatim
    return jsonify({'message': 'Use o frontend para pesquisar'})
