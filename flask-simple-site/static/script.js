const ctx = document.getElementById('D1').getContext('2d');

const diagramm = new Chart(ctx, {
    type: 'bar', // Diagrammtyp: bar, line, pie, etc.
    data: {
        labels: ['Jan', 'Feb', 'Mär', 'Apr'],
        datasets: [{
            label: 'Umsatz',
            data: [120, 190, 300, 250],
            borderWidth: 1
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

