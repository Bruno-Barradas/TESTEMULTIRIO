import os.path
import tkinter as tk
from tkinter import ttk, messagebox
from google.auth.transport.requests import Request
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

class GoogleSheetsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GERÊNCIA")
        self.root.geometry("800x500")  # Set initial window size

        # Initialize Google Sheets
        self.initialize_google_sheets()

        self.create_main_interface()

    def create_main_interface(self):
        self.origin_label = tk.Label(self.root, text="Origem:")
        self.origin_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        origin_options = ["Produto Multirio", "Atendimento SME", "Atendimento a Terceiros", "Pós-Produção", "Parceria", "Chamadas"]
        self.origin_var = tk.StringVar(self.root)
        self.origin_var.set("Selecione a Origem")
        self.origin_menu = tk.OptionMenu(self.root, self.origin_var, *origin_options)
        self.origin_menu.grid(row=0, column=1, sticky='w', padx=10, pady=5)

        self.format_label = tk.Label(self.root, text="Formato:")
        self.format_label.grid(row=1, column=0, sticky='w', padx=10, pady=5)

        format_options = ["CAMPANHA", "DIVULGAÇÃO", "EFEMERIDE", "INSTITUCIONAL", "MATERIA", "PROGRAMA", "TUTORIAL"]
        self.format_var = tk.StringVar(self.root)
        self.format_var.set("Selecione o Formato")
        self.format_menu = tk.OptionMenu(self.root, self.format_var, *format_options)
        self.format_menu.grid(row=1, column=1, sticky='w', padx=10, pady=5)

        self.program_name_label = tk.Label(self.root, text="Nome do Programa:")
        self.program_name_label.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        self.program_name_entry = tk.Entry(self.root, width=60)
        self.program_name_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)

        self.producer_label = tk.Label(self.root, text="Nome do Produtor:")
        self.producer_label.grid(row=3, column=0, sticky='w', padx=10, pady=5)

        producer_options = ["Beatriz Correa", "Bruno Barradas", "Claudia Pinto", "Fernanda Celleghin", "Monica Frazão"]
        self.producer_var = tk.StringVar(self.root)
        self.producer_var.set("Selecione o Produtor")
        self.producer_menu = tk.OptionMenu(self.root, self.producer_var, *producer_options)
        self.producer_menu.grid(row=3, column=1, sticky='w', padx=10, pady=5)

        self.location_label = tk.Label(self.root, text="Local:")
        self.location_label.grid(row=4, column=0, sticky='w', padx=10, pady=5)

        location_options = ["Estúdio", "Locação"]
        self.location_var = tk.StringVar(self.root)
        self.location_var.set("Selecione o Local")
        self.location_menu = tk.OptionMenu(self.root, self.location_var, *location_options)
        self.location_menu.grid(row=4, column=1, sticky='w', padx=10, pady=5)

        self.address_label = tk.Label(self.root, text="Endereço:")
        self.address_label.grid(row=5, column=0, sticky='w', padx=10, pady=5)

        self.address_entry = tk.Entry(self.root, width=80)
        self.address_entry.grid(row=5, column=1, sticky='w', padx=10, pady=5)

        self.observations_label = tk.Label(self.root, text="Observações:")
        self.observations_label.grid(row=6, column=0, sticky='w', padx=10, pady=5)

        self.observations_text = tk.Text(self.root, height=5)
        self.observations_text.grid(row=6, column=1, sticky='w', padx=10, pady=5)

        
        
        
        
        
        self.email_label = tk.Label(self.root, text="Enviar para o e-mail:")
        self.email_label.grid(row=7, column=0, sticky='w', padx=10, pady=5)

        self.email_var = tk.StringVar(self.root)
        self.email_var.set("brunobarradas28@gmail.com")  # Endereço de e-mail padrão
        self.email_entry = tk.Entry(self.root, textvariable=self.email_var, width=60)
        self.email_entry.grid(row=7, column=1, sticky='w', padx=10, pady=5)
        
        
        
        
        
        self.email_subject_label = tk.Label(self.root, text="Assunto do E-mail:")
        self.email_subject_label.grid(row=8, column=0, sticky='w', padx=10, pady=5)

        self.email_subject_entry = tk.Entry(self.root, width=60)
        self.email_subject_entry.grid(row=8, column=1, sticky='w', padx=10, pady=5)
        
        
        
    
        self.submit_button = tk.Button(self.root, text="Enviar Dados", command=self.submit_data)
        self.submit_button.grid(row=9, column=1, padx=10, pady=10, sticky='e')

        
        
        
        
    def initialize_google_sheets(self):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)

    def submit_data(self):
        current_date = datetime.date.today().strftime("%Y-%m-%d")

        program_name = self.program_name_entry.get()
        producer = self.producer_var.get()
        location = self.location_var.get()
        address = self.address_entry.get()
        observations = self.observations_text.get("1.0", "end-1c").strip()
        origin = self.origin_var.get()
        formato = self.format_var.get()
        recipient_email = self.email_var.get()  # Endereço de e-mail do destinatário
        email_subject = self.email_subject_entry.get()  # Assunto do e-mail

        #
        values_to_add = [[current_date, origin, formato, program_name, producer, location, address, observations]]

        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().append(
                spreadsheetId='1XPuVb9OtFd-BmHF4U8xqV2R2XTw2kkY98SQMBS3znDc',
                range='Página1!C1',  # Alterado para a coluna C
                valueInputOption="USER_ENTERED",
                body={"values": values_to_add}
            ).execute()

            print(f"{result['updates']['updatedCells']} cells updated.")

            messagebox.showinfo("Sucesso", "Dados cadastrados com sucesso!")

            self.clear_input_fields()

            # Envie um e-mail com os dados e o assunto (é necessário configurar um servidor SMTP e credenciais de e-mail)
            self.send_email(recipient_email, values_to_add, email_subject)

        except HttpError as err:
            print(err)

    def clear_input_fields(self):
        self.program_name_entry.delete(0, tk.END)
        self.producer_var.set("Selecione o Produtor")
        self.location_var.set("Selecione o Local")
        self.origin_var.set("Selecione a Origem")
        self.format_var.set("Selecione o Formato")
        self.address_entry.delete(0, tk.END)
        self.observations_text.delete("1.0", tk.END)
        self.email_subject_entry.delete(0, tk.END)
        
        
        
        

    def send_email(self, recipient_email, data, email_subject):
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

            messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")

        except Exception as e:
            print("Erro ao enviar e-mail:", e)

if __name__ == '__main__':
    root = tk.Tk()
    app = GoogleSheetsApp(root)
    root.mainloop()