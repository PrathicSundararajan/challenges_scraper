import smtplib, ssl

def send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "myautomatedmachine@gmail.com"  # Enter your address
    receiver_email = "prathic44@gmail.com" # Enter receiver address
    password = '?r!+H-b.9QMZ@}D:w-b$3?{D777pM;'
    message = """\
    Subject: Hi there

    This message is sent from Python."""
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        # TODO: Send email here


#print(len(spans))
def hello():
    print('hello')
if __name__ == '__main__':
    hello()
