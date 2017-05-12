import os
from flask import (
        Flask, request, session, g, redirect, url_for, abort,
        render_template, flash, current_app, jsonify
)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Table, MetaData
from initdb import session, metadata, engine
import sqlalchemy
from backend.dt_schema_store import DTSchemaStoreSQL
from backend.dt_data_engine import DTDataEngineSQL
from backend.excp.column_exceptions import DuplicateColumn

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI="postgresql://leo:password@localhost:5432/flask_air",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='blahlbahblah',
    USERNAME='admin',
    PASSWORD='admin'
))

app.config.from_envvar('AIR_SETTINGS', silent=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

import models, helpers

schema_store = DTSchemaStoreSQL(session, engine)
data_engine = DTDataEngineSQL(session, engine, metadata)

@app.route('/api/v1/user', methods=['POST'])
def create_user():
    pass

@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    pass

@app.route('/api/v1/user/<int:user_id>/sheets', methods=['GET'])
def get_user_sheets(user_id):
    sheets = []
    query = session.query(models.Sheets).filter_by(user_id=user_id).all()
    for sheet in query:
        sheets.append(
            {
                'name': sheet.sheet_name,
                'id': sheet.id
            }
        )
    return jsonify(sheets=sheets)

@app.route('/api/v1/user/<int:user_id>/sheets', methods=['POST'])
def create_new_sheet(user_id):
    dtable = schema_store.get_schema(table_name=request.json['sheet_name'])
    dtable.info['action'] = 'generate'
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(status=200)

@app.route('/api/v1/user/<int:user_id>/sheets/<int:sheet_id>', methods=['DELETE'])
def delete_sheet(user_id, sheet_id):
    dtable = schema_store.get_schema(table_id=sheet_id)
    dtable.info['action'] = 'drop'
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>', methods=['GET'])
def get_schema(sheet_id):
    dtable = schema_store.get_schema(table_id=sheet_id)
    return jsonify(schema=dtable.get_schema())

@app.route('/api/v1/sheet/<int:sheet_id>/update', methods=['POST'])
def update_sheet(sheet_id):
    dtable = schema_store.get_schema(table_id=sheet_id)
    dtable.change_table_name(request.json['new_sheet_name'])
    schema_store.set_schema(dtable)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>/contents', methods=['GET'])
def get_contents(sheet_id):
    dtable = schema_store.get_schema(table_id=sheet_id)
    handle = data_engine.create_handle(dtable)
    contents = helpers.format_user_data(dtable, handle.get_rows(dtable))
    inputs, cells = helpers.format_user_data_2(dtable, handle.get_rows(dtable))
    cols = inputs + ['Commands']
    return jsonify(columns=cols, cells=cells, inputs=inputs)

@app.route('/api/v1/sheet/<int:sheet_id>/columns', methods=['POST'])
def add_column(sheet_id):
    column_name = request.json['column_name']
    column_type = request.json['column_type']
    dtable = schema_store.get_schema(table_id=sheet_id)
    dtable.add_column(column_name, column_type)
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>/columns/<int:column_id>', methods=['PUT'])
def update_column(sheet_id, column_id):
    new_name = request.json['new_name']
    old_name = request.json['old_name']
    new_type = request.json['new_type']
    dtable = schema_store.get_schema(table_id=sheet_id)
    dtable.alter_column(old_name, new_name, new_type, column_id)
    schema_store.set_schema(dtable)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>/columns/<int:column_id>', methods=['DELETE'])
def delete_column(sheet_id, column_id):
    dtable = schema_store.get_schema(table_id=sheet_id)
    dtable.remove_column(column_id)
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>/entry', methods=['POST'])
def add_entry(sheet_id):
    values = request.json['values']
    dtable = schema_store.get_schema(table_id=sheet_id)
    handle = data_engine.create_handle(dtable)
    data = {'col_{}'.format(dtable.columns[i].column_id): values[i] for i, _ in enumerate(values)}
    handle.add_row(dtable, data)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>/entry/<int:row_id>', methods=['PUT'])
def update_entry(sheet_id, row_id):
    values = request.json['values']
    dtable = schema_store.get_schema(table_id=sheet_id)
    handle = data_engine.create_handle(dtable)
    handle.update_row(dtable, row_id, values)
    return jsonify(status=200)

@app.route('/api/v1/sheet/<int:sheet_id>/entry/<int:row_id>', methods=['DELETE'])
def delete_entry(sheet_id, row_id):
    dtable = schema_store.get_schema(table_id=sheet_id)
    handle = data_engine.create_handle(dtable)
    handle.delete_row(dtable, row_id)
    return jsonify(status=200)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
