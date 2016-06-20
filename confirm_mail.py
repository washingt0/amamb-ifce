import smtplib


def send_mail(email, mhash):
    smtp = smtplib.SMTP('grupostk.com', 587)
    smtp.starttls()

    de = 'no-reply@grupostk.com'
    senha = '**********'
    smtp.login(de, senha)

    para = []
    para.append(email)
    print para
    msg = """From: %s
    To: %s
    Subject: Confirmacao de cadastro AMAMB

    Para confirmar o seu cadastro clique no link a seguir:
    https://www.grupostk.com/amamb/confirm?id=%s.""" % (de, ', '.join(para), mhash)

    smtp.sendmail(de, para, msg)

    smtp.quit()
    print "enviado"
    return 0
