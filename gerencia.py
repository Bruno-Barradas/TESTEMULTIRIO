import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Google Sheets code can be integrated here.

# Initialize Streamlit app
st.title("Google Sheets App")

# Input fields
origin = st.selectbox("Origem:", ["Produto Multirio", "Atendimento SME", "Atendimento a Terceiros", "Pós-Produção", "Parceria", "Chamadas"])
format = st.selectbox("Formato:", ["CAMPANHA", "DIVULGAÇÃO", "EFEMERIDE", "INSTITUCIONAL", "MATERIA", "PROGRAMA", "TUTORIAL"])
program_name = st.text_input("Nome do Programa:")
producer = st.selectbox("Nome do Produtor:", ["Beatriz Correa", "Bruno Barradas", "Claudia Pinto", "Fernanda Celleghin", "Monica Frazão"])
location = st.selectbox("Local:", ["Estúdio", "Locação"])
address = st.text_input("Endereço:")
observations = st.text_area("Observações:")
recipient_email = st.text_input("Enviar para o e-mail:", value="brunobarradas28@gmail.com")  # E-mail do destinatário
email_subject = st.text_input("Assunto do E-mail:")

# Submit button
if st.button("Enviar Dados"):
    # Your Google Sheets data submission code can go here.
    # This is where you would send data to Google Sheets.

    # For demonstration purposes, we're just printing the input values.
    print(f"Origin: {origin}")
    print(f"Format: {format}")
    print(f"Program Name: {program_name}")
    print(f"Producer: {producer}")
    print(f"Location: {location}")
    print(f"Address: {address}")
    print(f"Observations: {observations}")
    
    # You can also send an email using the provided recipient_email and email_subject.
    smtp_server = "smtp.gmail.com"  # Gmail SMTP server
    smtp_port = 587  # Gmail SMTP port for TLS
    smtp_username = "producaomultirioteste@gmail.com"  # Your email address
    smtp_password = "rusy scor urcu ugbm"  # Your email password (replace with your actual password)

    subject = email_subject  # Use the provided email subject

    # Create and send an email with the input data
    body = f"Origin: {origin}\nFormat: {format}\nProgram Name: {program_name}\nProducer: {producer}\nLocation: {location}\nAddress: {address}\nObservations: {observations}"
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = subject
    body_text = body
    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_email, msg.as_string())

        st.success("Dados enviados com sucesso e e-mail enviado com sucesso!")

    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
