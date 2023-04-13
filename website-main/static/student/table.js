const ul = document.body;


function generateGraphs(obj, myChart1, myChart2, myChart3, myChart4) {
    let maxmarks = obj.max_marks;
    let totalStudents = obj.main.length;
    let totalQuestions = obj.que.length;

    // First graph
    let studentMarks = [];

    for (let i = 0; i < totalStudents; ++i) studentMarks.push((obj.main)[i].marks);

    let xValues = new Array();
    let yValues = new Array();
    let barColors = new Array();
    let frequency = new Array();
    for (let i = 0; i <= maxmarks; i++) xValues.push(i);
    for (let i = 0; i <= maxmarks; i++) frequency.push(0);
    for (let i = 0; i < totalStudents; i++) frequency[studentMarks[i]]++;

    for (let i = 0; i < frequency.length; i++) {
        yValues.push(frequency[i]);
        barColors.push("#ffa500");
    }

    new Chart(myChart1, {
        type: "bar",
        data: {
            labels: xValues,
            datasets: [{
                barPercentage: 0.7,
                backgroundColor: barColors,
                data: yValues,
            }]
        },
        options: {
            showLine: false,
            legend: {
                display: false
            },
            title: {
                display: true,
                text: "Marks Distribution"
            },
            scales: {
                x: {
                    grid: {
                        color: 'red',
                    }
                },
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Student'
                    },
                    gridLines: {
                        display: false,
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Marks'
                    },
                    gridLines: {
                        display: false,
                    }
                }]
            }
        }
    });


    // Second Graph
    let question = new Array();

    let attempted = [];
    let correct = [];
    let wrong = [];

    for (let i = 0; i < totalQuestions; i++) {
        question.push(`Q${i+1}`);
        attempted[i] = 0;
        correct[i] = 0;
        wrong[i] = 0;
    }

    for (let i = 0; i < totalStudents; ++i) {
        for (let j = 0; j < totalQuestions; ++j) {
            if (obj.main[i].main[j] !== '-') {
                attempted[j]++;

                if (obj.main[i].main[j] === obj.corr[j]) {
                    correct[j]++;
                } else {
                    wrong[j]++;
                }
            }
        }
    }

    let data2 = {
        labels: question,
        datasets: [{
                label: "Attempted",
                backgroundColor: "#FF6384",
                data: attempted,
                minBarLength: 2,
            },
            {
                label: "Correct",
                backgroundColor: "#4BC0C0",
                data: correct,
                minBarLength: 2,
            },
            {
                label: "Wrong",
                backgroundColor: "#36A2EB",
                data: wrong,
                minBarLength: 2,
            }
        ]
    };

    new Chart(myChart2, {
        type: "bar",
        data: data2,
        options: {
            barValueSpacing: 100,
            legend: {
                display: true
            },
            title: {
                display: true,
                text: "Marks Distribution"
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Students'
                    },
                    gridLines: {
                        display: false,
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Question'
                    },
                    gridLines: {
                        display: false,
                    }
                }]
            }
        }
    });


    // Third and Fourth graph

    // difficulty level set by teachers
    let easy = 0;
    let med = 0;
    let hard = 0;

    for (let i = 0; i < totalQuestions; ++i) {
        if (obj.diff[i] === 'e') {
            easy++;
        } else if (obj.diff[i] === 'm') {
            med++;
        } else {
            hard++;
        }
    }

    let data3 = {
        labels: [
            'Easy',
            'Medium',
            'Hard'
        ],
        datasets: [{
            label: 'Level',
            data: [easy, med, hard],
            backgroundColor: [
                'yellow',
                'orange',
                'red'
            ],
            borderColor: [
                'black',
                'black',
                'black'
            ],
            hoverOffset: 4
        }]
    };

    new Chart(myChart3, {
        type: "pie",
        data: data3,
        options: {
            legend: {
                display: true
            },
            title: {
                display: true,
                text: "Difficulty Level(Teacher)"
            }
        }
    });

    // difficulty level according to students
    let easy1 = 0
    let med1 = 0;
    let hard1 = 0;

    let correctFreqQuestionWise = [];

    for (let i = 0; i < totalQuestions; ++i) {
        correctFreqQuestionWise[i] = 0;
    }

    for (let i = 0; i < totalStudents; ++i) {
        for (let j = 0; j < totalQuestions; ++j) {
            if (obj.main[i].main[j] === obj.corr[j]) {
                correctFreqQuestionWise[j]++;
            }
        }
    }

    for (let i = 0; i < totalQuestions; ++i) {
        let accuracy = (correctFreqQuestionWise[i] / totalStudents) * 100;

        if (accuracy > 80) {
            easy1++;
        } else if (accuracy > 30) {
            med1++;
        } else {
            hard1++;
        }
    }

    let data4 = {
        labels: [
            'Easy',
            'Medium',
            'Hard'
        ],
        datasets: [{
            label: 'Level',
            data: [easy1, med1, hard1],
            backgroundColor: [
                'yellow',
                'orange',
                'red'
            ],
            borderColor: [
                'black',
                'black',
                'black'
            ],
            hoverOffset: 4
        }]
    };

    new Chart(myChart4, {
        type: "pie",
        data: data4,
        options: {
            legend: {
                display: true
            },
            title: {
                display: true,
                text: "Difficulty level(Student)"
            }
        }
    });
}

