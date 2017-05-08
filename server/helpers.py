import sqlalchemy
import sqlalchemy.types as sa_Types
import models
from initdb import session, metadata
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from migrate.changeset import *

def format_user_data(dtable, data):
    """
    Given various length tuples, trim the id and leave the rest
    intact to display to the user.
    """
    content = {'columns': [s.column_name for s in dtable.columns]}
    content['columns'].append('Commands')
    content['rows'] = {}

    for i, _ in enumerate(data):
        ph = '{}'.format(i)
        content['rows'][ph] = {'cells': []}

        for cell in data[i][1:]:
            content['rows'][ph]['cells'].append(cell)
        content['rows'][ph]['id'] = data[i][0]
    return content
