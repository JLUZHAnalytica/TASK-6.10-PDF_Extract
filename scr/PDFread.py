# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author；鸿
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

def PDF_read(filename):
    '''读取PDF'''
    output_string = StringIO()
    with open(filename, 'rb') as in_file:
        parser = PDFParser(in_file)
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

def write_xls(text_list,newfilename):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    # 存第一行cell(1,1)和cell(1,2)
    for i in range(len(text_list)):
        booksheet.write(0, i, text_list[i])
    workbook.save('{}.xls'.format(newfilename))
    print('{}.xls保存成功'.format(newfilename))

if __name__ == '__main__':
    pdf_s = glob.glob("*.pdf")
    for pdf_name in pdf_s:
        text = PDF_read(pdf_name)
        text_list = extract(text)
        write_xls(text_list,pdf_name)
    input('按下任意键退出...')


