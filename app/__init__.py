from flask import Flask

from app.views import configure_views



def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)


    configure_views(app)

    from app.services.views import sort_bp
    app.register_blueprint(sort_bp)

    from app.geo.views import geo_bp
    app.register_blueprint(geo_bp)

    return app

from app import views