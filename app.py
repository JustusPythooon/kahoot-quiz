from flask import Flask, render_template, request, redirect
import json, os, random, time
app=Flask(__name__)
DATA='quizzes.json'

def load():
    if not os.path.exists(DATA): return {}
    with open(DATA,'r',encoding='utf-8') as f: return json.load(f)

def save(d):
    with open(DATA,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False)

quizzes=load(); games={}
avatars=['🧙‍♂️','🤖','🦊','🐯','🐸','🦄','🐲','🐼','🐶','🐱']

@app.route('/')
def pin(): return render_template('pin.html')

@app.route('/name',methods=['POST'])
def name(): return render_template('name.html',pin=request.form['pin'])

@app.route('/avatar',methods=['POST'])
def avatar(): return render_template('avatar.html',pin=request.form['pin'],name=request.form['name'],avatars=avatars)

@app.route('/join',methods=['POST'])
def join():
    pin,name,av=request.form['pin'],request.form['name'],request.form['avatar']
    if pin not in games: return 'Falsche PIN'
    games[pin]['players'][name]={'avatar':av,'score':0}
    return redirect(f'/lobby/{pin}/{name}')

@app.route('/lobby/<pin>/<name>')
def lobby(pin,name): return render_template('lobby.html',pin=pin,players=games[pin]['players'])

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST': quizzes[request.form['quiz']]=[]; save(quizzes)
    return render_template('admin.html',quizzes=quizzes)

@app.route('/editor/<quiz>',methods=['GET','POST'])
def editor(quiz):
    if request.method=='POST': quizzes[quiz].append(dict(request.form)); save(quizzes)
    return render_template('editor.html',quiz=quiz,questions=quizzes[quiz])

@app.route('/host/<quiz>')
def host(quiz):
    pin=str(random.randint(100000,999999))
    games[pin]={'quiz':quiz,'players':{},'q':0}
    return render_template('host.html',pin=pin)

@app.route('/question/<pin>/<name>')
def question(pin,name):
    q=quizzes[games[pin]['quiz']][games[pin]['q']]
    return render_template('question.html',q=q,pin=pin,name=name)

@app.route('/answer',methods=['POST'])
def answer():
    pin,name,ans=request.form['pin'],request.form['name'],request.form['ans']
    q=quizzes[games[pin]['quiz']][games[pin]['q']]
    if ans==q['correct']: games[pin]['players'][name]['score']+=100
    return redirect(f'/score/{pin}')

@app.route('/score/<pin>')
def score(pin):
    ranking=sorted(games[pin]['players'].items(), key=lambda x:x[1]['score'], reverse=True)
    return render_template('score.html',ranking=ranking)

app.run(host='0.0.0.0',port=5000)
