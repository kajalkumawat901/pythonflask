# from flask import Flask 

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "hello world!"

# @app.route("/harry")
# def harry():
#     return "hello harry!"

# app.run(debug=True)


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/about")
def harry():
    return render_template('about.html')
app.run(debug = True)

if __name__ == "__main__":
    app.run(debug=True)
