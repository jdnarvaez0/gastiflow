"""
Email service for sending verification emails and notifications
"""
import os
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USER)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Gastiflow")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def _get_smtp_connection():
        """Create and return SMTP connection"""
        try:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            return server
        except Exception as e:
            logger.error(f"Error connecting to SMTP server: {e}")
            raise
    
    @staticmethod
    def _send_with_retry(send_func, max_retries=3, base_delay=1):
        """
        Send email with exponential backoff retry mechanism.
        
        Args:
            send_func: Function that performs the actual send
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds for exponential backoff
            
        Returns:
            Tuple (success: bool, error_message: Optional[str])
        """
        for attempt in range(max_retries):
            try:
                return send_func(), None
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Email send attempt {attempt + 1}/{max_retries} failed: {error_msg}")
                
                if attempt < max_retries - 1:
                    # Exponential backoff with jitter: delay = base_delay * 2^attempt + random(0, 1)
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {max_retries} attempts failed. Last error: {error_msg}")
                    return False, error_msg
        
        return False, "Unknown error"
    
    @staticmethod
    def _create_verification_email_html(username: str, verification_link: str) -> str:
        """Create HTML template for verification email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .content h2 {{
                    color: #333;
                    font-size: 22px;
                    margin-top: 0;
                }}
                .content p {{
                    color: #666;
                    font-size: 16px;
                    margin: 15px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 32px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white !important;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 25px 0;
                    transition: transform 0.2s;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #999;
                    font-size: 14px;
                }}
                .divider {{
                    border-top: 1px solid #e0e0e0;
                    margin: 30px 0;
                }}
                .info-box {{
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 Gastiflow</h1>
                </div>
                <div class="content">
                    <h2>¡Bienvenido, {username}! 👋</h2>
                    <p>Gracias por registrarte en Gastiflow. Para completar tu registro y comenzar a gestionar tus finanzas, necesitamos verificar tu dirección de correo electrónico.</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_link}" class="button">Verificar mi correo electrónico</a>
                    </div>
                    
                    <div class="info-box">
                        <p style="margin: 0;"><strong>💡 Consejo:</strong> Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                        <p style="margin: 10px 0 0 0; word-break: break-all; color: #667eea;">{verification_link}</p>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <p style="font-size: 14px; color: #999;">
                        Este enlace de verificación expirará en 24 horas. Si no solicitaste esta verificación, puedes ignorar este correo de forma segura.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Gastiflow - Tu gestor de finanzas personales</p>
                    <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def _create_email_changed_notification_html(username: str) -> str:
        """Create HTML template for email change notification"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #999;
                    font-size: 14px;
                }}
                .warning-box {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 Gastiflow</h1>
                </div>
                <div class="content">
                    <h2>Cambio de correo electrónico</h2>
                    <p>Hola {username},</p>
                    <p>Te informamos que el correo electrónico asociado a tu cuenta de Gastiflow ha sido modificado.</p>
                    
                    <div class="warning-box">
                        <p style="margin: 0;"><strong>⚠️ Importante:</strong> Si no realizaste este cambio, por favor contacta con soporte inmediatamente.</p>
                    </div>
                    
                    <p style="font-size: 14px; color: #999; margin-top: 30px;">
                        Este correo se envió a tu dirección anterior como medida de seguridad.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Gastiflow - Tu gestor de finanzas personales</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def send_verification_email(email: str, token: str, username: str) -> tuple[bool, Optional[str]]:
        """
        Send email verification email with retry mechanism
        
        Args:
            email: Recipient email address
            token: Verification token
            username: User's username
            
        Returns:
            Tuple (success: bool, error_message: Optional[str])
        """
        if not SMTP_USER or not SMTP_PASSWORD:
            logger.warning("SMTP credentials not configured. Email not sent.")
            logger.info(f"Verification link would be: {FRONTEND_URL}/verify-email?token={token}")
            return False, "SMTP not configured"
        
        def _send():
            verification_link = f"{FRONTEND_URL}/verify-email?token={token}"
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Verifica tu correo electrónico - Gastiflow'
            msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
            msg['To'] = email
            
            # Create HTML content
            html_content = EmailService._create_verification_email_html(username, verification_link)
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            server = EmailService._get_smtp_connection()
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Verification email sent to {email}")
            return True
        
        success, error = EmailService._send_with_retry(_send)
        return success, error
    
    @staticmethod
    def send_email_change_notification(old_email: str, username: str) -> tuple[bool, Optional[str]]:
        """
        Send notification to old email when email is changed
        
        Args:
            old_email: Previous email address
            username: User's username
            
        Returns:
            Tuple (success: bool, error_message: Optional[str])
        """
        if not SMTP_USER or not SMTP_PASSWORD:
            logger.warning("SMTP credentials not configured. Email not sent.")
            return False, "SMTP not configured"
        
        def _send():
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Cambio de correo electrónico - Gastiflow'
            msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
            msg['To'] = old_email
            
            # Create HTML content
            html_content = EmailService._create_email_changed_notification_html(username)
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            server = EmailService._get_smtp_connection()
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email change notification sent to {old_email}")
            return True
        
        success, error = EmailService._send_with_retry(_send)
        return success, error
