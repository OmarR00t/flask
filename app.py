from flask import Flask , render_template
app = Flask(__name__)
counter = 0


@app.route('/')
def hello():
    return "Hello word!! ,if you looking for how many visit this websit write in URL /counter/ to see your number!!,,  if you looking our website type in url /home/"

@app.route('/counter/')
def how():
    global counter
    counter += 1
    return str (counter) 

@app.route('/home/')
def homepage():
        return render_template("hello.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')