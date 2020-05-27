# -*- coding: utf-8 -*-
from django.db import connection
import re
from io import StringIO
from django.conf import settings
import os


# this function get raw MySQL statement
def run_sql(sql):
    def load_data_from_sql(app, schema_editor):
        f = StringIO(sql)
        return _runsql(f)

    return load_data_from_sql


# this function get sql file
def run_sql_file(filename):
    def load_data_from_sql(app, schema_editor):
        filepath = os.path.join(settings.PROJECT_PATH, '../deploy/mysql/', filename)
        with open(filepath, 'rb') as f:
            return _runsql(f)

    return load_data_from_sql


# in this function content splits and checks line by line
def _runsql(f):
    with connection.cursor() as c:
        file_data = f.readlines()
        statement = ''
        delimiter = ';\n'
        for line in file_data:
            if re.findall('DELIMITER', line): # found delimiter
                if re.findall('^\s*DELIMITER\s+(\S+)\s*$', line):
                    delimiter = re.findall('^\s*DELIMITER\s+(\S+)\s*$', line)[0] + '\n'
                    continue
                else:
                    raise SyntaxError('Your usage of DELIMITER is not correct, go and fix it!')
            statement += line # add lines while not met lines with current delimiter
            if line.endswith(delimiter):
                if delimiter != ';\n':
                    statement = statement.replace(';', '; --').replace(delimiter, ';') # found delimiter, add dash symbols (or any symbols you want) for converting MySQL statements with multiply delimiters in SQL statement
                c.execute(statement) # execute current statement
                statement = '' # begin collect next statement