from flask import Blueprint, request, jsonify
from DatabaseWork.workWdatabase import WorkWithDb


parts_bp = Blueprint('parts', __name__)

@parts_bp.route('/get_parts', methods=['GET'])
def get_parts():
    db = WorkWithDb('Databases/parts.db')
    db.connect()
    try:
        parts = db.fetch_all('SELECT * FROM parts')

        parts_list = [dict(part) for part in parts]

        return jsonify(parts_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()

@parts_bp.route('/get_part', methods=['GET'])
def get_part():
    db = WorkWithDb('Databases/parts.db')
    db.connect()
    try:
        part_id = request.args.get('id')

        # Ensure part_id is valid
        if not part_id or not part_id.isdigit():
            return jsonify({'error': 'Invalid or missing id parameter'}), 400

        part = db.fetch_one('SELECT * FROM parts WHERE id = ?', (int(part_id),))

        if not part:
            return jsonify({'error': f'Part with id {part_id} not found'}), 404

        # Convert the result to a dictionary if column names are available
        columns = ['id', 'name', 'price']
        part_dict = dict(zip(columns, part))

        return jsonify(part_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()


@parts_bp.route('/add_part', methods=['POST'])
def add_part():
    db = WorkWithDb('Databases/parts.db')
    db.connect()
    try:
        part = request.get_json()
        db.execute_query('INSERT INTO parts (name, price) VALUES (?, ?)', (part['name'], part['price']))

        return jsonify({'message': 'Part added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()

@parts_bp.route('/update_part/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    db = WorkWithDb('Databases/parts.db')
    db.connect()
    try:
        part = request.get_json()
        db.execute_query('UPDATE parts SET name = ?, price = ? WHERE id = ?', (part['name'], part['price'], part_id))

        return jsonify({'message': 'Part updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()
@parts_bp.route('/delete_part/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    db = WorkWithDb('Databases/parts.db')
    db.connect()
    try:
        db.execute_query('DELETE FROM parts WHERE id = ?', (part_id,))

        return jsonify({'message': 'Part deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.commit_and_close()









"""
/get_parts endpoint test.
curl -X GET http://127.0.0.1:5000/parts/get_parts

[
  {
    "id": 1,
    "name": "Right Front Door",
    "price": 300.0
  },
  {
    "id": 2,
    "name": "Left Back Door",
    "price": 300.0
  },
  ...
]
/ get_part endpoint test.
curl -X GET "http://127.0.0.1:5000/parts/get_part?id=1"

{
  "id": 1,
  "name": "Right Front Door",
  "price": 300.0
}
/ add_part endpoint test.
curl -X POST http://127.0.0.1:5000/parts/add_part -H "Content-Type: application/json" -d '{"name": "Right Front Door", "price": 350}'
{
  "message": "Part added successfully"
}

/update_part endpoint test.
curl -X PUT http://127.0.0.1:5000/parts/update_part/1 \
-H "Content-Type: application/json" \
-d '{"name": "Left Front Door Updated", "price": 500}'

{
  "message": "Part updated successfully"
}
/delete_part endpoint test.
curl -X DELETE http://127.0.0.1:5000/parts/delete_part/8

{
  "message": "Part deleted successfully"
}


"""

