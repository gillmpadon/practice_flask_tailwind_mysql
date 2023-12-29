from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

# MySQL configurations
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',  # Often 'localhost' or '127.0.0.1'
    'database': 'mydb',
}

@app.route('/')
def hello():
    from_id = request.args.get('from_id',default=0, type=int)
    to_id = request.args.get('to_id',default=0,  type=int)
    emp_id = request.args.get('emp_id',default=0,  type=int)
    where_conditions = []

    if emp_id:
        where_conditions.append(f"emp.idemployees = {emp_id}")
    else:
        if from_id or to_id:
            if from_id and to_id:
                where_conditions.append(f"emp.idemployees >= {from_id} AND emp.idemployees <= {to_id}")
            elif from_id:
                where_conditions.append(f"emp.idemployees >= {from_id}")
            elif to_id:
                where_conditions.append(f"emp.idemployees <= {to_id}")

    where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""


    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(f"SELECT skemp.employees_idemployees, CONCAT(emp.last_name, ' ', emp.first_name) AS name, ski.skill_type, ski.idskills, skemp.skill_level, emp.last_updated FROM skills_has_employees skemp INNER JOIN employees emp ON skemp.employees_idemployees = emp.idemployees INNER JOIN skills ski ON ski.idskills = skemp.skills_idskills {where_clause}")
    data = cursor.fetchall()  # Fetch all rows
    cursor.close()
    connection.close()
    
    # Prepare JSON response
    results = []
    for row in data:
        result = {
            'employees_id': row[0],
            'name': row[1],
            'skill_type': row[2],
            'skill_id': row[3],
            'skill_level': row[4],
            'last_updated': row[5].isoformat() if row[5] else None  # Convert datetime to ISO format
        }
        results.append(result)

    return jsonify({'data': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
