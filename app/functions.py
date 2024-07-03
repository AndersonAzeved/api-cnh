import cv2
import pytesseract
import pandas as pd
import string
import re
from validate_docbr import CNH


def extractCnhToImage(path):
    image = cv2.imread(path)
    
    data = pytesseract.image_to_data(image)

    dataList = list(map(lambda x: x.split('\t'), data.split('\n')))
    df = pd.DataFrame(dataList[1:], columns=dataList[0])
    df.dropna(inplace=True)
    
    df['conf'] = df['conf'].astype(int)
    useFulData = df.query('conf >= 30')
    imageData = pd.DataFrame()
    imageData['text'] = useFulData['text']
    text = imageData
    
    whitespace = string.whitespace
    punctuation = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'''
    tableWhitespace = str.maketrans('','',whitespace)
    tablePunctuation = str.maketrans('','',punctuation)
    
    def cleanText(txt):
        text = str(txt)
        text = text.lower()
        removewhitespace = text.translate(tableWhitespace)
        removepunctuation = removewhitespace.translate(tablePunctuation)
        
        return str(removepunctuation)
    
    
    df['text'] = df['text'].apply(cleanText)
    dataClean = df.query("text != '' ")
    
    textExtract = ' '
    for data in dataClean:
        textExtract += dataClean[data].astype(str).str.cat(sep=' ')

    cnhList = re.findall(r'\d{11}', textExtract)
    useCNH = CNH()
    for cnh in cnhList:
        if useCNH.validate(cnh):
            return cnh
    
    return None