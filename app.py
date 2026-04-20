from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configuration de la base de données (SQLite pour la simplicité)
app.config['SQLALCHEMY_DATABASE_DATABASE_URI'] = 'sqlite:///sante_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODÈLE DE DONNÉES (La Structure) ---
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(10), nullable=False)
    symptome = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    ville = db.Column(db.String(50), nullable=False)

# Création de la base de données
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Serveur de Collecte de Santé Opérationnel"

if __name__ == '__main__':
    app.run(debug=True)
    
    
@app.route('/api/analyse', methods=['GET'])
def analyser_donnees():
    query = Consultation.query.all()
    if not query:
        return jsonify({"message": "Vide"}), 404
    
    # Conversion en DataFrame Pandas pour l'analyse
    df = pd.DataFrame([(c.age, c.genre, c.symptome, c.temperature) for c in query], 
                      columns=['age', 'genre', 'symptome', 'temperature'])

    # Analyse Descriptive robuste avec Pandas
    analyse = {
        "total_consultations": len(df),
        "temperature_moyenne": round(df['temperature'].mean(), 2),
        "age_moyen": round(df['age'].mean(), 1),
        "symptome_dominant": df['symptome'].mode()[0],
        "repartition_genre": df['genre'].value_counts().to_dict()
    }
    
    return jsonify(analyse)

@app.route('/dashboard')
def dashboard():
    return render_template('analyse.html')
    
    
    
from flask import redirect, url_for

# ... (reste du code précédent)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collecte', methods=['POST'])
def collecte():
    # Récupération des données du formulaire
    nouvelle_consultation = Consultation(
        age=int(request.form.get('age')),
        genre=request.form.get('genre'),
        symptome=request.form.get('symptome'),
        temperature=float(request.form.get('temperature')),
        ville=request.form.get('ville')
    )
    
    # Enregistrement dans la base de données
    db.session.add(nouvelle_consultation)
    db.session.commit()
    
    # Une fois enregistré, on redirige vers l'index ou une page de succès
    return redirect(url_for('index'))
