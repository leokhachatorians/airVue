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

import forms, models, helpers

schema_store = DTSchemaStoreSQL(session, engine)
data_engine = DTDataEngineSQL(session, engine, metadata)

@app.route('/get_sheet', methods=['POST'])
def get_sheet_data():
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

@app.route('/view_sheet/<sheet_name>')
def view_sheet(sheet_name):
    return render_template('view_sheet_vue.html')

@app.route('/')
def index():
    sheets = session.query(models.Sheets).filter_by(user_id=1).all()
    new_sheet_form = forms.NewSheetForm(request.form)
    delete_form = forms.DeleteTableForm(request.form)
    return render_template("index_vue.html", sheets=sheets,
            new_sheet_form=new_sheet_form, delete_form=delete_form)

@app.route('/example')
def example():
    return render_template('example.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
