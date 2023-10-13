import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of the target spreadsheet.
SPREADSHEET_ID = '1XPuVb9OtFd-BmHF4U8xqV2R2XTw2kkY98SQMBS3znDc'
RANGE_NAME = 'Página1!A1'

def initialize_google_sheets():
    creds = None

    if st.button("Authorize Google Sheets"):
        if st.file_uploader("Upload credentials.json", type=["json"]) is not None:
            st.write("Credentials uploaded successfully.")

    if st.button("Initialize Google Sheets"):
        if st.file_uploader("Upload token.json", type=["json"]) is not None:
            st.write("Token uploaded successfully.")

def submit_data():
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    program_name = st.text_input("Nome do Programa:")
    producer = st.selectbox("Nome do Produtor", ["Beatriz Correa", "Bruno Barradas", "Claudia Pinto", "Fernanda Celleghin", "Monica Frazão"])
    location = st.selectbox("Local", ["Estúdio", "Locação"])
    address = st.text_input("Endereço:")
    observations = st.text_area("Observações")
    origin = st.selectbox("Origem", ["Produto Multirio", "Atendimento SME", "Atendimento a Terceiros", "Pós-Produção", "Parceria", "Chamadas"])
    formato = st.selectbox("Formato", ["CAMPANHA", "DIVULGAÇÃO", "EFEMERIDE", "INSTITUCIONAL", "MATERIA", "PROGRAMA", "TUTORIAL"])
    recipient_email = st.text_input("Enviar para o e-mail:", value="brunobarradas28@gmail.com")
    email_subject = st.text_input("Assunto do E-mail:")

    values_to_add = [[current_date, origin, formato, program_name, producer, location, address, observations]]

    if st.button("Enviar Dados"):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            sheet = build('sheets', 'v4', credentials=creds).spreadsheets()
            result = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range='Página1!C1',
                valueInputOption="USER_ENTERED",
                body={"values": values_to_add}
            ).execute()

            st.write(f"{result['updates']['updatedCells']} cells updated.")
            st.success("Dados cadastrados com sucesso!")

            # Envie um e-mail com os dados e o assunto (é necessário configurar um servidor SMTP e credenciais de e-mail)
            send_email(recipient_email, values_to_add, email_subject)

        except HttpError as err:
            st.error(f"Erro: {err}")

def send_email(recipient_email, data, email_subject):
    smtp_server = "smtp.gmail.com"  # Servidor SMTP do Gmail
    smtp_port = 587  # Porta SMTP para TLS do Gmail
    smtp_username = "producaomultirioteste@gmail.com"  # Seu endereço de e-mail
    smtp_password = "rusy scor urcu ugbm"  # Sua senha de e-mail (substitua pela senha real)

    subject = email_subject  # Use o assunto do e-mail fornecido

    body = "\n".join([" | ".join(row) for row in data])

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

        st.success("E-mail enviado com sucesso!")

    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

if __name__ == '__main__':
    st.title("GERÊNCIA")
    st.sidebar.header("Configurações")
    initialize_google_sheets()
    st.header("Preencha os Dados")
    submit_data()
