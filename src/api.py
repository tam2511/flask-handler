from random import randint

from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields

test_input = ''
status = 'Empty'
error = ''


def create_app():
    app = Flask('edges')

    api = Api(app, version='1.0', title='Simple task handler', doc='/api/', prefix='/api/')
    CORS(app)
    namespace = api.namespace('')

    progress_response = api.model('ProgressResponse', {
        'current': fields.Integer,
        'all': fields.Integer
    })

    task_input = api.model('TaskInput', {
        'test_input': fields.String
    })

    task_info = api.model('TaskInfo', {
        'test_input': fields.String,
        'status': fields.String,
        'error': fields.String
    })

    @namespace.route('/setup')
    class Setup(Resource):
        @namespace.doc('TaskSetup')
        @namespace.expect(task_input)
        def post(self):
            # Do something
            global test_input, status
            status = 'Ready'
            test_input = api.payload['test_input']
            return 200

    @namespace.route('/info')
    class Info(Resource):
        @namespace.doc('TaskInfo')
        @namespace.marshal_with(task_info)
        def get(self):
            # Do something
            global test_input, status
            return {
                       'test_input': test_input,
                       'status': status,
                       'error': '-',
                   }, 200

    @namespace.route('/start')
    class Start(Resource):
        @namespace.doc('Start')
        def post(self):
            # Do something
            global test_input, status
            status = 'Active'
            test_input = test_input + ' : started'
            return 200

    @namespace.route('/stop')
    class Stop(Resource):
        @namespace.doc('Stop')
        def post(self):
            # Do something
            global test_input, status
            status = 'Empty'
            test_input = ''
            return 200

    @namespace.route('/pause')
    class Pause(Resource):
        @namespace.doc('Pause')
        def post(self):
            # Do something
            global test_input, status
            status = 'Paused'
            test_input = test_input + ' : pause'
            return 200

    @namespace.route('/progress')
    class Progress(Resource):
        @namespace.doc('Progress')
        @namespace.marshal_with(progress_response)
        def get(self):
            # Do something
            return {
                       'current': randint(0, 100),
                       'all': 100
                   }, 200

    return app


if __name__ == '__main__':
    create_app().run(port=5002, debug=False)
