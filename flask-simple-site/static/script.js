const ctx = document.getElementById('D1').getContext('2d');

const diagramm = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul'],
        datasets: [{
            label: 'Umsäze durch Kisten',
            data: [1, 20, 60, 140, 190, 300, 250],
            backgroundColor: ['white'],
            borderColor: 'black',
            lineColor: 'white',
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
