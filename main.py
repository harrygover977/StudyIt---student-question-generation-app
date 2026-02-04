from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager()

load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

login_manager.init_app(app)
login_manager.login_view = "signup"
login_manager.login_message = "Please sign up to access this page"
login_manager.login_message_category = "error"

def app_routes(app):
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (TypeError, ValueError):
            return None
    
    @app.route("/")
    @login_required
    def index():
        return render_template("index.html")
    
    @app.route("/upload", methods=["POST", "GET"])
    def upload():
        if request.method == "POST":
            file = request.files.get("notes")
            print(file)
        return redirect(url_for("index"))
    
    @app.route("/signup", methods=["POST", "GET"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
        
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                # Add flash message
                return redirect(url_for("login"))
            elif len(password) < 8:
                # add flash message
                return redirect(url_for("signup"))
            elif password != confirm_password:
                # add flash message
                return redirect(url_for("signup"))
            
            new_user = User(username=username,
                            password=generate_password_hash(password))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("index"))
            
        return render_template("signup.html")
    
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            
            user = User.query.filter_by(username=username).first()
            
            if not user or not check_password_hash(user.password, password):
                # add flash message
                return redirect(url_for("signup"))
            
            login_user(user)
            print(user.is_authenticated)
            return redirect(url_for("index"))
        
        return render_template("login.html")
    
    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))
    
app_routes(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)