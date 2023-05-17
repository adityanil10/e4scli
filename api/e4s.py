from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///modules.sqlite3'  # Use any database URI here
db = SQLAlchemy(app)

class modules1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(10))


with app.app_context():
    db.create_all() 


@app.route('/')
def home():
    return "You have reached the homepage"


#POST /smi/reset - Reset the E4S platform 
@app.route('/smi/reset')
def reset():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return jsonify({'message' : 'Reset the e4s platform.'})

#POST /smi/reset/{module_id} - Reset a specific module identified by its ID 
@app.route('/smi/reset/<int:module_id>', methods =['POST'])
def reset_module(module_id):
    delete_module(module_id)
    return jsonify({'message':f'Resetting module {module_id}'})



#GET-smi/modules ==> get a list of all modules in e4s backplane
@app.route('/smi/modules', methods=['GET'])
def get_modules():
    all_modules = modules1.query.all()
    item_list = []
    for item in all_modules:
        item_list.append(item.name)
    return jsonify({'Modules': item_list})


#GET /smi/modules/{module_id} - Get information about a specific module identified by its ID 
@app.route('/smi/modules/<int:module_id>', methods=['GET'])
def get_module_info(module_id):
    item = modules1.query.get(module_id)
    if item:
        return jsonify({
            'id': item.id,
            'name': item.name
        })
    else:
        return jsonify({'message': 'Module not found'})



#GET /smi/modules/{module_id}/settings - Get the current settings for a specific module
@app.route('/smi/modules/<int:module_id>/settings', methods=['GET'])
def get_module_settings(module_id):
    item = modules1.query.get(module_id)
    if item:
        return jsonify({'message': f'Settings of module {module_id}'})
    else:
        return jsonify({'message': 'Module not found'})
    
@app.route('/smi/auth/<int:module_id>/<string:password>', methods=['GET'])
def auth(module_id, password):
    item = modules1.query.get(module_id)
    if item:
        module_pass = item.password
        if module_pass == password:
            return jsonify({'message': f'Authentication of module {module_id} successful.'})
        else:
            return jsonify({'message': f'Authenication failed.'})
    else:
        return jsonify({'message': 'Module not found'})


#PUT /smi/modules/{module_id}/settings - Update the settings for a specific module 
@app.route('/smi/modules/<int:module_id>/settings', methods=['PUT'])
def update_module_settings(module_id):
    item = modules1.query.get(module_id)
    if item:
        return jsonify({'message': f'Settings of module {module_id} updated'})
    else:
        return jsonify({'message': 'Module not found'})
    
#POST /smi/watchdog/{module_id} - Check the status of the watchdog for a specific module 
@app.route('/smi/watchdog/<int:module_id>', methods=['GET'])
def watchdog_module(module_id):
    item = modules1.query.get(module_id)
    if item:
        return jsonify({'message': f'Status of watchdog of module {module_id}'})
    else:
        return jsonify({'message': 'Module not found'})


#POST /smi/housekeeping/power/<module_id> - Control the power supply of the E4S platform modules
@app.route('/smi/housekeeping/power/on/<int:module_id>', methods = ['POST'])
def housekeeping_power_on(module_id):
    item = modules1.query.get(module_id)
    if item:
        #data = request.get_json()
        return jsonify({'message': f'Module {module_id} on'})
    else:
        return jsonify({'message': 'Module not found'})
    
@app.route('/smi/housekeeping/power/off/<int:module_id>', methods = ['POST'])
def housekeeping_power_off(module_id):
    item = modules1.query.get(module_id)
    if item:
        #data = request.get_json()
        return jsonify({'message': f'Module {module_id} off'})
        # if data == 'on':
        #     return jsonify({'message': f'Turned on module with id {module_id}'})
        # elif data == 'off':
        #     return jsonify({'message': f'Turned off module with id {module_id}'})
        # else:
        #     return jsonify({'message': f'Operation cannot be performed.'})
    else:
        return jsonify({'message': 'Module not found'})


#POST /smi/housekeeping/other - Control other housekeeping functions on the E4S platform
@app.route('/smi/housekeeping/other', methods = ['POST'])
def housekeeping_other():
    return jsonify({'message':'Control other housekeeping functions on the E4S platform '})

#POST /smi/modules - create a new module 
@app.route('/smi/modules', methods=['POST'])
def create_module():
    data = request.get_json()
    newmodule = modules1(name=data['name'], password=data['password'])  
    db.session.add(newmodule)
    db.session.commit()
    return jsonify({'message': 'Module created successfully'})


#GET /smi/modules/{module_id} - Delete a specific module identified by its ID
@app.route('/smi/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = modules1.query.get(module_id)
    if module:
        db.session.delete(module)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'message': 'Item not found'})


# updating module info
@app.route('/smi/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    data = request.get_json()
    item = modules1.query.get(module_id)
    item.name = data['name'] 
    item.password = data['password']
    db.session.commit()
    return jsonify({'message': 'Module updated successfully'})

@app.route('/smi/alerts/<string:alert>', methods=['POST'])
def alerts(alert):
    return jsonify({'message': f'Alert notification {alert} sent'})


if __name__ == "__main__":
    app.run(debug = True)
