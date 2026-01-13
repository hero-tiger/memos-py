import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class EmailPlugin:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from_email = settings.SMTP_FROM_EMAIL
        self.smtp_from_name = settings.SMTP_FROM_NAME
        self.smtp_use_tls = settings.SMTP_USE_TLS
    
    def is_configured(self) -> bool:
        return all([
            self.smtp_host,
            self.smtp_username,
            self.smtp_password,
            self.smtp_from_email
        ])
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        if not self.is_configured():
            logger.error("Email plugin is not configured")
            return False
        
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
            message["To"] = to_email
            
            if cc_emails:
                message["Cc"] = ", ".join(cc_emails)
            
            if text_content:
                text_part = MIMEText(text_content, "plain", "utf-8")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)
            
            recipients = [to_email]
            if cc_emails:
                recipients.extend(cc_emails)
            if bcc_emails:
                recipients.extend(bcc_emails)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_use_tls:
                    server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.smtp_from_email, recipients, message.as_string())
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        subject = "Welcome to Memos"
        html_content = f"""
        <html>
            <body>
                <h2>Welcome to Memos, {username}!</h2>
                <p>Thank you for signing up. We're excited to have you on board.</p>
                <p>Start creating your first memo and organize your thoughts efficiently.</p>
                <p>Best regards,<br>The Memos Team</p>
            </body>
        </html>
        """
        return await self.send_email(to_email, subject, html_content)
    
    async def send_password_reset_email(self, to_email: str, reset_link: str) -> bool:
        subject = "Password Reset Request"
        html_content = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>You requested to reset your password. Click the link below to reset it:</p>
                <p><a href="{reset_link}">Reset Password</a></p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </body>
        </html>
        """
        return await self.send_email(to_email, subject, html_content)


email_plugin = EmailPlugin()
