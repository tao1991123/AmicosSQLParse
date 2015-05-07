# -*- coding: UTF-8 -*-
import codecs
import re
from SQLParseConst import *



class ColumnName(object):
    """
    列表名称类，通过输入字符串获取列名称，表简写名称，表名称
    """

    def __init__(self, originalText, tableDict):
        if not ('.' in originalText):
            self.columnname = originalText
            self.tablename = tableDict['__default__']
            self.tableshortname = tableDict['__default__']
        else:
            text = originalText.split('.')
            self.columnname = text[1].strip()
            self.tableshortname = text[0].strip()
            self.tablename = tableDict[self.tableshortname]

    def __str__(self):
        return "ColumnName : \'" + \
               self.columnname + \
               '\' tableShortName : \'' + \
               self.tableshortname + \
               '\' tableName : \'' + \
               self.tablename + '\''



"""
class VariableName(object):


    def __init__(self, originalText, tableDict, varname=None):
        if varname is None:
            text = originalText.split(' ')
            self.variable = text[1]
            self.column = ColumnName(text[0].strip(), tableDict)
        else:
            self.variable = varname
            self.column = ColumnName(originalText, tableDict)


    def __str__(self):
        return 'VariableName : \'' + self.variable + '\' ' + str(self.column)
"""

class VariableName(ColumnName):

    def __init__(self, originalText, tableDict, varname=None):
        if varname is None:
            text = originalText.split(' ')
            super(VariableName,self).__init__(text[0].strip(), tableDict)
            self.variable = text[1]

        else:
            super(VariableName,self).__init__(originalText, tableDict)
            self.variable = varname

    def __str__(self):
        return 'VariableName : \'' + self.variable + '\' ' + super(VariableName,self).__str__()


