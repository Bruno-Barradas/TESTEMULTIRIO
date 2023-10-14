import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Carrega as configurações do arquivo secrets.toml
gsheets_config = {
    "spreadsheet": "https://docs.google.com/spreadsheets/d/16Pkg3aoOjojpTBUVtvGjWYek9OY41xZmcwR7CLdXRsU/edit#gid=0",
    "type": "service_account",
    "project_id": "streamlit-401921",
    "private_key_id": "f6558500ff680e6e27695cb817e9d0d0b04f6482",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0ARzy2ajCpiti\nc2lc2aBL8YyYhpZclsJsrTxpmrc6ZW7eQ/EhZ5iSCn2/xnDYXLoY6h8MpQgQnTz9\nWRzNKbYBzOaowS1LRID/tY1RaEYUTMIF6zif3v90Ocrnx1+SJmmje5k0D7xkmQXe\nzExG3SMqEgDKnt+WfTVQ6KO1kikAXeNA+JUV0jlBdL11hPYQTEcRYNIbMcLCJhrc\nT9eg2i4UR1zsfjvj6e764rpjY7GRe32E5eHQprmhhQMzO5DRq+0Ds/QiZgScwILt\ngk3o/5FUgxuxI0jwJ62cCZmNdqBqUQ06t2S6LqDVqiVlxzQ1yMwI+WyvKeSx8gfy\nGRkbVNpjAgMBAAECggEAT98OkVOzZmuFZLIBVonabthHooZVwc/DhaV44QMdunO3\ntjg/jqsBMAwnsCjFebvrd5KrJFk2MukSXvhjp0WS1UmuL8NH7dX/x3cvtaenMOq+\nTRIKliXFBDWAq0f0SE1zIm99k3RIC/s6d5n/XpJRQCGs6DuGyqfUOIqB2dd5Cgff\nu8ZlxcBNuZ/iRd1acEptaeUhFrKqtQfPiABxQoTLg60vYZj8wvXgNZ34zEd5devk\nr5UFtDxFmJ5vP/oW+zrbasf6Dlqm8tYv4VwLdlNBdYYOG/UWNKH/SQBQRMSAAZGJ\nMudFDCey/1IiKRGWSXc5k0rGEI87JNWHh9jKx2tlgQKBgQDrGR/TbyupElQED/rY\nccJRhCe9TMWG+DYUG2hfxXpsEmY8vKHTvlsIZc8cKtlBxTGXmw0jgbR9xuW9hJDD\nwXYIeyOjtyIc7BSUkWyCQrXefmz+YZB8cMh3/p9TRGLRLZ9J3b5xGqZaBujKPkjb\nPc+/q7xBK0X5+cJEGRgVqKCSqwKBgQDEAgtPGeKbOVxXT/4I70ZwwoNs4EctSJzQ\nCKs+FMnoYrWlTbfwvTvFB1MECaJmzmy8eN4epAEB2ZnHtBQG+jimuEhvxgDiAfgJ\nwnNZibS/paMliHMoh5wqCeAWNb0SlOzTl7Q3RdZ1Fh9cvvKgkL/n3HYQBQF2nvfO\n23dOhVAXKQKBgQDJJCLFnBzHt4WoQB/G5XVyltYFMNTjCCQEifp/zg5Svl84Yc82\nwWtTQP+0wrhEfDlU03SnR0asQeq3fd75jOC2mtxAKuQFyLpG7jDfNcIyjQ4TnT0\nIitx9qhL7nt5KkZZRV21mS5wYe7zcdyVr0m6XG1heGuTVuutpaakiTRwpwKBgQC1\n+mfhgtje4LyY282xIeW2XwGCHiA3LMlaZBIIy2hB9xNKbAOw4SAS55/tibxb0p8l\nxNoEfKPqwcqCnPBTIhFiyImILL85FjbhaMWLhcxoejIkcLDqGi2k4hJIzI/EJrxS\nHvDUuGRJxMZNZ4MADCP/8rEyYlNffGv6g8wa/K7FMQKBgCWw9hwL2/yK0aN3ySKP\n3o9x1sj8A55Z2DigzkWBmsau/jhGKo8v3kGIuy/7AOLPOVwAK0IwxTnU+mWsiMJI\nXFRIdd2T2CabZZ/nlwpoh/oq687bBc/dn4PQIJOtz299buZo4Dy+iysuEpfw11BV\nXuPKZV9JNfMRXXLQ3azmro6o\n-----END PRIVATE KEY-----",
    "client_email": "streamlitmultirio@streamlit-401921.iam.gserviceaccount.com",
    "client_id": "111631547223255663929",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlitmultirio%40streamlit-401921.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}

# Inicializa as credenciais do Google Sheets
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

credentials = Credentials.from_service_account_info(gsheets_config, scopes=scope)
gc = gspread.authorize(credentials)

# Abre a planilha
spreadsheet_url = gsheets_config["spreadsheet"]
sh = gc.open_by_url(spreadsheet_url)

# Adicione um campo de entrada para o nome
name = st.text_input("Insira um nome:")

# Se o nome foi inserido, insira-o na planilha
if name:
    worksheet = sh.get_worksheet(0)  # Escolha a planilha desejada (0 é a primeira planilha)
    worksheet.append_table([[name]])  # Adiciona o nome à planilha

# Faz algo com a planilha, por exemplo, obtém a lista de planilhas
worksheet_list = sh.worksheets()
for worksheet in worksheet_list:
    st.write(worksheet.title)
