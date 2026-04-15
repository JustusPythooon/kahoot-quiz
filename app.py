from flask import Flask, render_template, request, redirect
import json, os, random

app = Flask(__name__)
DATA='quizzes.json'

def load():
    if not os.path.exists(DATA): return {}
    return json.load(open(DATA,'r',encoding='utf-8'))

def save(d): json.dump(d, open(DATA,'w',encoding='utf-8'), indent=2, ensure_ascii=False)

quizzes = load()
games = {}
avatars=['🧙‍♂️','🤖','🦊','🐯','🐸','🦄','🐲','🐼','🐶','🐱','🧸','🐧']

@app.route('/')
def step1(): return render_template('step_pin.html')

@app.route('/name', methods=['POST'])
def step2():
    return render_template('step_name.html', pin=request.form['pin'])

@app.route('/avatar', methods=['POST'])
def step3():
    return render_template('step_avatar.html', pin=request.form['pin'], name=request.form['name'], avatars=avatars)

@app.route('/join', methods=['POST'])
def join():
    pin,name,av=request.form['pin'],request.form['name'],request.form['avatar']
    if pin not in games: return 'Falsche PIN'
    games[pin]['players'][name]={'score':0,'avatar':av}
    return redirect(f'/lobby/{pin}/{name}')

@app.route('/lobby/<pin>/<name>')
def lobby(pin,name): return render_template('lobby.html', pin=pin, players=games[pin]['players'])

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST': quizzes[request.form['quiz']] = []; save(quizzes)
    return render_template('admin.html', quizzes=quizzes)

@app.route('/editor/<quiz>', methods=['GET','POST'])
def editor(quiz):
    if request.method=='POST': quizzes[quiz].append(dict(request.form)); save(quizzes)
    return render_template('editor.html', quiz=quiz, qs=quizzes[quiz])

@app.route('/host/<quiz>')
def host(quiz):
    pin=str(random.randint(100000,999999))
    games[pin]={'quiz':quiz,'players':{},'i':0}
    return render_template('host.html', pin=pin)

app.run(host='0.0.0.0',port=5000)
