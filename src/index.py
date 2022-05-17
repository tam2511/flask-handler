from flask import render_template, Response, request
import time
import requests

from src.api import create_app

host = 'http://127.0.0.1'
port = '5002'
progress_timeout = 0.5

last_action = ''

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_action
    if request.method == 'POST':
        action = request.form['submit_button']
        if action == 'Setup':
            info = requests.get('/'.join([host + ':' + port, 'api', 'info'])).json()
            if 'test_input' in request.form and info['status'] not in ['Active', 'Paused']:
                requests.post('/'.join([host + ':' + port, 'api', 'setup']), json={
                    'test_input': request.form['test_input']
                })
        if action == 'Start' and last_action != 'Start':
            requests.post('/'.join([host + ':' + port, 'api', 'start']))
        if action == 'Stop' and last_action != 'Stop':
            requests.post('/'.join([host + ':' + port, 'api', 'stop']))
        if action == 'Pause' and last_action != 'Pause':
            requests.post('/'.join([host + ':' + port, 'api', 'pause']))
        last_action = action
    elif request.method == 'GET':
        return render_template('index.html', info=requests.get('/'.join([host + ':' + port, 'api', 'info'])).json())
    return render_template('index.html', info=requests.get('/'.join([host + ':' + port, 'api', 'info'])).json())


@app.route('/progress')
def progress():
    def generate():
        while True:
            response = requests.get('/'.join([host + ':' + port, 'api', 'progress'])).json()
            precentage = response['current'] / response['all'] * 100
            yield "data:" + '{:.1f}'.format(precentage) + "\n\n"
            time.sleep(progress_timeout)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(port=5002, debug=False)