import smtplib, ssl
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

def send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = username  # Enter your address
    receiver_email = target # Enter receiver address
    password = pwd
    message =     """\
    Subject: Hi there

    This message is sent from Python."""
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        # TODO: Send email here


if __name__ == '__main__':    
    
    username, pwd, target = loading_config_info(path_config)
    send_email()