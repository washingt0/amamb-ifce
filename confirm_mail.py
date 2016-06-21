from email.mime.text import MIMEText
import smtplib
import config


def send_mail(email, mhash):
    smtp = smtplib.SMTP('grupostk.com', 587)
    smtp.starttls()
    mensagem = MIMEText("""
    Para confirmar o seu cadastro clique no link a seguir:
    https://www.grupostk.com/amamb/confirm?id=%s.""" % (mhash))
    smtp.login(config.EMAIL_USER, config.EMAIL_PASSWD)
    print email
    mensagem['Subject'] = "Confirmacao de Cadastro AMAMB"
    mensagem['From'] = config.EMAIL_USER
    mensagem['To'] = email
    smtp.sendmail(config.EMAIL_USER, email, mensagem.as_string())

    smtp.quit()
    print "enviado"
    return 0
