import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser


path_config = "config.ini"

def loading_config_info(config_path):
  #Read config.ini file
  config_object = ConfigParser()
  config_object.read(config_path)
  #Get the password
  sender_info = config_object["Sender"]
  reciever_info = config_object["Receiver"]

  username = str(sender_info['email'])
  pwd = str(sender_info['password'])
  target = str(reciever_info['email'])
  return username, pwd, target

def create_text_html():
    # Create the plain-text and HTML version of your message
    text = """\
        Company Contact Country Alfreds Futterkiste
        Maria Anders
        Germany 
        Centro comercial Moctezuma 
        Francisco Chang X`
        Mexico
        """
    html = """ <table>
      <tr>
        <th>Company</toh>
        <th>Contact</th>
        <th>Country</th>
      </tr>
      <tr>
        <td>Alfreds Futterkiste</td>
        <td>Maria Anders</td>
        <td>Germany</td>
      </tr>
      <tr>
        <td>Centro comercial Moctezuma</td>
        <td>Francisco Chang</td>
        <td>Mexico</td>
      </tr>
    </table> 
    """
    return text, html 

def send_email(text, html):
  username, pwd, target = loading_config_info(path_config)
  sender_email = username  # Enter your address
  receiver_email = target # Enter receiver address
  password = pwd

  message = MIMEMultipart("alternative")
  message["Subject"] = "multipart test"
  message["From"] = sender_email
  message["To"] = receiver_email

  text, html = create_text_html()

  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  #server =  smtplib.SMTP_SSL("smtp.gmail.com", 465, context)
  server =  smtplib.SMTP_SSL("smtp.gmail.com")
  #server =  smtplib.SMTP("smtp.gmail.com", 465, context)
  server.login(sender_email, password)
  server.sendmail(sender_email, receiver_email, message.as_string())
  server.quit()

if __name__ == '__main__':
  text, html = create_text_html()
  send_email(text, html)