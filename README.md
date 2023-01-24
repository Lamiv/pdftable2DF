# pdftable2DF
## OCR a Table in PDF into a Data Frame, CSV or expose as REST API
Here is an example of using Camelot library to read a PDF with a table in it.
<br/>This mimics the PDF2CSV or Save as CSV functionality of Adobe PDF services. 
<br/>In this implementation, the PDF is read into a Dataframe and exposed as a REST API returning JSON with fields and their values.
<br/>If you want to make it a CSV, just the Pandas function to save the DataFrame as CSV.

The repo consists of 2 files:
#### 1. log.py 
This file contains an implementation of the logger library. You may modify this class to suite your needs.
#### 2. pdfreader.py
This is the PdfReader class, using Camelot to read the PDF file, and tables within it.
It also has an implementation of Flask API to expose the PdfReader as a REST API.

Note: you need to adapt the DF based on the coloumns in your PDF file.
