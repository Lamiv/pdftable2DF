# pdftable2DF
## OCR a Table in PDF into a Data Frame, CSV or expose as REST API
Here is an implementation of Camelot library to read a PDF with a table in it.

This mimics the PDF2CSV or Save as CSV functionality of Adobe PDF services. 

In this implementation, the PDF is read into a Dataframe and exposed as a REST API returning JSON with fields and their values.

If you want to make it a CSV, just the Pandas function to save the DataFrame as CSV.
