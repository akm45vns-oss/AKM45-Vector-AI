"""
Email service using Resend.
Handles transactional emails: verification, password reset, welcome.
"""

from typing import Optional

import resend
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

resend.api_key = settings.RESEND_API_KEY

APP_URL = "http://localhost:3000"  # overridden by env in prod


def _send(*, to: str, subject: str, html: str) -> bool:
    """Internal send helper. Returns True on success."""
    if not settings.RESEND_API_KEY or settings.RESEND_API_KEY.startswith("re_your"):
        logger.warning(
            "RESEND_API_KEY not configured — email skipped",
            to=to,
            subject=subject,
        )
        return False
    try:
        params: resend.Emails.SendParams = {
            "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
            "to": [to],
            "subject": subject,
            "html": html,
        }
        resend.Emails.send(params)
        logger.info("Email sent", to=to, subject=subject)
        return True
    except Exception as exc:
        logger.error("Email send failed", to=to, error=str(exc))
        return False


def send_verification_email(
    to_email: str, user_name: str, token: str
) -> bool:
    """Send email verification link."""
    verify_url = f"{APP_URL}/verify-email?token={token}"
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Inter, sans-serif; background: #0d0f1a; color: #e2e8f0; padding: 40px;">
      <div style="max-width: 520px; margin: 0 auto; background: #141625;
                  border-radius: 16px; padding: 40px; border: 1px solid #1e2238;">
        <div style="text-align: center; margin-bottom: 32px;">
          <h1 style="color: #6b8afd; font-size: 28px; margin: 0;">AKM45 Vector AI</h1>
          <p style="color: #64748b; margin: 4px 0 0;">AI-Powered Recruitment</p>
        </div>
        <h2 style="color: #f1f5f9; font-size: 22px;">Welcome, {user_name}! 👋</h2>
        <p style="color: #94a3b8; line-height: 1.6;">
          Thanks for signing up. Please verify your email address to activate your account.
        </p>
        <div style="text-align: center; margin: 32px 0;">
          <a href="{verify_url}"
             style="background: linear-gradient(135deg, #6b8afd, #a855f7);
                    color: white; padding: 14px 32px; border-radius: 10px;
                    text-decoration: none; font-weight: 600; font-size: 15px;
                    display: inline-block;">
            Verify Email Address
          </a>
        </div>
        <p style="color: #64748b; font-size: 13px; text-align: center;">
          This link expires in 24 hours. If you didn't create an account, ignore this email.
        </p>
        <hr style="border: none; border-top: 1px solid #1e2238; margin: 24px 0;">
        <p style="color: #475569; font-size: 12px; text-align: center;">
          © 2025 HireSmart AI · All rights reserved
        </p>
      </div>
    </body>
    </html>
    """
    return _send(
        to=to_email,
        subject="Verify your HireSmart AI account",
        html=html,
    )


def send_password_reset_email(
    to_email: str, user_name: str, token: str
) -> bool:
    """Send password reset link."""
    reset_url = f"{APP_URL}/reset-password?token={token}"
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Inter, sans-serif; background: #0d0f1a; color: #e2e8f0; padding: 40px;">
      <div style="max-width: 520px; margin: 0 auto; background: #141625;
                  border-radius: 16px; padding: 40px; border: 1px solid #1e2238;">
        <div style="text-align: center; margin-bottom: 32px;">
          <h1 style="color: #6b8afd; font-size: 28px; margin: 0;">AKM45 Vector AI</h1>
        </div>
        <h2 style="color: #f1f5f9; font-size: 22px;">Reset your password 🔐</h2>
        <p style="color: #94a3b8; line-height: 1.6;">
          Hi {user_name}, we received a request to reset your password.
          Click the button below to choose a new one.
        </p>
        <div style="text-align: center; margin: 32px 0;">
          <a href="{reset_url}"
             style="background: linear-gradient(135deg, #6b8afd, #a855f7);
                    color: white; padding: 14px 32px; border-radius: 10px;
                    text-decoration: none; font-weight: 600; font-size: 15px;
                    display: inline-block;">
            Reset Password
          </a>
        </div>
        <p style="color: #64748b; font-size: 13px; text-align: center;">
          This link expires in 1 hour. If you didn't request a password reset, ignore this email.
        </p>
        <hr style="border: none; border-top: 1px solid #1e2238; margin: 24px 0;">
        <p style="color: #475569; font-size: 12px; text-align: center;">
          © 2025 HireSmart AI · All rights reserved
        </p>
      </div>
    </body>
    </html>
    """
    return _send(
        to=to_email,
        subject="Reset your HireSmart AI password",
        html=html,
    )
