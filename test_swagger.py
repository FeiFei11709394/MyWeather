#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : test_swagger.py
# @Description:  test_swagger


from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api_app = Api(app=app)
name_space = api_app.namespace(name='helloworld',
                               description='The helloworld APIs EndPoint.')
from flask_restplus import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name')

@name_space.route('/')
class HelloWorld(Resource):


    def get(self):
        return {
            'status': 'you get a request.'
        }

    @api_app.param(parser)
    @api_app.expect({"test": 1})
    def post(self):
        return {
            'status': 'you post a request.'
        }


if __name__ == "__main__":
    app.run(debug=True)