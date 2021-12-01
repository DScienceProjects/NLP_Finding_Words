import pandas as pd
import json
import os
from werkzeug.utils import secure_filename

import Constants
from NltkPro import NltkProcessing

pred = NltkProcessing()
from logger_class import Logger

log = Logger("IndexPage")


class DataManipulation:
    def cleanFile(self, file):
        with open(file, "r+") as f:
            old = f.read()
            f.seek(0)
            f.write("[" + old[:len(old) - 1] + "]")
            f.close()
            return file

    def convertDataTocsv(self, file, path, filename):

        df = self.extract_words(file)
        df.to_csv(os.path.join(path, Constants.OUTPUT_FOLDER, secure_filename(filename)), index=False)
        return os.path.join(path, Constants.OUTPUT_FOLDER, secure_filename(filename))

    def extract_words(self,file):

            try:
                df = pd.read_csv(file)

                nlt = NltkProcessing()
                l = []

                for data in df['Description']:
                    result = nlt.process(data)
                    res = ""
                    for j in result:
                        res = res + j + " "
                    print(res)
                    l.append(res)

                df['Result'] = l
                return df

            except Exception as e:
                log.add_exception_log(Constants.EXCEPTION_HANDLING + " extract_words() " + e)
                return pd.DataFrame()