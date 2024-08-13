import logging

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

logger = logging.getLogger("django")


class SendEmail:
    def __init__(self, subject: str, body: str, to: list) -> None:
        """
        Send email to list of user

        :parameter
            subject (string): Email subject
            body (string): Email body only text
            to (list): list of recipient

        :return:
            None
        """
        self.subject = subject
        self.body = body
        self.to = to

    def simple_email(self) -> str:
        """
        Send simple text email to list of user

        :parameter
            self (SendEmail): SendEmail objects instance

        :return:
            str: a success message or an error message
        """
        try:
            send_mail(
                self.subject,
                self.body,
                settings.EMAIL_HOST_USER,
                self.to,
                fail_silently=False,
            )
            response = f"Mail send successfully at {self.to}"
            logger.info(response + "\n\n")
            return response
        except Exception as ex:
            logger.error(ex.__str__() + "\n\n")
            return ex.__str__()

    def html_email(self, html_template_path, context) -> str:
        """
        Send html email

        :parameter
            self (SendEmail): SendEmail objects instance

        :return:
            str: a success message or an error message
        """
        try:
            # render html template
            html_content = render_to_string(html_template_path, context)

            send_mail(
                subject=self.subject,
                message=self.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=self.to,
                html_message=html_content,
                fail_silently=False,
            )
            response = f"Mail send successfully at {self.to}"
            logger.info(response + "\n\n")
            return response
        except Exception as ex:
            logger.error(ex.__str__() + "\n\n")
            return ex.__str__()

    def email_with_attachment(self, attachment_path) -> str:
        """
        Send email with attachment to list of user

        :parameter
            self (SendEmail): SendEmail objects instance

        :return:
            str: a success message or an error message
        """
        try:
            email = EmailMessage(
                subject=self.subject,
                body=self.body,
                from_email=settings.EMAIL_HOST_USER,
                to=self.to,
                bcc=[],
                reply_to=[],
                headers={},
            )
            email.attach_file(attachment_path)
            email.send(fail_silently=False)
            response = f"Mail send successfully at {self.to}"
            logger.info(response + "\n\n")
            return response
        except Exception as ex:
            logger.error(ex.__str__() + "\n\n")
            return ex.__str__()