const createResult = function () {
    const tbody = document.getElementsByTagName('tbody');
    ul.insertAdjacentHTML('beforebegin', `<div>
    <a class="btn-css" id="quiz-btn" href="./">Go to Quiz</a>
  </div>`);
    ul.insertAdjacentHTML('beforebegin', `
    <h1 id="main-heading" >Result</h1>
    <table class="results xa" id="cmbn" data-excel-name="Summary">
        <tr>
            <th>S.no</th>
            <th>Name</th>
            <th>Roll_no.</th>
            <th>Email</th>
        </tr>
        <tr>
            <th>Marks</th>
            <th>-</th>
            <th>-</th>
            <th>-</th>
        </tr>
    </table>
    `);

    for (let i = 0; i < array.length; i++) {
        tbody[0].children[0].insertAdjacentHTML('beforeend', `<th>${array[i].heading}</th>`);
    }
    tbody[0].children[0].insertAdjacentHTML('beforeend', `<th>Total Marks</th>`);

    let totalmarks = 0;
    for (let i = 0; i < array.length; i++) {
        tbody[0].children[1].insertAdjacentHTML('beforeend', `<th>${array[i].max_marks}</th>`);
        totalmarks += array[i].max_marks;
    }
    tbody[0].children[1].insertAdjacentHTML('beforeend', `<th>${totalmarks}</th>`);

    for (let j = 0; j < array[0].main.length; j++) {
        tbody[0].insertAdjacentHTML('beforeend', `
    <td>${array[0].main[j].num}</td>
    <td>${array[0].main[j].name}</td>
    <td>${array[0].main[j].rollno}</td>
    <td>${array[0].main[j].mail}</td>
    `);
    }
    if (array.length == 1) {
        console.log(tbody);
        let res = document.querySelectorAll('.result tbody tr');
        res.forEach(ele => {
            let len = ele.childElementCount;
            ele.children[len - 2].style.display = "none";
        });
    }

    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].main.length; j++) {
            tbody[0].children[j + 2].insertAdjacentHTML('beforeend', `<td>${array[i].main[j].score}</td>`);
        }
    }
    const last = tbody[0].querySelectorAll('tr');
    for (let i = 2; i < last.length; i++) {
        let td = last[i].children;
        let score = 0;
        for (let j = 4; j < td.length; j++) score += Number(td[j].textContent);
        tbody[0].children[i].insertAdjacentHTML('beforeend', `<td>${score}</td>`);
    }
}

