from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import magenta, pink, blue, green, lightgrey
from reportlab.pdfbase import pdfform
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial','ARIAL.ttf'))
from dataset_builder import build_dataset
import numpy as np
import pandas as pd


def make_form():
    c = canvas.Canvas('C:/storyboards/test_form.pdf')
    c.setFont("Courier", 20)
    c.drawCentredString(300, 700, "Test Form")
    c.drawString(10, 650, 'First Name:')
    form = c.acroForm
    form.textfield(name='fname', tooltip='First Name',
                   x=110, y=635, borderStyle='inset',
                   borderColor=magenta, fillColor=pink,
                   width=300,
                   textColor=blue, forceBorder=True)

    c.drawString(10, 600, 'Last Name:')
    form.textfield(name='lname', tooltip='Last Name',
                   x=110, y=585, borderStyle='inset',
                   borderColor=green, fillColor=magenta,
                   width=300,
                   textColor=blue, forceBorder=True)

    c.drawString(10, 550, 'Address:')
    form.textfield(name='address', tooltip='Address',
                   x=110, y=535, borderStyle='inset',
                   width=400, forceBorder=True)

    c.drawString(10, 500, 'City:')
    form.textfield(name='city', tooltip='City',
                   x=110, y=485, borderStyle='inset',
                   forceBorder=True)

    c.drawString(250, 500, 'State:')
    form.textfield(name='state', tooltip='State',
                   x=350, y=485, borderStyle='inset',
                   forceBorder=True)

    c.drawString(10, 450, 'Zip Code:')
    form.textfield(name='zip_code', tooltip='Zip Code',
                   x=110, y=435, borderStyle='inset',
                   forceBorder=True)
    c.save()

