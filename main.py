from flask import Flask, render_template

app = Flask(__name__)

def app_routes():
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/signup")
    def signup():
        return render_template("signup.html")
    
    @app.route("/login")
    def login():
        return render_template("login.html")
    
app_routes()

if __name__ == "__main__":
    app.run(debug=True)