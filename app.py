from flask import Flask, render_template, request, redirect
import random, json, os, time

app = Flask(__name__)
DATA_FILE='quizzes.json'

def load():
    if not os.path.exists(DATA_FILE): return {}
    return json.load(open(DATA_FILE,'r',encoding='utf-8'))

def save(d): json.dump(d, open(DATA_FILE,'w',encoding='utf-8'), indent=2, ensure_ascii=False)

quizzes = load()
games = {}
avatars=['🧙‍♂️','🧌','🤖','🦊','🐸','🐯','🐶','🐱','🦁','🐼','🐵','🐧','🦄','🐲','🐷','🐰','🐨','🦉']

@app.route('/')
def join(): return render_template('join.html', avatars=avatars)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        name=request.form['name']
        quizzes[name]=[]; save(quizzes)
        return redirect(f'/editor/{name}')
    return render_template('admin.html', quizzes=quizzes)

@app.route('/editor/<q>', methods=['GET','POST'])
def editor(q):
    if request.method=='POST':
        quizzes[q].append(dict(request.form))
        save(quizzes)
    return render_template('editor.html', quiz=q, questions=quizzes[q])

@app.route('/host/<q>')
def host(q):
    pin=str(random.randint(100000,999999))
    games[pin]={
      'quiz':q,'players':{},'i':0,'start':time.time()
    }
    return render_template('host.html',pin=pin,quiz=q)

@app.route('/join_game',methods=['POST'])
def join_game():
    pin=request.form['pin']
    if pin not in games: return 'Falsche PIN'
    name=request.form['name']; av=request.form['avatar']
    games[pin]['players'][name]={'score':0,'avatar':av}
    return redirect(f'/lobby/{pin}/{name}')

@app.route('/lobby/<pin>/<name>')
def lobby(pin,name):
    return render_template('lobby.html',pin=pin,players=games[pin]['players'])

@app.route('/question/<pin>/<name>')
def question(pin,name):
    g=games[pin]; q=quizzes[g['quiz']][g['i']]
    return render_template('question.html',q=q,pin=pin,name=name)

@app.route('/answer',methods=['POST'])
def answer():
    pin,name,ans=request.form['pin'],request.form['name'],request.form['ans']
    g=games[pin]; q=quizzes[g['quiz']][g['i']]
    if ans==q['answer']: g['players'][name]['score']+=100
    return redirect(f'/question/{pin}/{name}')

@app.route('/next/<pin>')
def nextq(pin): games[pin]['i']+=1; return 'OK'

@app.route('/scoreboard/<pin>')
def score(pin): return render_template('score.html',p=games[pin]['players'])

app.run(host='0.0.0.0',port=5000)