class SelectSQLParser(object):
    """
    解析Select SQL语句
    """

    def __init__(self, originalSQL, sqlType):
        self.selectType = sqlType
        self.outputText = None


        tablesMatch = re.findall(r'from.+where', originalSQL)
        tables = re.sub(r'(from|where)', '', tablesMatch[0])
        tables = re.sub(r'\s+', ' ', tables)
        tables = tables.strip()
        self.sqlfrom = '\nFROM '+ tables
        self.tableDict = self.__tableDictInit(tables)
        self.varnames = self.__variableInit(originalSQL)
        self.sqlwhere = self.__sqlWhere(originalSQL) + ' ; '




    def __tableDictInit(self, originalText):
        tables = originalText.split(',')
        tableDict = {}

        if len(tables) == 1 and not ( ' ' in tables[0].strip() ):
            tableDict['__default__'] = tables[0].strip()
            tableDict[tables[0].strip()] = tables[0].strip()
            return tableDict

        for table in tables:
            tableitem = table.strip().split(' ')
            tableDict[tableitem[1]] = tableitem[0]

        return tableDict

    def __variableInit(self,originalSQL,):
        varnames = []
        cols = re.findall(r'select\s.+\sfrom',originalSQL)
        col = re.sub(r'(select|from)','',cols[0])

        if 'dbms alias' in originalSQL :
            variableMatch = re.findall(r'alias\s.+\ssql',originalSQL)
            variable = re.sub(r'(alias|sql)','',variableMatch[0])
            variable = variable.replace(' ','')
            variable = variable.strip()
            variables = variable.split(',')

            colMatch = re.findall(r'select\s.+\sfrom',originalSQL)
            column = re.sub(r'(select|from)','',colMatch[0])
            column = column.replace(' ','')
            column = column.strip()
            columns = column.split(',')

            if len(columns) != len(variables):
                self.outputText = SQLParseError[0]
            else:
                for i in range( len(columns)):
                    varname = VariableName(columns[i],self.tableDict,variables[i])
                    varnames.append(varname)

        else:
            textMatch = re.findall(r'select\s.+\sfrom',originalSQL)
            #print(textMatch)
            text = re.sub(r'(select|from)','',textMatch[0])
            text = re.sub(r'\s+', ' ', text)
            texts = text.split(',')
            for original in texts:
                varname = VariableName(original.strip(),self.tableDict)
                varnames.append(varname)

        return varnames

    def __sqlWhere(self,originalSQL):
        sqlWhereMatch = re.findall(r'where\s.+',originalSQL)
        trimVar = re.findall(r':\+\w+',sqlWhereMatch[0])
        sqlWhere = sqlWhereMatch[0]
        for var in trimVar:
            sqlWhere =  sqlWhere.replace(var , 'rtrim('+re.sub(r':\+','',var) + ')' )

        sqlWhere = sqlWhere.replace('where','\nWHERE')
        return sqlWhere

    def getText(self):
        if self.outputText != None:
            return self.outputText

        if self.selectType == 0 :
            # 0 代表"单变量Select"
            self.outputText = self.__typeZeroSQLGenerator()
        elif self.selectType == 1:
            # 1 代表"数组Select"
            self.outputText = self.__typeOneSQLGenerator()
        else:
            self.outputText = SQLParseError[3]


        return  self.outputText

    def __typeZeroSQLGenerator(self):
        defineText = '--变量定义部分\n'
        selectText = '\n--SQL改写部分\nSELECT '
        intoText  = '\nINTO　'
        isSingleTable = '__default__' in self.tableDict.keys()

        for variable in self.varnames:
            temptext = variable.variable + ' ' + \
                       variable.tablename  + '.' + \
                       variable.columnname + '%TYPE;\n'
            defineText = defineText + temptext

            if  isSingleTable :
                selectText = selectText + variable.columnname + ' , '
                intoText = intoText + variable.variable + ' , '
            else:
                selectText = selectText + variable.tableshortname +'.'+ variable.columnname + ' , '
                intoText = intoText + variable.variable + ' , '

        selectText = selectText.rstrip()
        selectText = selectText.rstrip(',')

        intoText = intoText.rstrip()
        intoText = intoText.rstrip(',')


        return defineText + selectText + intoText +self.sqlfrom + self.sqlwhere




    def __typeOneSQLGenerator(self):
        arrayDefineText = '--数组类型定义\n\n'
        defineText = '\n\n--变量定义\n\n'
        cursorText = '\n\n--游标定义\nCursor my_cursor Is\nSelect  '
        selectText = '\n\n--SQL改写\nSELECT '
        intoText  = '\nBULK COLLECT INTO　'
        isSingleTable = '__default__' in self.tableDict.keys()
        for variable in self.varnames:

            temptext = 'Type ' + variable.tablename+'_' + \
                       variable.columnname +'_array Is Table Of ' +\
                       variable.tablename+'.'+ \
                       variable.columnname + \
                       '%Type Index By Binary_Integer;\n'
            arrayDefineText = arrayDefineText + temptext

            temptext = variable.variable + ' ' +  variable.tablename+'_' + \
                       variable.columnname +'_array;\n'
            defineText = defineText + temptext

            if  isSingleTable :
                selectText = selectText + variable.columnname + ' , '
                cursorText = cursorText + variable.columnname + ' , '
                intoText = intoText + variable.variable + ' , '
            else:
                selectText = selectText + variable.tableshortname +'.'+ variable.columnname + ' , '
                cursorText = cursorText + variable.tableshortname +'.'+ variable.columnname + ' , '
                intoText = intoText + variable.variable + ' , '

        selectText = selectText.rstrip()
        selectText = selectText.rstrip(',')

        cursorText = cursorText.rstrip()
        cursorText = cursorText.rstrip(',')

        intoText = intoText.rstrip()
        intoText = intoText.rstrip(',')


        return arrayDefineText +  defineText+cursorText +self.sqlfrom + self.sqlwhere  + selectText + intoText +self.sqlfrom + self.sqlwhere



if __name__ == '__main__':
    pass