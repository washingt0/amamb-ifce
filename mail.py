from email.mime.text import MIMEText
import smtplib
import config


def send_mail(email, mhash, tipo):
    mensagem = ''
    if tipo == 0:
        mensagem = MIMEText("""
            Para confirmar o seu cadastro clique no link a seguir:
            https://www.grupostk.com/amamb/confirm?id=%s.""" % mhash)
        mensagem['Subject'] = "Confirmacao de Cadastro | AMAMB"
    elif tipo == 1:
        mensagem = MIMEText("""
            Para recuperar sua senha clique no link a seguir:
            https://www.grupostk.com/amamb/rescue?id=%s.""" % mhash)
        mensagem['Subject'] = "Recuperacao de senha | AMAMB"
    elif tipo == 2:
        mensagem = MIMEText("""
            Prova: %s
            Professor: %s
            Quantidade de Questoes: %s
            Acertos: %s
            """ % (mhash[0], mhash[1], mhash[2], mhash[3]))
        mensagem['Subject'] = "Resultado da prova | AMAMB"

    mensagem['From'] = config.EMAIL_USER
    mensagem['To'] = email
    smtp = smtplib.SMTP('grupostk.com', 587)
    smtp.starttls()
    smtp.login(config.EMAIL_USER, config.EMAIL_PASSWD)
    smtp.sendmail(config.EMAIL_USER, email, mensagem.as_string())

    smtp.quit()
    print "enviado"
    return 0
