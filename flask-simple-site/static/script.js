const ctx = document.getElementById('D1').getContext('2d');

const diagramm = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul'],
        datasets: [{
            label: 'Umsäze durch Kisten',
            data: [1, 20, 60, 140, 190, 300, 250],
            backgroundColor: ['purple'],
            borderColor: 'black',
            borderWidth: 1,
            pointRadius: 8,
            pointHoverRadius: 10,                            
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

