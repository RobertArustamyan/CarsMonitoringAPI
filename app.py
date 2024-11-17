from flask import Flask
from DatabaseWork.workWdatabase import WorkWithDb
from blueprints.cars.cars import cars_bp
from blueprints.parts.parts import parts_bp

app = Flask(__name__)
app.register_blueprint(parts_bp, url_prefix='/parts')
app.register_blueprint(cars_bp, url_prefix='/cars')


if __name__ == "__main__":
    app.run(debug=False)

