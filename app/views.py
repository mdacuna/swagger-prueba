# views.py

from flask import render_template
from app import app

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
        return jsonify(spec.to_dict())

class BookResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        description = fields.Str()
        author = fields.Str()
        

class BookListResponseSchema(Schema):
        article_list = fields.List(fields.Nested(BookResponseSchema))

@app.route('/books')
def book():
    """Get List of Books
        ---
        get:
            description: Get List of Books
            responses:
                200:
                    description: Return a book list
                    content:
                        application/json:
                            schema: BookListResponseSchema
    """
    """Post List of Books
        ---
        post:
            description: Upload a Book
            responses:
                200:
                    description: Add a book to the list
                    content:
                        application/json:
                            schema: BookListResponseSchema
    """
    """Delete a Book from the list
        ---
        delete:
            description: Delete a Book
            responses:
                200:
                    description: Delete a book from the list
                    content:
                        application/json:
                            schema: BookListResponseSchema
    """

    books = [
        {
            'id': 1,
            'title': 'La hojarasca',
            'description': 'Good one',
            'author': 'Gabo'
        },
        {
            'id': 2,
            'title': 'El coronel no tiene quien le escriba',
            'description': 'Interesting',
            'author': 'Gabo'
        }
    ]

    return BookListResponseSchema().dump({'article_list':books})

with app.test_request_context():
    spec.path(view=book)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html',base_url='/docs')
    else:
        return send_from_directory('static',path)
