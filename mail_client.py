import smtplib
import base64

SENDER = base64.b64decode("c2V0LnRpbWVzLmFwcGxpY2F0aW9uQGdtYWlsLmNvbQ==")
SENDER_NAME = "Set Times"
PASSWORD = base64.b64decode("JDN0LXRpbWVz")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

if __name__ == '__main__':
  recipient = "JonahRRosenberg@gmail.com"
  subject = "Gmail SMTP Test"
  body = "HERRO"

  headers = "\r\n".join(["From: " + "SENDER_NAME",
             "Subject: " + subject,
             "To: " + recipient,
             "MIME-Version: 1.0",
             "Content-Type: text/html"])

  session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
  session.ehlo()
  session.starttls()
  session.ehlo
  session.login(SENDER, PASSWORD)
   
  session.sendmail(SENDER, recipient, headers + "\r\n\r\n" + body)
  print "Sent!"
  session.quit()
  print "Quit"

