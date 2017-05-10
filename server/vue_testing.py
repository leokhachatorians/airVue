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

@app.route('/get_sheet', methods=['POST'])
def get_sheet():
    id_ = request.json['id']
    sheet = session.query(models.Sheets).filter_by(id=id_).first()
    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)
    handle = data_engine.create_handle(dtable)
    contents = handle.get_rows(dtable)
    contents = helpers.format_user_data(dtable, contents)
    contents['sheet_info'] = {
            'name': sheet.sheet_name,
            'id': sheet.id
    }
    return jsonify(contents)

@app.route('/edit_sheet_name', methods=['POST'])
def edit_sheet_name():
    sheet_id = request.json['sheet_id']
    new_table_name = request.json['new_sheet_name']
    dtable = schema_store.get_schema('', sheet_id)
    dtable.change_table_name(new_table_name)
    schema_store.set_schema(dtable)
    return jsonify(status=200)

@app.route('/get_modify_sheet', methods=['POST'])
def get_modify_sheet():
    id_ = request.json['id']
    sheet = session.query(models.Sheets).filter_by(id=id_).first()
    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)
    contents = {}
    contents['sheet_name'] = sheet.sheet_name
    contents['schema'] = []
    for i, column in enumerate(dtable.columns):
        contents['schema'].append(
                {'name': column.column_name,
                'type': column.column_type,
                'id': column.column_id,
                'num': i + 1})
    return jsonify(contents)

@app.route('/delete_column', methods=['POST'])
def delete_column():
    sheet_id = request.json['sheet_id']
    column_name = request.json['column_name']
    column_id = request.json['column_id']
    dtable = schema_store.get_schema('', sheet_id)
    dtable.remove_column(column_name, column_id)
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(status=200)

@app.route('/alter_column', methods=['POST'])
def alter_column():
    sheet_id = request.json['sheet_id']
    new_name = request.json['new_name']
    old_name = request.json['old_name']
    new_type = request.json['new_type']
    col_id = request.json['col_id']
    dtable = schema_store.get_schema('', sheet_id)
    dtable.alter_column(old_name, new_name, new_type, col_id)
    schema_store.set_schema(dtable)
    return jsonify(status=200)

@app.route('/add_column', methods=['POST'])
def add_column():
    sheet_id = request.json['sheet_id']
    column_name = request.json['column_name']
    column_type = request.json['column_type']
    dtable = schema_store.get_schema('', sheet_id)
    dtable.add_column(column_name, column_type)
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(status=200)

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    sheet = session.query(models.Sheets).filter_by(id=data['sheet_id']).first()

    dtable = schema_store.get_schema(sheet.sheet_name, sheet.id)
    handle = data_engine.create_handle(dtable)
    data = {'col_{}'.format(dtable.columns[i].column_id): data['values'][i] for i, _ in enumerate(data['values'])}
    handle.add_row(dtable, data)

    return jsonify(status=200,
            table_id=sheet.id)

@app.route('/add_sheet', methods=['POST'])
def add_sheet():
    data = request.json
    dtable = schema_store.get_schema(data['sheet_name'])
    dtable.info['action'] = 'generate'
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)

    return jsonify(
            status=200,
            new_table=data['sheet_name'])

@app.route('/delete_sheet', methods=['POST'])
def delete_sheet():
    id_ = request.json['id']
    dtable = schema_store.get_schema('_', id_)
    dtable.info['action'] = 'drop'
    schema_store.set_schema(dtable)
    data_engine.set_schema(dtable)
    return jsonify(
            status=200,
            dropped=id_)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    data = request.json
    dtable = schema_store.get_schema('_', data['sheet_id'])

    handle = data_engine.create_handle(dtable)
    handle.delete_row(dtable, data['row_id'])

    return jsonify(
            status=200,
            sheet_id=data['sheet_id'],
            deleted_row_id=data['row_id'])

@app.route('/modify_data', methods=['POST'])
def modify_data():
    data = request.json
    dtable = schema_store.get_schema('_', data['sheet_id'])

    handle = data_engine.create_handle(dtable)
    handle.update_row(dtable, data['row_id'], data['values'])

    return jsonify(
            status=200,
            sheet_id=data['sheet_id'],
            modified_row_id=data['row_id'])

@app.route('/get_sheets')
def get_sheets():
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    contents = {'sheets': []}
    for sheet in sheets:
        d = {
            'name': sheet.sheet_name,
            'id': sheet.id
        }
        contents['sheets'].append(d)
    return jsonify(contents)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