def pdfmaker(sectorname, date):
    doc = SimpleDocTemplate("C:/storyboards/" + sectorname + " - "+ date + "-email.pdf", rightMargin=10, leftMargin=10,
                            topMargin=10, bottomMargin=10, pagesize=(A4[1], A4[0]))
    # initialise empty list (will become our report)
    main_pdf = []
    # this lets us alter para styles to prevent code duplication
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="header", fontSize=24, textColor='#003087', vAlign='MIDDLE'))
    styles.add(ParagraphStyle(name='table', fontSize=8))
    styles.add(ParagraphStyle(name='tablehead', fontSize=8, textColor='#FFFFFF', vAlign='MIDDLE'))
    styles.add(ParagraphStyle(name='execsum', fontSize=14, textColor='#003087',
                              borderColor=colors.HexColor('#003087'), leading=14))
    styles.add(ParagraphStyle(name='bottomText', fontSize=14, textColor='#003087', leading=14,
                              borderColor=colors.HexColor('#003087'), linkUnderline=1, alignment=TA_CENTER))
    logo = Image('ggclogo.jpg', 0.5 * inch * 1.5, 0.45 * inch * 1.5)
    header = Paragraph(sectorname + " - " + date + " Storyboard", styles['header'])
    headertable = Table([[logo, header]])
    headertable.setStyle([('VALIGN', (1, 0), (1, 0), 'TOP'),
                          ('FONTSIZE', (1,0), (1,0), 24),
                          ('TEXTCOLOR', (1,0), (1,0), colors.HexColor('#003087')),
                          ('FONTNAME', (1,0), (1,0), 'Arial'),
                          ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                          ('ALIGN', (1, 0), (1, 0), 'RIGHT')
                          ])

    main_pdf.append(headertable)
    main_pdf.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor('#003087'),
                               spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))

    exec_summary = "<b>Executive Summary</b>: "
    tabledata = []
    with open('C:/storyboards/template.txt') as template:
        for line in template:
            if "*" in line:
                continue
            if "[Exec Summary]" in line:
                line = line.strip().split(" = ")
                exec_summary += line[1]
                continue
            line = line.strip().split(",")
            line[0] = "<i>"+line[0]+"</i>"
            line[5] = "<b>"+line[5]+"</b>"
            print(line)
            tabledata.append(line)
    print(tabledata)
    exec_text = Paragraph(exec_summary, styles['execsum'])
    exec_summary = Table([[exec_text]])
    exec_summary.setStyle([('BOX', (0, 0), (0, 0), 0.006 * inch, (0, 0, 0)),
                           ('BOTTOMPADDING', (0, 0), (0, 0), 12)
                           ])
    main_pdf.append(Spacer(0, 12))
    main_pdf.append(exec_summary)



    tableheaders = ['Date', 'Action', 'Timeframe', 'Responsible Person', 'Update', 'Status']
    tableheaders = [Paragraph(x, styles['tablehead']) for x in tableheaders]
    print(tableheaders)
    tabledata = [[Paragraph(x, styles['table']) for x in item] for item in tabledata]
    tabledata.insert(0, tableheaders)


    target_table = Table(tabledata,
                   colWidths=2.45 * cm)
    q = (len(tabledata[0])-1, len(tabledata)-1)

    target_table.setStyle([('BACKGROUND', (0, 0), (q[0], 0), colors.HexColor("#005EB8")),
                    ('TEXTCOLOR', (0, 0), (q[0], 0), colors.HexColor("#E8EDEE")),
                    ('FONTSIZE', (0, 1), (q[0], 1), 8),
                    ('ALIGN', (0, 0), (q[0], q[1]), 'CENTER'),
                     ('VALIGN', (0,0), (q[0],q[1]), 'MIDDLE'),
                    ('BOX', (0, 1), (q[0], q[1]), 0.006 * inch, colors.black),
                    ('BOX', (0, 0), (q[0], 0), 0.006 * inch, (0, 0, 0))
                    ])
    w, h = target_table.wrap(0, 0)
    statmand_graph = Image('graph1.png', w-25, h+2)
    wrapperTable1 = Table([[statmand_graph, target_table]])

    wrapperTable1.setStyle([('LEFTPADDING', (1, 0), (1, 0), 5),
                            ('LEFTPADDING', (0,0), (0,0), 5),
                            ('RIGHTPADDING', (0,0), (0,0), 0)]
                           )
    main_pdf.append(wrapperTable1)



    table_dataset = build_dataset()
    data_table = Table(np.vstack((list(table_dataset), np.array(table_dataset))).tolist(), colWidths=(3.68 * cm))
    q = (len(table_dataset.columns)-1, len(table_dataset))

    print(table_dataset)
    data_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (q[0], 0), colors.HexColor("#005EB8")),
                                     ('TEXTCOLOR', (0, 0), (q[0], 0), colors.HexColor("#E8EDEE")),
                                     ('FONTSIZE', (0, 1), (q[0], q[1]), 8),
                                     ('ALIGN', (1, 0), (q[0], q[1]), 'CENTER'),
                                     ('BOX', (0, 1), (q[0], q[1]), 0.006 * inch, colors.black),
                                     ('BOX', (0, 0), (q[0], 0), 0.006 * inch, (0, 0, 0))
                                     ]))

    w, h = data_table.wrap(0, 0)
    absence_graph = Image('graph2.png', w-25, h+2)



    wrapperTable2 = Table([[absence_graph, data_table]])
    wrapperTable2.setStyle([('LEFTPADDING', (1, 0), (1, 0), 5),
                            ('LEFTPADDING', (0, 0), (0, 0), 5),
                            ('RIGHTPADDING', (0, 0), (0, 0), 0)]
                           )
    main_pdf.append(wrapperTable2)
    w, h = wrapperTable2.wrap(0, 0)

    workforce_text = Paragraph("This document was produced by the NHS GGC Workforce Planning & Analytics team. "
                               '<br/>For more information or for ad-hoc data requests, please email '
                               '<a href = "mailto:steven.munce@ggc.scot.nhs.uk">Steven Munce</a>.',
                          styles['bottomText'])
    workforce_blurb = Table([[workforce_text]], colWidths=w-12)
    workforce_blurb.setStyle([('BOX', (0, 0), (0, 0), 0.006 * inch, (0, 0, 0)),
                           ('BOTTOMPADDING', (0, 0), (0, 0), 12),
                           ])
    main_pdf.append(workforce_blurb)

    doc.build(main_pdf)
    print(q)
pdfmaker("South Sector", "May 2020")
make_form()