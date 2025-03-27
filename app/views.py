from flask import request, render_template
from datetime import datetime
import platform

def inject_global_data():
    global_data = {
        'u_agent': request.headers.get('User-Agent'),
        'OS': platform.system(),
        'time': datetime.now()
    }
    return global_data

def configure_views(app):
    @app.context_processor
    def context_processor():
        return inject_global_data()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/main")
    def main():
        return render_template("main.html")