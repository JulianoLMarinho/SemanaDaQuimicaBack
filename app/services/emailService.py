import base64
from email.mime.image import MIMEImage
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import Depends
from app.services.coresEdicaoService import CoresEdicaoService

from app.services.edicaoSemanaService import EdicaoSemanaService


class EmailService:
    def __init__(self, edicaoSemanaService: EdicaoSemanaService = Depends(), coresEdicaoService: CoresEdicaoService = Depends()):
        self.port = 587
        self.password = os.getenv("EMAIL_PASSWORD")
        self.server = os.getenv("EMAIL_SERVER")
        self.email = os.getenv("EMAIL_USER")
        self.semanaService = edicaoSemanaService
        self.corService = coresEdicaoService

    def sendEmail(self, assunto, corpoMensagem, email):

        edicaoSemana = self.semanaService.getEdicaoAtiva()
        cores = self.corService.obterCoresEdicao(edicaoSemana.id)
        logo = edicaoSemana.logo_completa
        if logo is not None:
            logoByte = base64.b64decode(logo.split('base64,')[1])

            logoSemana = MIMEImage(logoByte)
            logoSemana.add_header("Content-ID", "<logoSemana>")

        message = MIMEMultipart("alternative")

        message["Subject"] = assunto
        message["From"] = self.email
        message["To"] = email

        html = f"""\
                <html>
                <body>
                    <table style="min-width: 300px; max-width: 1000px">
                        <tbody>
                            <tr align="center">
                            <td style="width: 40%">
                                <div
                                style="
                                    height: 10px;
                                    border-radius: 3px;
                                    background-color: {cores.cor2};
                                "
                                ></div>
                            </td>
                            <td style="width: 20%">
                                <img
                                style="width: 100%"
                                src="cid:logoSemana"
                                />
                            </td>
                            <td style="width: 40%">
                                <div
                                style="
                                    height: 10px;
                                    border-radius: 3px;
                                    background-color:  {cores.cor2};
                                "
                                ></div>
                            </td>
                            </tr>
                            <tr>
                            <td colspan="3"><div style="margin: 20px 0; font-size: large">{corpoMensagem}</div></td>
                            </tr>
                            <tr>
                            <td colspan="3">
                                <div
                                style="
                                    height: 10px;
                                    border-radius: 3px;
                                    background-color:  {cores.cor2};
                                "
                                ></div>
                            </td>
                            </tr>
                            <tr align="center">
                            <td colspan="3" style="font-size: 11px; color:  {cores.cor1}">
                                Comissão organizadora da {edicaoSemana.numero_edicao}ª Edição da Semana Da Química
                            </td>
                            </tr>
                        </tbody>
                    </table>
                </body>
                </html>
                """

        message.attach(MIMEText(html, 'html'))
        if logo is not None:
            message.attach(logoSemana)

        with smtplib.SMTP(self.server, self.port) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, email,
                            message.as_string())
            server.quit()
