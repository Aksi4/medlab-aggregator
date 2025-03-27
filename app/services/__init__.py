from flask import Blueprint

sort_bp = Blueprint("sort_bp", __name__, template_folder="templates")


from . import views
