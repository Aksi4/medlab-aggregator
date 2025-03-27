from flask import request, jsonify, render_template
from database import get_db
from . import geo_bp
from database.models import Lab
from .utils import get_coordinates, haversine, get_city_and_region

@geo_bp.route("/map", methods=["GET"])
def map():
    return render_template("map.html")


@geo_bp.route("/labs_nearby", methods=["POST"])
def labs_nearby():
    data = request.json
    user_lat = data.get("latitude")
    user_lon = data.get("longitude")

    if not user_lat or not user_lon:
        print(f"Помилка: координати не передані. user_lat: {user_lat}, user_lon: {user_lon}")
        return jsonify({"error": "Координати не передані"}), 400

    db = next(get_db())

    try:
        labs = db.query(Lab).all()
        if not labs:
            print("Немає лабораторій у базі даних.")
            return jsonify({"error": "Лабораторії не знайдено в базі даних"}), 404

        city, region = get_city_and_region(user_lat, user_lon)

        if not city and not region:
            print("Не вдалося визначити місто чи регіон. Використовуємо Івано-Франківськ.")
            city = "Івано-Франківськ"
            region = "Івано-Франківська область"

        lab_distances = []
        for lab in labs:
            coordinates_list = get_coordinates(lab.lab_name, city, region)
            if coordinates_list:
                for lat, lon in coordinates_list:
                    distance = haversine(user_lat, user_lon, lat, lon)


                    icon_path = f"/static/images/lab/{lab.lab_name.lower().replace(' ', '')}.jpg"

                    lab_distances.append({
                        "lab_name": lab.lab_name,
                        "distance": distance,
                        "coordinates": (lat, lon),
                        "icon": icon_path
                    })
            else:
                print(f"Не вдалося отримати координати для лабораторії {lab.lab_name}")

        if not lab_distances:
            print("Не вдалося обчислити відстань для жодної лабораторії.")
            return jsonify({"error": "Не вдалося обчислити відстань для лабораторій"}), 404

        # сортуємо лабораторії за відстанню та вибираємо XX(50) найближчих
        closest_labs = sorted(lab_distances, key=lambda x: x["distance"])[:50]

        print(f"Знайдено {len(closest_labs)} найближчих лабораторій.")
        return jsonify(closest_labs)

    except Exception as e:
        print(f"Помилка при отриманні лабораторій: {e}")
        return jsonify({"error": "Сталася помилка при отриманні лабораторій"}), 500

# тест
# @geo_bp.route("/test_coordinates", methods=["GET"])
# def test_coordinates():
#     lab_name = "Сінево"
#     coordinates = get_coordinates(lab_name)
#
#     if coordinates:
#         return jsonify({"lab_name": lab_name, "coordinates": coordinates})
#     else:
#         return jsonify({"lab_name": lab_name, "error": "Координати не знайдені"})


