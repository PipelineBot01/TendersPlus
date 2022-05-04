from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import settings



def create_html_doc(doc: dict):
    return f"""
    <h4 style="text-align:center"><strong><a href="{doc['URL']}">{doc['Title']}</a></strong></h4>

    <table align="center" border="0" cellpadding="1" cellspacing="1" style="width:600px">
    <tbody>
        <tr>
            <td style="text-align:right; width:141px"><span style="color:#999999"><strong>Close Date &amp; Time:&nbsp;</strong></span></td>
            <td style="width:346px"><span style="color:#999999">{doc['Close Date & Time']}</span></td>
        </tr>
        <tr>
            <td style="width:141px">
            <p style="text-align:right"><span style="color:#999999"><strong>Location:&nbsp;</strong></span></p>
            </td>
            <td style="width:346px"><span style="color:#999999">{doc['Location']}</span></td>
        </tr>
        <tr>
            <td style="text-align:right; width:141px"><span style="color:#999999"><strong>Divisions:&nbsp;</strong></span></td>
            <td style="width:346px"><span style="color:#999999">{doc['division']}</span></td>
        </tr>
        <tr>
            <td style="text-align:right; width:141px"><span style="color:#999999"><strong>Keywords:&nbsp;</strong></span></td>
            <td style="width:346px"><span style="color:#999999">{' '.join(doc['tags'].split(' ')[:5])}</span></td>
        </tr>
    </tbody>
    </table>
    <h4 style="text-align:center">&nbsp;</h4>
    """


def create_html_message(docs: list, recipients: list):
    html_docs = ' '.join([create_html_doc(doc) for doc in docs])
    print('html docs',html_docs)
    body = f"""
 
    <p style="text-align:center"><a href="http://110.40.137.110/tendersplus/" target="_blank">view more on tendersplus</a></p>

    <h1 style="text-align:center"><span style="color:#1abc9c"><strong><span style="font-family:Arial,Helvetica,sans-serif"><span style="font-size:28px">Find your opportunities &amp; Seize your chance !</span></span></strong></span></h1>

    <p style="text-align:center">&nbsp;</p>
    {html_docs}

    """

    return MessageSchema(
        subject="Seize your chance! - see what's the Grant opportunities recommendation ",
        recipients=recipients,
        body=body,
        subtype='html'
    )


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="TendersPlus",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

def create_sender():
    global conf
    return FastMail(conf)
