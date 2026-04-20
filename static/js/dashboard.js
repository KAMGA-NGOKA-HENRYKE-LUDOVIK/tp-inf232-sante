// static/js/dashboard.js

// Cette fonction récupère les données de l'API Python et crée les graphiques
fetch('/api/analyse')
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            console.log("En attente de données...");
            return;
        }

        // Mise à jour des cartes de statistiques
        document.getElementById('total-count').innerText = data.total_consultations;
        document.getElementById('avg-temp').innerText = data.temperature_moyenne + "°C";
        document.getElementById('common-symptom').innerText = data.symptome_dominant;

        // Création du graphique de répartition par genre
        const ctx = document.getElementById('genreChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(data.repartition_genre),
                datasets: [{
                    label: 'Répartition par Genre',
                    data: Object.values(data.repartition_genre),
                    backgroundColor: ['#007bff', '#ff6384', '#ffce56']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Répartition des Patients' }
                }
            }
        });
    })
    .catch(error => console.error('Erreur lors de la récupération des données:', error));
