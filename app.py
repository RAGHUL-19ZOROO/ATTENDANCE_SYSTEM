from flask import Flask, render_template
from routes.REP_AUTH_ROUTES import REP_auth
from routes.REP_DASH_ROUTES import rep_dash_bp
app=Flask(__name__)

app.register_blueprint(REP_auth)
app.register_blueprint(rep_dash_bp)
    
@app.route("/")
def index():
    return render_template('HOME_PAGE.html')
@app.route("/replogin")
def replogin():
    return render_template("REP_LOGIN.html")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",data="Welcome to the dashboard!")


if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)  