// ===========================
// Datensätze für Dropdown
// ===========================

const datensaetze = {
  kisten: {
    label: 'Umsätze durch Kisten',
    data: [1, 20, 60, 140, 190, 300, 250],
    borderColor: '#9C27B0',
    backgroundColor: 'rgba(156, 39, 176, 0.1)',
  },
  gewinn: {
    label: 'Gesamtgewinn',
    data: [10, 40, 80, 110, 160, 210, 190],
    borderColor: '#4CAF50',
    backgroundColor: 'rgba(76, 175, 80, 0.1)',
  },
  umsatz: {
    label: 'Gesamtumsatz',
    data: [50, 90, 130, 200, 250, 320, 310],
    borderColor: '#2196F3',
    backgroundColor: 'rgba(33, 150, 243, 0.1)',
  },
  performance: {
    label: 'Performance (%)',
    data: [5, 12, 18, 25, 30, 42, 38],
    borderColor: '#FF5722',
    backgroundColor: 'rgba(255, 87, 34, 0.1)',
  }
};

// ===========================
// Diagramm initialisieren
// ===========================

const ctx = document.getElementById('D1').getContext('2d');

const diagramm = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul'],
    datasets: [{
      label: datensaetze.kisten.label,
      data: datensaetze.kisten.data,
      borderColor: datensaetze.kisten.borderColor,
      backgroundColor: datensaetze.kisten.backgroundColor,
      borderWidth: 2,
      pointRadius: 8,
      pointHoverRadius: 10,
      fill: true,
      tension: 0.4,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0,0,0,0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    plugins: {
      legend: {
        display: false
      }
    }
  }
});

// ===========================
// Dropdown → Diagramm wechseln
// ===========================

document.getElementById('chart-select').addEventListener('change', function () {
  const auswahl = datensaetze[this.value];

  diagramm.data.datasets[0].label = auswahl.label;
  diagramm.data.datasets[0].data = auswahl.data;
  diagramm.data.datasets[0].borderColor = auswahl.borderColor;
  diagramm.data.datasets[0].backgroundColor = auswahl.backgroundColor;

  diagramm.update();
});

