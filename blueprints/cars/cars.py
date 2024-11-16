from flask import Blueprint, request, jsonify
from DatabaseWork.workWdatabase import WorkWithDb

cars_bp = Blueprint('cars', __name__)

@cars_bp.route('get_cars', methods=['GET'])
def get_cars():
    db = WorkWithDb('Databases/cars.db')
    db.connect()
    try:
        cars = db.fetch_all('SELECT * FROM cars')

        cars_list = [dict(car) for car in cars]

        return jsonify(cars_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()

@cars_bp.route('/get_car', methods=['GET'])
def get_car():
    db = WorkWithDb('Databases/cars.db')
    db.connect()
    try:
        car_id = request.args.get('id')

        # Ensure car_id is valid
        if not car_id or not car_id.isdigit():
            return jsonify({'error': 'Invalid or missing id parameter'}), 400

        car = db.fetch_one('SELECT * FROM cars WHERE id = ?', (int(car_id),))

        if not car:
            return jsonify({'error': f'Car with id {car_id} not found'}), 404

        # Convert the result to a dictionary if column names are available
        car_dict = dict(car)

        return jsonify(car_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()

@cars_bp.route('/add_car', methods=['POST'])
def add_car():
    db = WorkWithDb('Databases/cars.db')
    db.connect()
    try:
        car = request.get_json()

        parts = car['parts'].split(',')

        parts_db = WorkWithDb('Databases/parts.db')
        parts_db.connect()

        total_price = 0
        for part_id in parts:
            part = parts_db.fetch_one('SELECT price FROM parts WHERE id = ?', (part_id,))
            if part:
                total_price += part['price']
            else:
                raise Exception(f"Part with ID {part_id} not found")

        parts_db.commit_and_close()

        counted_total = total_price + car.get('profit', 0)  # You can adjust based on your profit logic

        db.execute_query('''
            INSERT INTO cars (name, parts, profit, image, total) 
            VALUES (?, ?, ?, ?, ?)
        ''', (car['name'], car['parts'], car['profit'], car['image'], counted_total))

        db.commit_and_close()

        return jsonify({'message': 'Car added successfully', 'total': counted_total})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()

@cars_bp.route('/update_car', methods=['PUT'])
def update_car():
    db = WorkWithDb('Databases/cars.db')
    db.connect()
    try:
        car_id = request.args.get('id')
        car = request.get_json()

        parts = car['parts'].split(',')

        parts_db = WorkWithDb('Databases/parts.db')
        parts_db.connect()

        total_price = 0
        for part_id in parts:
            part = parts_db.fetch_one('SELECT price FROM parts WHERE id = ?', (part_id,))
            if part:
                total_price += part['price']
            else:
                raise Exception(f"Part with ID {part_id} not found")

        parts_db.commit_and_close()

        counted_total = total_price + car.get('profit', 0)  # You can adjust based on your profit logic

        db.execute_query('''
            UPDATE cars SET name = ?, parts = ?, profit = ?, image = ?, total = ?
            WHERE id = ?
        ''', (car['name'], car['parts'], car['profit'], car['image'], counted_total, car_id))

        db.commit_and_close()

        return jsonify({'message': 'Car updated successfully', 'total': counted_total})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()

@cars_bp.route('/delete_car', methods=['DELETE'])
def delete_car():
    db = WorkWithDb('Databases/cars.db')
    db.connect()
    try:
        car_id = request.args.get('id')

        db.execute_query('DELETE FROM cars WHERE id = ?', (car_id,))

        db.commit_and_close()

        return jsonify({'message': 'Car deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()






"""
----------------------

/get_cars endpoint test.
curl -X GET http://127.0.0.1:5000/cars/get_cars
[
  {
    "id": 1,
    "image": "base64encodedimage...",
    "name": "BMW X5",
    "parts": "1,2,3,7",
    "profit": 500.0,
    "total": 2200.0
  },
  {
    "id": 2,
    "image": "base64encodedimage...",
    "name": "Mercedes 222",
    "parts": "1,5,2",
    "profit": 250.0,
    "total": 1550.0
  },
  {
    "id": 3,
    "image": "base64encodedimage...",
    "name": "Porsche 911",
    "parts": "5,3",
    "profit": 100.0,
    "total": 900.0
  }
]


----------------------
/get_car endpoint test.
curl -X GET http://127.0.0.1:5000/cars/get_car?id=1
{
  "id": 1,
  "image": "base64encodedimage...",
  "name": "BMW X5",
  "parts": "1,2,3,7",
  "profit": 500.0,
  "total": 2200.0
}
----------------------
/ add_car endpoint test.
curl -X POST http://127.0.0.1:5000/cars/add_car -H "Content-Type: application/json" -d '{
    "name": "Mercedes 222",
    "parts": "1,5,2", 
    "profit": 250,
    "image": "base64encodedimage..."
}'
{
  "message": "Car added successfully",
  "total": 1550.0
}
----------------------
/update_car endpoint test.

curl -X PUT http://127.0.0.1:5000/cars/update_car?id=4 -H "Content-Type: application/json" -d '{
    "name": "Mercedes 212",
    "parts": "1,2,4", 
    "profit": 600,
    "image": "updatedbase64encodedimage..."
}'
{
  "message": "Car updated successfully",
  "total": 1900.0
}
----------------------
/delete_car endpoint test.

curl -X DELETE http://127.0.0.1:5000/cars/delete_car?id=5
{
  "message": "Car deleted successfully"
}

"""

