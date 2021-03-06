# -*- coding: utf-8 -*-

import requests
import sys
import smtplib
import time
import imaplib
import email

FROM_EMAIL = "complete with your email"
FROM_PWD = "complete with your password"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

# Je n'utilise plus cette fonction, elle était là pour la phase de test de l'oracle.
# Elle permet d'afficher le contenu du dernier mail envoyé dans le format spécifié dans le RFC 822 (le RFC 2822 que j'utilise
# pour ma grammaire est une version mise à jour du 822).
def readmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        type, data = mail.search(None,'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        latest_email_id = int(id_list[-1])

        type_mail, data_mail = mail.fetch(latest_email_id, '(RFC822)')
        for response_part in data_mail:
            if isinstance(response_part, tuple):
                msg_received = email.message_from_string(response_part[1])
                return msg_received
    except Exception, e:
        print str(e)

def main(url,subject,message,p_from):
    # Création d'un dictionnaire contenant les paramètres nécessaire pour le formulaire
    data = {"from":p_from, "subject":subject, "message":message}
    # Envoi de la requête POST
    response = requests.post(url,data=data)
    # Monitoring du status code de la réponse
    if(response.status_code != 200):
        exit(180)

    exit(0)

if __name__=="__main__":
    if(len(sys.argv) == 5):
        main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print("Usage: python smtp_oracle.py [url] [subject] [message] [from]")
