"""
Email service for sending campaigns and transactional emails.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Personalization
from loguru import logger
from app.core.config import settings
from app.core.redis import redis_client


class EmailService:
    """Email service for sending campaigns and transactional emails."""
    
    def __init__(self):
        self.sendgrid_client = None
        self.smtp_config = None
        self._setup_clients()
    
    def _setup_clients(self):
        """Setup email clients based on configuration."""
        # Setup SendGrid if API key is provided
        if settings.SENDGRID_API_KEY:
            self.sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        
        # Setup SMTP configuration
        self.smtp_config = {
            "host": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "username": settings.SMTP_USER,
            "password": settings.SMTP_PASSWORD,
            "use_tls": settings.SMTP_TLS,
            "use_ssl": settings.SMTP_SSL
        }
    
    async def send_campaign_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str = None,
        from_email: str = None,
        from_name: str = None,
        campaign_id: str = None,
        recipient_id: str = None,
        tracking_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Send a campaign email with tracking.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content
            from_email: Sender email address
            from_name: Sender name
            campaign_id: Campaign ID for tracking
            recipient_id: Recipient ID for tracking
            tracking_data: Additional tracking data
            
        Returns:
            Dict containing send result and tracking information
        """
        try:
            # Use SendGrid if available, otherwise use SMTP
            if self.sendgrid_client:
                result = await self._send_via_sendgrid(
                    to_email, subject, html_content, text_content,
                    from_email, from_name, campaign_id, recipient_id, tracking_data
                )
            else:
                result = await self._send_via_smtp(
                    to_email, subject, html_content, text_content,
                    from_email, from_name, campaign_id, recipient_id, tracking_data
                )
            
            # Store tracking information
            await self._store_tracking_data(
                campaign_id, recipient_id, to_email, result, tracking_data
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error sending campaign email: {str(e)}")
            raise
    
    async def send_transactional_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str = None,
        from_email: str = None,
        from_name: str = None,
        template_id: str = None
    ) -> Dict[str, Any]:
        """
        Send a transactional email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content
            from_email: Sender email address
            from_name: Sender name
            template_id: Template ID for tracking
            
        Returns:
            Dict containing send result
        """
        try:
            if self.sendgrid_client:
                result = await self._send_via_sendgrid(
                    to_email, subject, html_content, text_content,
                    from_email, from_name, template_id=template_id
                )
            else:
                result = await self._send_via_smtp(
                    to_email, subject, html_content, text_content,
                    from_email, from_name, template_id=template_id
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error sending transactional email: {str(e)}")
            raise
    
    async def send_bulk_campaign(
        self,
        recipients: List[Dict[str, Any]],
        subject: str,
        html_template: str,
        text_template: str = None,
        from_email: str = None,
        from_name: str = None,
        campaign_id: str = None,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Send bulk campaign emails.
        
        Args:
            recipients: List of recipient data
            subject: Email subject
            html_template: HTML template with placeholders
            text_template: Plain text template with placeholders
            from_email: Sender email address
            from_name: Sender name
            campaign_id: Campaign ID for tracking
            batch_size: Number of emails to send per batch
            
        Returns:
            Dict containing bulk send results
        """
        try:
            results = {
                "total_recipients": len(recipients),
                "sent": 0,
                "failed": 0,
                "errors": [],
                "campaign_id": campaign_id
            }
            
            # Process recipients in batches
            for i in range(0, len(recipients), batch_size):
                batch = recipients[i:i + batch_size]
                
                # Send batch
                batch_results = await self._send_batch(
                    batch, subject, html_template, text_template,
                    from_email, from_name, campaign_id
                )
                
                # Update results
                results["sent"] += batch_results["sent"]
                results["failed"] += batch_results["failed"]
                results["errors"].extend(batch_results["errors"])
                
                # Rate limiting - wait between batches
                if i + batch_size < len(recipients):
                    await asyncio.sleep(1)
            
            return results
            
        except Exception as e:
            logger.error(f"Error sending bulk campaign: {str(e)}")
            raise
    
    async def _send_via_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str = None,
        from_email: str = None,
        from_name: str = None,
        campaign_id: str = None,
        recipient_id: str = None,
        tracking_data: Dict[str, Any] = None,
        template_id: str = None
    ) -> Dict[str, Any]:
        """Send email via SendGrid."""
        try:
            # Prepare email
            from_email = from_email or settings.SENDGRID_FROM_EMAIL
            from_name = from_name or "AI Email Campaign Writer"
            
            mail = Mail(
                from_email=Email(from_email, from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            if text_content:
                mail.content = Content("text/plain", text_content)
            
            # Add tracking data
            if campaign_id or recipient_id or tracking_data:
                personalization = Personalization()
                personalization.add_to(Email(to_email))
                
                # Add custom tracking headers
                if campaign_id:
                    personalization.add_header("X-Campaign-ID", campaign_id)
                if recipient_id:
                    personalization.add_header("X-Recipient-ID", recipient_id)
                if tracking_data:
                    personalization.add_header("X-Tracking-Data", json.dumps(tracking_data))
                
                mail.add_personalization(personalization)
            
            # Send email
            response = self.sendgrid_client.send(mail)
            
            return {
                "success": True,
                "message_id": response.headers.get("X-Message-Id"),
                "status_code": response.status_code,
                "provider": "sendgrid",
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"SendGrid error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "provider": "sendgrid",
                "sent_at": datetime.utcnow().isoformat()
            }
    
    async def _send_via_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str = None,
        from_email: str = None,
        from_name: str = None,
        campaign_id: str = None,
        recipient_id: str = None,
        tracking_data: Dict[str, Any] = None,
        template_id: str = None
    ) -> Dict[str, Any]:
        """Send email via SMTP."""
        try:
            # Prepare email
            from_email = from_email or self.smtp_config["username"]
            from_name = from_name or "AI Email Campaign Writer"
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_email}>"
            msg["To"] = to_email
            
            # Add tracking headers
            if campaign_id:
                msg["X-Campaign-ID"] = campaign_id
            if recipient_id:
                msg["X-Recipient-ID"] = recipient_id
            if tracking_data:
                msg["X-Tracking-Data"] = json.dumps(tracking_data)
            
            # Add content
            if text_content:
                text_part = MIMEText(text_content, "plain")
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_config["host"], self.smtp_config["port"]) as server:
                if self.smtp_config["use_tls"]:
                    server.starttls()
                if self.smtp_config["use_ssl"]:
                    server = smtplib.SMTP_SSL(self.smtp_config["host"], self.smtp_config["port"])
                
                server.login(self.smtp_config["username"], self.smtp_config["password"])
                server.send_message(msg)
            
            return {
                "success": True,
                "message_id": f"smtp_{datetime.utcnow().timestamp()}",
                "status_code": 250,
                "provider": "smtp",
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"SMTP error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "provider": "smtp",
                "sent_at": datetime.utcnow().isoformat()
            }
    
    async def _send_batch(
        self,
        recipients: List[Dict[str, Any]],
        subject: str,
        html_template: str,
        text_template: str = None,
        from_email: str = None,
        from_name: str = None,
        campaign_id: str = None
    ) -> Dict[str, Any]:
        """Send a batch of emails."""
        results = {
            "sent": 0,
            "failed": 0,
            "errors": []
        }
        
        for recipient in recipients:
            try:
                # Personalize content
                html_content = self._personalize_content(html_template, recipient)
                text_content = None
                if text_template:
                    text_content = self._personalize_content(text_template, recipient)
                
                # Send email
                result = await self.send_campaign_email(
                    to_email=recipient["email"],
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content,
                    from_email=from_email,
                    from_name=from_name,
                    campaign_id=campaign_id,
                    recipient_id=recipient.get("id"),
                    tracking_data=recipient.get("tracking_data")
                )
                
                if result["success"]:
                    results["sent"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "email": recipient["email"],
                        "error": result.get("error", "Unknown error")
                    })
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "email": recipient.get("email", "unknown"),
                    "error": str(e)
                })
        
        return results
    
    def _personalize_content(self, template: str, recipient: Dict[str, Any]) -> str:
        """Personalize email content with recipient data."""
        content = template
        
        # Replace placeholders with recipient data
        for key, value in recipient.items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, str):
                content = content.replace(placeholder, value)
        
        return content
    
    async def _store_tracking_data(
        self,
        campaign_id: str,
        recipient_id: str,
        email: str,
        send_result: Dict[str, Any],
        tracking_data: Dict[str, Any] = None
    ):
        """Store email tracking data in Redis."""
        try:
            if not campaign_id:
                return
            
            tracking_key = f"email_tracking:{campaign_id}:{recipient_id}"
            tracking_info = {
                "email": email,
                "sent_at": send_result.get("sent_at"),
                "success": send_result.get("success", False),
                "message_id": send_result.get("message_id"),
                "provider": send_result.get("provider"),
                "status_code": send_result.get("status_code"),
                "error": send_result.get("error"),
                "tracking_data": tracking_data or {}
            }
            
            # Store in Redis with expiration (30 days)
            await redis_client.set(
                tracking_key,
                json.dumps(tracking_info),
                expire=30 * 24 * 3600
            )
            
        except Exception as e:
            logger.error(f"Error storing tracking data: {str(e)}")
    
    async def get_delivery_status(
        self,
        campaign_id: str,
        recipient_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get email delivery status."""
        try:
            tracking_key = f"email_tracking:{campaign_id}:{recipient_id}"
            tracking_data = await redis_client.get(tracking_key)
            
            if tracking_data:
                return json.loads(tracking_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting delivery status: {str(e)}")
            return None
    
    async def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign delivery statistics."""
        try:
            pattern = f"email_tracking:{campaign_id}:*"
            keys = await redis_client.client.keys(pattern)
            
            stats = {
                "total_sent": 0,
                "successful": 0,
                "failed": 0,
                "pending": 0
            }
            
            for key in keys:
                tracking_data = await redis_client.get(key)
                if tracking_data:
                    data = json.loads(tracking_data)
                    stats["total_sent"] += 1
                    
                    if data.get("success"):
                        stats["successful"] += 1
                    else:
                        stats["failed"] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting campaign stats: {str(e)}")
            return {
                "total_sent": 0,
                "successful": 0,
                "failed": 0,
                "pending": 0
            }


# Global email service instance
email_service = EmailService()


async def get_email_service() -> EmailService:
    """Dependency to get email service."""
    return email_service
