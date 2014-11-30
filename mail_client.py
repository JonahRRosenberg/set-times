import smtplib
import base64

SENDER = base64.b64decode("c2V0LnRpbWVzLmFwcGxpY2F0aW9uQGdtYWlsLmNvbQ==")
SENDER_NAME = "Set Times"
PASSWORD = base64.b64decode("JDN0LXRpbWVz")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

class MailClient(object):
  session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
  session.ehlo()
  session.starttls()
  session.ehlo
  session.login(SENDER, PASSWORD)
  print "Successfully logged into mail client"

  def shutdown(self):
    print "Quitting email session"
    self.session.quit()

  def send(self, to_email, event, message):
    #TODO: Check for if still connected and continue to retry

    try:
      subject = "Update on your event {0}".format(event)
      headers = "\r\n".join(["From: " + SENDER_NAME,
                 "Subject: " + subject,
                 "To: " + to_email,
                 "MIME-Version: 1.0",
                 "Content-Type: text/html"])
      body = message
      full_msg = headers + "\r\n\r\n" + body

      print "Sending email. to_email: {0} full_msg: {1}".format(
          to_email, full_msg)
      self.session.sendmail(SENDER, to_email, full_msg)
    except Exception as ex:
      print "ERROR: Exception sending email. ex: {0} message: {1}".format(
          ex, full_msg)

if __name__ == '__main__':
  to_email = "JonahRRosenberg@gmail.com"

  MailClient().send(
      "JonahRRosenberg@gmail.com",
      "Test Subject",
      "Test Message")

  MailClient().shutdown()

