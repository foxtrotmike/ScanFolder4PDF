# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 00:03:37 2017

@author: Dr. Fayyaz Minhas (http://faculty.pieas.edu.pk/fayyaz/)

List all pdf file names and their headers so you can find interesting papers in 
a folder
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
        break

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    
    
    return text

if __name__=='__main__':
    search_for = './Downloads/*.pdf'
    from glob import glob
    S = set()
    with open("out.txt",'w') as ofile:
        for f in glob(search_for):
            try:
                text = convert_pdf_to_txt(f)
                ht = ' '.join([l for l in text.split("\n") if len(l.strip())>5][:5])
                if ht in S:
                    continue
                S.add(ht)
                out = ht+"\n"+f+"\n\n"
                print out
                ofile.write(out)
            except Exception:
                continue
       