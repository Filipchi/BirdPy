from flask import Flask, render_template, jsonify, request, url_for, redirect

app = Flask(__name__)

from birds import birds

@app.route('/')
def home():
    data = {
        'title': 'Bird Python',
        'description': 'Welcome to BirdPy' 
    }
    return render_template('home.html', data=data)

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/about')
def about():
    return render_template('about.html')
# ---------------------------------------------------------------------------------
@app.route('/birds')
def getbirds():
    return jsonify(birds)

# Obtener un elemento
@app.route('/birds/<string:bird_name>')
def getbird(bird_name):
    birdFound = [bird for bird in birds if bird["name"] == bird_name]
    if (len(birdFound) > 0):
        return jsonify({"bird": birdFound[0]})
    return jsonify({"message": "bird not found"}) 

# Agregar un nuevo elemento
@app.route('/birds', methods= ["POST"])
def addBird():
    newBird = {
        "id": request.json['id'],
        "name": request.json['name'],
        "color": request.json['color']
    }
    birds.append(newBird)
    return jsonify({"message": "Birds added successfully", "birds": birds})

# Editar un elemento
@app.route('/birds/<string:bird_name>', methods= ["PUT"])
def editBird(bird_name):
    birdFound = [bird for bird in birds if bird["name"] == bird_name]
    if (len(birdFound) > 0):
        birdFound[0]['id'] = request.json['id']
        birdFound[0]['name'] = request.json['name']
        birdFound[0]['color'] = request.json['color']
        return jsonify({"message": "bird updated",
                    "bird": birdFound[0]}) 
    return jsonify({"message": "bird not found"}) 

# Eliminar un elemento
@app.route('/birds/<string:bird_name>', methods= ["DELETE"])
def deleteBird(bird_name):
    birdFound = [bird for bird in birds if bird["name"] == bird_name]
    if (len(birdFound) > 0):
        birds.remove(birdFound[0])
        return jsonify({"message": "bird deleted",
                    "bird": birds}) 
    return jsonify({"message": "bird not found"}) 
# ---------------------------------------------------------------------------------

# Pagina no encontrada error 404
def pageNoFound(error):
    # return render_template('404.html'), 404
    return redirect(url_for('home'))

# Autocompilación
if __name__ == '__main__':
    app.register_error_handler(404, pageNoFound)
    app.run(debug=True, port=4000)