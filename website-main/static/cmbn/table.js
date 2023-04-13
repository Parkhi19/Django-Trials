
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
        barColors.push("blue");
    }

    new Chart(myChart1, {
        type: "bar",
        data: {
            labels: xValues,
            datasets: [{
                backgroundColor: barColors,
                barThickness: 60,
                data: yValues
            }]
        },
        options: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: "Marks Distribution"
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
                backgroundColor: "red",
                data: attempted
            },
            {
                label: "Correct",
                backgroundColor: "green",
                data: correct
            },
            {
                label: "Wrong",
                backgroundColor: "blue",
                data: wrong
            }
        ]
    };

    new Chart(myChart2, {
        type: "bar",
        data: data2,
        options: {
            barValueSpacing: 100,
            legend: {
                display: false
            },
            title: {
                display: true,
                text: "Marks Distribution"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
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
                display: false
            },
            title: {
                display: true,
                text: "Teacher Level Distribution"
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
                display: false
            },
            title: {
                display: true,
                text: "Student Level Distribution"
            }
        }
    });
}

const createResult = function () {
    const tbody = document.getElementsByTagName('tbody');
    ul.insertAdjacentHTML('beforeend', `
    <h1>Result</h1>
    <table class="result" id="cmbn">
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
        tbody[tbody.length - 1].children[0].insertAdjacentHTML('beforeend', `<th>${array[i].heading}</th>`);
    }
    tbody[tbody.length - 1].children[0].insertAdjacentHTML('beforeend', `<th>Total Marks</th>`);

    let totalmarks = 0;
    for (let i = 0; i < array.length; i++) {
        tbody[tbody.length - 1].children[1].insertAdjacentHTML('beforeend', `<th>${array[i].max_marks}</th>`);
        totalmarks += array[i].max_marks;
    }
    tbody[tbody.length - 1].children[1].insertAdjacentHTML('beforeend', `<th>${totalmarks}</th>`);

    for (let j = 0; j < array[0].main.length; j++) {
        tbody[tbody.length - 1].insertAdjacentHTML('beforeend', `
    <td>${array[0].main[j].num}</td>
    <td>${array[0].main[j].name}</td>
    <td>${array[0].main[j].rollno}</td>
    <td>${array[0].main[j].mail}</td>
    `);
    }
}

const createTable = function () {
    for (let i = 0; i < array.length; i++) {
        ul.insertAdjacentHTML('beforeend', `<br>
    <button class="resultBtn">${array[i].heading} Result</button>
    <table class="com" id="cmbn" data-excel-name="${array[i].heading}">
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
    <button class = "chart-btn hide">SHOW CHART</button>
    <div class = "charts">
        <canvas id="myChart${i}1" style="width:100%;max-width:500px"></canvas>
        <canvas id="myChart${i}2" style="width:100%;max-width:500px"></canvas>
        <canvas id="myChart${i}3" style="width:100%;max-width:500px"></canvas>
        <canvas id="myChart${i}4" style="width:100%;max-width:500px"></canvas>
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

const createFeedback = function () {
    const tbody = document.getElementsByTagName('tbody');
    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].main.length; j++) {
            tbody[tbody.length - 1].children[j + 2].insertAdjacentHTML('beforeend', `<td>${array[i].main[j].score}</td>`);
        }
    }
    const last = tbody[tbody.length - 1].querySelectorAll('tr');
    for (let i = 2; i < last.length; i++) {
        let td = last[i].children;
        let score = 0;
        for (let j = 4; j < td.length; j++) score += Number(td[j].textContent);
        tbody[tbody.length - 1].children[i].insertAdjacentHTML('beforeend', `<td>${score}</td>`);
    }

    ul.insertAdjacentHTML('beforeend', `
    <h1>Feedback</h1>
        <table class="feedback" id="cmbn">
            <tr>
                <th>User</th>
                <th>Star 1</th>
                <th>Star 2</th>
                <th>Ans</th>
                <th>Cheat</th>
                <th>Prevent</th>
                <th>Rating</th>
                <th>Custom</th>
            </tr>
        </table>
        `);
    for (let i = 0; i < feedbackData.length; i++) {
        let text = "";
        for (let j = 0; j < feedbackData[i].custom.length; j++) {
            if (feedbackData[i].custom[j]) text += feedbackData[i].custom[j] + " , ";
        }
        tbody[tbody.length - 1].insertAdjacentHTML('beforeend', `
                <td>${feedbackData[i].user}</td>
                <td>${feedbackData[i].star1}</td>
                <td>${feedbackData[i].star2}</td>
                <td>${feedbackData[i].ans}</td>
                <td>${feedbackData[i].cheat}</td>
                <td>${feedbackData[i].prevent}</td>
                <td>${feedbackData[i].rating}</td>
                <td>${text.substring(0,text.length-1)}</td>
                `);
    }
}

const add = function () {
    createFeedback();
    let resultBtn = document.querySelectorAll('.resultBtn');
    let resultTable = document.querySelectorAll('.com');
    let chartBtn = document.querySelectorAll('.chart-btn');
    let charts = document.querySelectorAll('.charts');
    console.log(resultBtn);
    resultBtn.forEach((e, i) => {
        generateGraphs(array[i],`myChart${i}1`,`myChart${i}2`,`myChart${i}3`,`myChart${i}4`);
        e.addEventListener('click', function () {
            if (resultTable[i].style.display == "block") {
                resultTable[i].style.display = "none";
                chartBtn[i].style.display = "none";
            }
            else {
                resultTable[i].style.display = "block";
                chartBtn[i].style.display = "block";
            }
        });
    });
    chartBtn.forEach((e, i) => {
        e.addEventListener('click', function () {
            if (charts[i].style.display == "block") charts[i].style.display = "none";
            else charts[i].style.display = "block";
        });
    });
}
setTimeout(add, 10);
