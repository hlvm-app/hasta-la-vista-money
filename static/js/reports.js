const incomeAmounts = incomeExpense.incomeAmounts;
const receiptSums = incomeExpense.receiptSums;
const incomeExpenseByMonthsChartsBar = document.getElementById('income_expense_by_months_charts_bar').getContext('2d');
const incomeExpenseByMonthsChartsLine = document.getElementById('income_expense_by_months_charts_line').getContext('2d');

// Константы
const MONTHS = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь'
];

// Utils functions
function months(config) {
    const cfg = config || {};
    const count = cfg.count || 12;
    const section = cfg.section;
    const values = [];
    let i, value;

    for (i = 0; i < count; ++i) {
        value = MONTHS[Math.ceil(i) % 12];
        values.push(value.substring(0, section));
  }

  return values;
}

// Столбчатый график по доходам и расходам по месяцам
const incomeExpenseChartsBar = new Chart(incomeExpenseByMonthsChartsBar, {
    type: 'bar',
    data: {
        labels: months({count: 12}),  // Месяцы доходов на оси X
        datasets: [{
            label: 'Доходы по месяцам',
            data: incomeAmounts,  // Суммы доходов на оси Y
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 99, 132, 0.5)',
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
                'rgb(255, 99, 132)',
            ],
            fill: false
        }, {
            label: 'Расходы по месяцам',
            data: receiptSums,  // Суммы чеков на оси Y
            backgroundColor: [
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
            ],
            borderColor: [
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
                'rgb(137, 8, 165)',
            ],
            fill: false
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Линейный график по доходам и расходам по месяцам
const incomeExpenseChartsLine = new Chart(incomeExpenseByMonthsChartsLine, {
    type: 'line',
    data: {
        labels: months({count: 12}),
        datasets: [{
            label: 'Доходы по месяцам',
            data: incomeAmounts,
            backgroundColor: 'rgb(255, 99, 132, 0.5)',
            borderColor: 'rgb(255, 99, 132)',
            fill: false
        }, {
            label: 'Расходы по месяцам',
            data: receiptSums,
            backgroundColor: 'rgb(137, 8, 165, 0.5)',
            borderColor: 'rgb(137, 8, 165)',
            fill: false
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        title: {
        display: true,
        text: 'Chart.js Line Chart'
      }
    }
});
