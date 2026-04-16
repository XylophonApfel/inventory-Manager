// ===========================
// Datensätze für Dropdown
// ===========================

const datensaetze = {
  kisten: {
    label: 'Anzahl der Kisten',
    data: [1, 20, 60, 140, 190, 300, 250],
    borderColor: '#9C27B0',
    backgroundColor: 'rgba(156, 39, 176, 0.1)',
  },
  gesamtwert: {
    label: 'Gesamtwert des Inventars',
    data: [10, 40, 80, 110, 160, 210, 190],
    borderColor: '#4CAF50',
    backgroundColor: 'rgba(76, 175, 80, 0.1)',
  },
  // (alte Funktion, ist nicht mehr vorhanden, war zum TESTEN!)
  // test: {
  //   label: 'Test',
  //   data: [50, 90, 130, 200, 250, 320, 310],
  //   borderColor: '#2196F3',
  //   backgroundColor: 'rgba(33, 150, 243, 0.1)',
  // },
  // test1: {
  //   label: 'test',
  //   data: [500, 90, 1300, 200, 2500, 320, 3100],
  //   borderColor: '#FF5722',
  //   backgroundColor: 'rgba(255, 87, 34, 0.1)',
  // }
};

// ===========================
// Diagramm initialisieren
// ===========================
// Reihenfolge für den Abruf der Daten: 
// main.py → management.py → dashboard.html → script.js
// (Server)    (Daten)          (Template)      (Diagramm)

const ctx = document.getElementById('D1').getContext('2d');

const diagramm = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ECHTE_LABELS, // Benutzt die Daten aus Python
    datasets: [{
      label: 'Gesamtwert Portfolio',
      data: ECHTE_DATEN,   // Benutzt die Daten aus Python
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

// (alte Funktion, ist nicht mehr vorhanden, war zum TESTEN!)

// ===========================
// Dropdown → Diagramm wechseln 
// ===========================

// document.getElementById('chart-select').addEventListener('change', function () {
//   const auswahl = datensaetze[this.value];

//   diagramm.data.datasets[0].label = auswahl.label;
//   diagramm.data.datasets[0].data = auswahl.data;
//   diagramm.data.datasets[0].borderColor = auswahl.borderColor;
//   diagramm.data.datasets[0].backgroundColor = auswahl.backgroundColor;

//   diagramm.update();
// });
