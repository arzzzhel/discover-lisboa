import os
import secrets
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer

def generate_token():
    """Gerar token seguro para validação"""
    return secrets.token_urlsafe(32)

def get_serializer():
    """Obter serializer para tokens com timestamp"""
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_validation_token(email):
    """Gerar token de validação com timestamp"""
    serializer = get_serializer()
    return serializer.dumps(email, salt='email-validation')

def verify_validation_token(token, max_age=86400):
    """Verificar token de validação (max_age em segundos)"""
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt='email-validation', max_age=max_age)
        return email
    except:
        return None

def send_validation_email(user_email, username, validation_token):
    """Enviar email de validação"""
    try:
        # Configurações SMTP
        smtp_server = current_app.config['SMTP_SERVER']
        smtp_port = current_app.config['SMTP_PORT']
        sender_email = current_app.config['SMTP_EMAIL']
        sender_password = current_app.config['SMTP_PASSWORD']
        app_url = current_app.config['APP_URL']
        
        if not sender_email or not sender_password:
            print("AVISO: Configurações SMTP não definidas. Email não enviado.")
            return False
        
        # Link de validação
        validation_link = f"{app_url}/validate/{validation_token}"
        
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = "Discover Lisboa - Validação de Conta"
        message["From"] = sender_email
        message["To"] = user_email
        
        # Corpo do email em HTML
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">Bem-vindo ao Discover Lisboa!</h2>
                    <p>Olá <strong>{username}</strong>,</p>
                    <p>Obrigado por te registares no Discover Lisboa, o teu guia turístico interativo de Lisboa.</p>
                    <p>Para completar o teu registo, clica no botão abaixo para validar o teu email:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{validation_link}" 
                           style="background-color: #3498db; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Validar Email
                        </a>
                    </div>
                    <p style="font-size: 12px; color: #7f8c8d;">
                        Ou copia e cola este link no teu navegador:<br>
                        <a href="{validation_link}">{validation_link}</a>
                    </p>
                    <p style="font-size: 12px; color: #7f8c8d;">
                        Este link expira em 24 horas.
                    </p>
                    <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 20px 0;">
                    <p style="font-size: 11px; color: #95a5a6;">
                        Se não te registaste no Discover Lisboa, ignora este email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))
        
        # Enviar email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message.as_string())
        
        print(f"Email de validação enviado para: {user_email}")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def allowed_file(filename):
    """Verificar se a extensão do ficheiro é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    """Guardar ficheiro carregado"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adicionar timestamp para evitar colisões
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None

def get_media_type(filename):
    """Determinar tipo de média baseado na extensão"""
    if not filename:
        return None
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in {'png', 'jpg', 'jpeg', 'gif'}:
        return 'image'
    elif ext in {'mp4', 'mov', 'avi'}:
        return 'video'
    elif ext in {'mp3', 'wav'}:
        return 'audio'
    return None
