from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from utils import generate_validation_token, verify_validation_token, send_validation_email
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registo de novo utilizador"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        
        # Validações
        if not username or not email:
            flash('Username e email são obrigatórios.', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username deve ter pelo menos 3 caracteres.', 'error')
            return render_template('register.html')
        
        # Verificar se já existe
        if User.query.filter_by(username=username).first():
            flash('Username já existe.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já registado.', 'error')
            return render_template('register.html')
        
        # Criar utilizador
        user = User(username=username, email=email)
        
        # Gerar token de validação
        validation_token = generate_validation_token(email)
        user.validation_token = validation_token
        user.token_expiration = datetime.utcnow() + timedelta(hours=24)
        
        db.session.add(user)
        db.session.commit()
        
        # Enviar email
        email_sent = send_validation_email(email, username, validation_token)
        
        if email_sent:
            flash(f'Registo efetuado! Verifica o email {email} para validar a conta.', 'success')
        else:
            flash(f'Registo efetuado! Link de validação: /validate/{validation_token}', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/validate/<token>')
def validate_email(token):
    """Validar email através do token"""
    # Verificar token
    email = verify_validation_token(token)
    
    if not email:
        flash('Link de validação inválido ou expirado.', 'error')
        return redirect(url_for('auth.register'))
    
    # Procurar utilizador
    user = User.query.filter_by(email=email, validation_token=token).first()
    
    if not user:
        flash('Utilizador não encontrado.', 'error')
        return redirect(url_for('auth.register'))
    
    if user.is_validated:
        flash('Email já validado. Podes fazer login.', 'info')
        return redirect(url_for('auth.login'))
    
    # Verificar expiração
    if user.token_expiration and datetime.utcnow() > user.token_expiration:
        flash('Link expirado. Solicita novo link de validação.', 'error')
        return redirect(url_for('auth.register'))
    
    # Marcar como validado
    user.is_validated = True
    user.validation_token = None
    db.session.commit()
    
    # Guardar user_id na sessão para definir password
    session['pending_password_user_id'] = user.id
    
    flash('Email validado com sucesso! Define agora a tua password.', 'success')
    return redirect(url_for('auth.set_password'))


@auth_bp.route('/set-password', methods=['GET', 'POST'])
def set_password():
    """Definir password após validação"""
    # Verificar se há utilizador pendente
    user_id = session.get('pending_password_user_id')
    
    if not user_id:
        flash('Sessão inválida. Valida o teu email primeiro.', 'error')
        return redirect(url_for('auth.register'))
    
    user = User.query.get(user_id)
    
    if not user or not user.is_validated:
        flash('Utilizador não encontrado ou email não validado.', 'error')
        session.pop('pending_password_user_id', None)
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validações
        if not password or not password_confirm:
            flash('Preenche ambos os campos de password.', 'error')
            return render_template('set_password.html', username=user.username)
        
        if password != password_confirm:
            flash('As passwords não coincidem.', 'error')
            return render_template('set_password.html', username=user.username)
        
        if len(password) < 6:
            flash('A password deve ter pelo menos 6 caracteres.', 'error')
            return render_template('set_password.html', username=user.username)
        
        # Definir password
        user.set_password(password)
        db.session.commit()
        
        # Limpar sessão
        session.pop('pending_password_user_id', None)
        
        flash('Password definida com sucesso! Podes agora fazer login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('set_password.html', username=user.username)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login de utilizador"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username_or_email or not password:
            flash('Preenche todos os campos.', 'error')
            return render_template('login.html')
        
        # Procurar por username ou email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email.lower())
        ).first()
        
        if not user:
            flash('Utilizador não encontrado.', 'error')
            return render_template('login.html')
        
        if not user.is_validated:
            flash('Email não validado. Verifica o teu email.', 'error')
            return render_template('login.html')
        
        if not user.password_hash:
            flash('Password não definida. Valida o teu email primeiro.', 'error')
            return render_template('login.html')
        
        if not user.check_password(password):
            flash('Password incorreta.', 'error')
            return render_template('login.html')
        
        # Login bem-sucedido
        login_user(user, remember=remember)
        flash(f'Bem-vindo, {user.username}!', 'success')
        
        # Redirecionar para página solicitada ou dashboard
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout de utilizador"""
    logout_user()
    flash('Sessão terminada.', 'info')
    return redirect(url_for('main.index'))
