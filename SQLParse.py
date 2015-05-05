#-*- coding: UTF-8 -*-

from SQLParser import SelectSQLParser

def SQLParse(originText , sqlType):
    lines = originText.split('\n')
    processedText = ''
    outputText = ''
    for line in lines:
        line = line.strip()
        line = line.replace('\\','')
        processedText = processedText + ' ' + line

    if sqlType in (0,1):
        outputText = SelectSQLParser(processedText.lower(),sqlType).getText()
    elif sqlType in (3,):
        outputText = 'update功能未完善，待编写'
    else:
        outputText = '未完成功能，待编写'

    return  outputText
