import os, camelot, logging, pandas as pd, glob, json, log
#from datetime import datetime
from dateutil import parser
from flask import Flask, request, jsonify, send_file
from tqdm import tqdm
from gevent.pywsgi import WSGIServer

class PdfReader:
    def __init__(self):
        print('PDF to CSV convertor v1.0')
        self.mapped_drive = 'Z:'
        self.logger = log.get_logger("pdfreader")
        self.logger.info("Class initialized")
    def get_file(self, gen_date = ''):
        """
        This method reads one PDF Report file generated for a given date and returns the data as a dataframe.
        It is expected the file name will be like "Data_20221122071008853.PDF"
        Params:
            gen_date: (string)Date that file is generated in YYYYMMDD format. e.g., 20221122
        Returns:
            filename: name of the file read
            path    : complete path so flask can read and return
        """
        success = 1
        data = ''
        filename = ''
        file_pattern = self.mapped_drive + os.sep +'Data_{0}*.PDF'.format(gen_date)
        #get list of files matching the pattern
        pdfFiles = glob.glob(file_pattern)
        if (len(pdfFiles) == 0):
            self.logger.error('File not found')
            raise Exception("File Not Found")
            success = 0
        elif (len(pdfFiles) > 1): 
            self.logger.warning('More than one file found. Program will randomly select one of these (sorted, so may be the latest)')
            pdfFiles.sort(reverse=True)
        if (success == 1):
            self.logger.info('Found and returning file {0}'.format(pdfFiles[0]))
            filename = os.path.basename(pdfFiles[0])
            return filename, pdfFiles[0] #return
    
    def read_file(self, gen_date = ''):
        """
        This method reads one DCS Report file generated for a given date and returns the data as a dataframe.
        It is expected the file name will be like "Data_20221122071008853.PDF"
        Params:
            gen_date: (string)Date that file is generated in YYYYMMDD format. e.g., 20221122
        Returns:
            data: Dataframe with the data
        """
        file_pattern = self.mapped_drive + os.sep +'Data_{0}*.PDF'.format(gen_date)
        #get list of files matching the pattern
        pdfFiles = glob.glob(file_pattern)
        if (len(pdfFiles) == 0):
            self.logger.error('File not found')
            raise Exception("File Not Found")
        elif (len(pdfFiles) > 1): 
            self.logger.warning('More than one file found. Program will randomly select one of these(sorted, so may be the latest)')
            pdfFiles.sort(reverse=True)
        try: 
            self.logger.info('Reading file {0}'.format(pdfFiles[0]))
            #set the table area for better detection and read file using pdf reader
            pdf = camelot.read_pdf(pdfFiles[0], flavor='stream', table_areas=['20,760,530,200'], pages = 'all')
            #save the confidence report
            report = pdf[0].parsing_report
            #some logic to get the for date form the file
            try:
                keyDate = pdf[0].df[5][1]
                dt = parser.parse(keyDate)
            except:
                keyDate = pdf[0].df[5][0]
                dt = parser.parse(keyDate)
            spl = keyDate.split(" ", maxsplit=1)
            self.logger.info('Date/Time in file: {0}'.format(dt))
            pdf[0].df = pdf[0].df.iloc[2:]
            df = pd.DataFrame()
            for page in pdf:
                df = pd.concat([df, page.df],ignore_index=True)
            lines = len(df)
            self.logger.info('Lines read: {0}'.format(lines))
            df['CrDate']= spl[0]
            df['CrTime']= spl[1]
            df['CrDateTime'] = dt
            #df.insert(0, 'CrDate', df.pop('CrDate'))
            self.df = df.rename(columns={0:'DCSTAG', 1:'UNIT', 2:'SHIFT_1',3:'SHIFT_2',4:'SHIFT_3',5:'DAY_TOTAL'})
            self.df = self.df[1:]
            self.df = self.df[self.df.DCSTAG!='CONTENT']
            del df
            print('File read {0}'.format(report))
            return report, self.df
        except:  
            self.logger.exception('File could not be read: Exception raised')
        #camelot.plot(pdf[0], kind='contour').show()
        
app = Flask(__name__)

@app.route('/pdf/getContent', methods=['GET'])
def readPDFFile():
    logger = log.get_logger("pdfreader")
    gen_date = request.args.get('date')
    logger.info('Recieved request for PDF Content /date {0}'.format(gen_date))
    try:
        reader = PdfReader()
        result, data = reader.read_file(gen_date)
    except Exception as e:
        self.logger.exception(str(e))
        return str(e)
    response = { 'result': result, 'content': json.loads(data.to_json( orient='table' ))}
    del reader
    return json.loads(json.dumps(response))

@app.route('/pdf/getFile', methods=['GET'])
def getPDFFile():
    logger = log.get_logger("pdfreader")
    gen_date = request.args.get('date')
    logger.info('Recieved request for PDF File /date {0}'.format(gen_date))
    reader = PdfReader()
    filename, path = reader.get_file(gen_date)
    del reader
    try:
        return send_file(path, attachment_filename=filename, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    #app.run(host = '0.0.0.0')
    logger = log.get_logger("pdfreader")
    logger.info('Starting server at Port 5858')
    http_server = WSGIServer(('0.0.0.0', 5858), app)
    logger.info('Server started...')
    http_server.serve_forever()
