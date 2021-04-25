from flask import Flask, render_template,request,redirect
import shelve, datetime

app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])
def mainPage():
    if request.method =='POST':
        text = request.form['content']
        if text=="":
            pass
        else:
            file = shelve.open("tasks.db")
            if len(file.keys())==0:
                Id = 1
            else:
                Id = max(list(map(lambda x:int(x), list(file.keys()))))+1
            file[str(Id)] = [text, str(datetime.datetime.now())]
            file.close()
        return redirect('/')
            
    elif request.method=="GET":
        file = shelve.open('tasks.db')
        task = list(file.items())
        file.close()
        check = len(task)==0
        return render_template("mainPage.html", tasks = task, check =  check)



@app.route("/delete/<string:Id>")
def delete(Id):
    file = shelve.open("tasks.db")
    if Id in file.keys():
        del file[Id]
    file.close()
    return redirect('/')

@app.route("/update/<string:Id>", methods = ["GET", "POST"])
def update(Id):
    if request.method=="GET":
        file = shelve.open("tasks.db")
        if Id in file.keys():
            text = file[Id][0]
            return render_template("update.html", text = text, id = Id)
        else:
            file.close()
            return redirect('/')
    elif request.method=="POST":
        file = shelve.open("tasks.db")
        file[Id] = [request.form['content'], file[Id][1]]
        file.close()
        return redirect('/')
app.run(debug=True)