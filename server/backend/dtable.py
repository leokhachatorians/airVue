import pprint
from .dt_column import DTColumn
from .excp.column_exceptions import DuplicateColumn

class DTable():
    """Container for a users table

    Sole purpose of the DTable class is to be a bridge between the database and
    the user. Whenever the user wishes to modify their table in any matter, it
    first is modified here. The DTable will then be consumed by the 'DT Schema Store'
    which is in charge of actually modifying the meta-schema of the table in the
    actual database.
    """
    def __init__(self, name, id_=None, columns=[]):
        self.name = name
        self.id_ = id_
        self.columns = columns
        self._set_table_info()

    def add_column(self, name, type_):
        try:
            self.info['columns'][name]
            return False
            #raise DuplicateColumn(
            #    self.id_, self.table_info['columns'][name].column_id, name)
        except KeyError:
            self.info['modifications']['name'] = name
            self.info['modifications']['type'] = type_
            self.info['action'] = 'add'
            return True

    def alter_column(self, old_name, new_name, new_type, col_id):
        try:
            self.info['columns'][old_name]
            self.info['modifications']['name'] = new_name
            self.info['modifications']['type'] = new_type
            self.info['modifications']['id'] = col_id
            self.info['action'] = 'alter'
            return True
        except KeyError:
            return False

    def remove_column(self, name, id_):
        try:
            self.info['columns'][name]
            self.info['modifications']['id'] = id_
            self.info['action'] = 'remove'
            return True
        except KeyError:
            return False

    def change_table_name(self, name):
        self.info['modifications']['name'] = name
        self.info['action'] = 'change table name'
        return True

    def _set_table_info(self):
        """Sets up the internal dictionary to be consumed

        The 'info' dictionary is essentially the vehicle used to
        transport the information held by the DTable to 'DT Schema Store'.
        It contains basic information about what table to operate on, as well
        as what columns need to be altered, deleted, or created.
        """

        self.info = {
            'table_name': self.name,
            'table_id': self.id_,
            'columns': {},
            'action': '',
            'modifications': {
                'name': None,
                'type': None,
                'id': None,
            }
        }
        for column in self.columns:
            self.info['columns'][column.column_name] = column

    def get_schema(self):
        schema = []
        for c in self.columns:
            schema.append(
                {
                    'name': c.column_name,
                    'type': c.column_type,
                    'id': c.column_id,
                }
            )
        return schema

