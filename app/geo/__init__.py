from flask import Blueprint

geo_bp = Blueprint("geo_bp", __name__, template_folder="templates")


from . import views
