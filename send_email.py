from email.mime.text import MIMEText
import smtplib 

def send_email(email, height, average_height, count):
    from_email="cstreadapps@gmail.com"
    from_password="#Pjs7!e$3L*7"
    to_email=email

    subject="Height Data"
    message="Hey there, your height is <strong>%s</strong> inches. <br> Average height of everyone so far is <strong>%s</strong> from <strong>%s</strong> people. <br> Thanks!" % (height, average_height, count)
    

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)