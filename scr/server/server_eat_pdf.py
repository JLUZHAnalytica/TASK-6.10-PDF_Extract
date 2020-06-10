from flask import Flask,request
from io import StringIO
import glob
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import xlwt
import re
import sys
import os
import base64

app = Flask(__name__)
cache = {}

def PDF_read(data):
    output_string = StringIO()
    parser = PDFParser(data)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    text = output_string.getvalue()[:500]
    return text


def extract(text):
    '''提取text文本'''
    text_list = []
    title_head = re.findall('/P \n\n \n\n \n\n(.*?) \n\n \n\n \n\n',text)[0]
    text_list.append(title_head)
    title = re.findall('作者： \n\n(.*?) \n',text)[0]
    text_list.append(title)
    anuther = re.findall(' \n作者： .*? \n(.*?) \n收稿日期：',text,re.S)[0].replace('\n','')
    text_list.append(anuther)
    Date_of_receipt = re.findall('\n收稿日期： \n(.*?) \n',text,re.S)[0]
    text_list.append(Date_of_receipt)
    first_launch = re.findall(' \n网络首发日期：  (.*?) \n',text,re.S)[0]
    text_list.append(first_launch)
    Reference_format =  re.findall('引用格式： \n\n(.*?) \n\n \n\n \n \n \n \n\n \n\n \n\n网络首发：',text,re.S)[0].split('\n')
    Reference_format[1] = ''.join(Reference_format[:2])
    Reference_format = '\n'.join(Reference_format[1:])
    text_list.append(Reference_format)
    return text_list


@app.route('/')
def eat_pfd():
    pdf_data = request.args.get('pdf')
    # pdf_data.replace('\n','+')
    with open("output/fucking_base64.txt" , 'w') as fd:
        fd.write(pdf_data)
    my_pdf = base64.b64decode(pdf_data)
    return json.dumps(extract(my_pdf), ensure_ascii=False)