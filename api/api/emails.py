#!/usr/bin/env python3

import email.message
import mimetypes
import os
import smtplib
import ssl

def generate(sender, recipient, subject, body, attachment_path):
  """Creates an email with an attachement."""
  # Basic Email formatting
  message = email.message.EmailMessage()
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = subject
  message.set_content(body)

  # Process the attachment and add it to the email
  if attachment_path:
      attachment_filename = os.path.basename(attachment_path)
      mime_type, _ = mimetypes.guess_type(attachment_path)
      mime_type, mime_subtype = mime_type.split('/', 1)

      with open(attachment_path, 'rb') as ap:
        message.add_attachment(ap.read(),
                              maintype=mime_type,
                              subtype=mime_subtype,
                              filename=attachment_filename)

  return message

def send(sender, message, recipient):
  # Create a secure SSL context
  #context = ssl.create_default_context()
  """Sends the message to the configured SMTP server."""
  #mail_server = smtplib.SMTP('smtp.gmail.com',587)
  #mail_server.starttls(context=context)
  mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

  mail_server.login(sender, os.environ.get('WEB_APP_GMAIL_PASSWORD'))
  mail_server.sendmail(str(sender), str(recipient), str(message))
  mail_server.quit()