const tables = document.getElementById('tables');
const createTable = function () {
    for (let i = 0; i < array.length; i++) {
        tables.insertAdjacentHTML('beforeend', `<br>
    <h1 class="result">${array[i].heading} Result</h1>
    <table class="com xa" id="cmbn" data-excel-name="${array[i].heading}">
        <tr>
            <th>S.no</th>
            <th>Name</th>
            <th>Roll_no.</th>
            <th>Email</th>
        </tr>
        <tr>
            <th>Correct Answers</th>
            <th>-</th>
            <th>-</th>
            <th>-</th>
        </tr>
    </table>
    <div class = "charts">
        <canvas class="chart-section" id="myChart${i}1" style="width:100%;max-width:900px"></canvas>
        <canvas class="chart-section" id="myChart${i}2" style="width:100%;max-width:900px"></canvas>
        <canvas class="chart-section" id="myChart${i}3" style="width:100%;max-width:500px;display:flex"></canvas>
        <canvas class="chart-section" id="myChart${i}4" style="width:100%;max-width:500px;display:flex"></canvas>
    <div>
    `);
    }

    const tbody = document.getElementsByTagName('tbody');

    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].que.length; j++) {
            tbody[i].children[0].insertAdjacentHTML('beforeend', `<th>${array[i].que[j]}</th>`);
        }
        tbody[i].children[0].insertAdjacentHTML('beforeend', `<th>Score</th>`);
    }


    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].que.length; j++) {
            tbody[i].children[1].insertAdjacentHTML('beforeend', `<th>${array[i].corr[j]}</th>`);
        }
    }

    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].main.length; j++) {
            tbody[i].insertAdjacentHTML('beforeend', `
        <td>${array[i].main[j].num}</td>
        <td>${array[i].main[j].name}</td>
        <td>${array[i].main[j].rollno}</td>
        <td>${array[i].main[j].mail}</td>
        `);
        }
    }

    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].main.length; j++) {
            for (const it of array[i].main[j].main) {
                tbody[i].children[j + 2].insertAdjacentHTML('beforeend', `<td>${it}</td>`);
            }
        }
    }
    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].main.length; j++) {
            let score = 0;
            for (let k = 0; k < array[i].main[j].main.length; k++) {
                if (array[i].main[j].main[k] == array[i].corr[k]) score++;
            }
            array[i].main[j].score = score;
            tbody[i].children[j + 2].insertAdjacentHTML('beforeend', `<td>${score}</td>`);
        }
    }

    createResult();
}
createTable();

function it() {
    st = ""
    for (let i = 0; i < feed.length; i++) {
        st += "<th>" + feed[i] + `</th>`
    }
    return st;

}

function doit(i) {
    st = ""
    for (let j = 0; j < feed.length; j++) {
        if (j >= data[i].answers.length) {
            st += `<td> - </td>
            `
            continue;
        }
        st += `<td>` + data[i].answers[j] + `</td>
        `
    }
    return st;
}
const createFeedback = function () {
    const tbody = document.getElementsByTagName('tbody');
    ul.insertAdjacentHTML('beforebegin', `<button class="feedback btn-css">Feedback</button>`);
    ul.insertAdjacentHTML('beforeend', `
    <div id=fb>
    
  <h1 style="center">Feedback</h1>
  <table class="fee" id="cmbn">
      <tr>
          <th>Name</th>` + it() + `
      </tr>
  </table>
  </div>
  `);
    for (let i = 0; i < data.length; i++) {
        tbody[tbody.length - 1].insertAdjacentHTML('beforeend', `
          <td>${data[i].name}</td>
          ` + doit(i));
    };

    let feedback = document.querySelectorAll('.feedback');
    let fb = document.getElementById('fb');
    fb.style.display = "none";

}
const add = function () {
    createFeedback();
    let resultTable = document.querySelectorAll('.com');
    let result = document.querySelectorAll('.result');
    let chart = document.querySelectorAll('.charts');
    resultTable.forEach((e, i) => {
        generateGraphs(array[i], `myChart${i}1`, `myChart${i}2`, `myChart${i}3`, `myChart${i}4`);
        e.style.display = "none";
        result[i].style.display = "none";
        chart[i].style.display = "none";
    });

    ul.insertAdjacentHTML('beforebegin', `<button class="btn-css" id = "resultBtn">Detailed Result</button>`);
    ul.insertAdjacentHTML('beforebegin', `<button class="btn-css" id = "showChart">Detailed Analysis</button>`);
    let resultBtn = document.querySelector('#resultBtn');
    let showChart = document.querySelector('#showChart');
    let fb = document.getElementById('fb');
    resultBtn.addEventListener('click', function () {
        resultTable.forEach((e, i) => {
            if (e.style.display === "none") {
                e.style.display = "block";
                result[i].style.display = "block";
            } else {
                e.style.display = "none";
                result[i].style.display = "none";
            }
            chart[i].style.display = "none";
        });
        fb.style.display = "none";
    });
    showChart.addEventListener('click', function () {
        chart.forEach((e, i) => {
            if (e.style.display === "none") {
                e.style.display = "block";
                result[i].style.display = "block";
            } else {
                e.style.display = "none";
                result[i].style.display = "none";
            }
            resultTable[i].style.display = "none";
        });
        fb.style.display = "none";
    });

    let feedback = document.querySelectorAll('.feedback');
    feedback[0].addEventListener('click', function () {
        if (fb.style.display == "none") {
            fb.style.display = "block";
            resultTable.forEach((e, i) => {
                e.style.display = "none";
                result[i].style.display = "none";
                chart[i].style.display = "none";
            });
        } else {
            fb.style.display = "none";
        }
    });
}
setTimeout(add, 10);
