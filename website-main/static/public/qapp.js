find = window.location.href

fetch(find.substr(0, find.length - 4) + 'get_question/', ).then(response => response.json())
  .then(objects => {
    'use strict mode'

    op = 0;
    $(window).blur(function () {
      if (op == 0) {
        op = 1
        alert("Don't change tab again. Test will get automatically submitted.");
      } else if (op == 1) {
        quiz.innerHTML = `<h1>You changed tabs twice which lead to automatic submission of your test!</h1>`;
        let str = new String,
          quest = new String;
        for (const [x, y] of clicked) {
          quest += x + ',';
          if (y != undefined) {
            let muls = new String;
            if (typeof y === "object") {
              for (let i = 0; i < y.length; i++) {
                muls += y[i] + '+';
              }
              str += muls.substr(0, muls.length - 1) + ',';
            } else str += y + ',';
          } else str += ',';
        }
        if (quest.length == 0) {
          for (let i = 0; i < obj.length; i++) {
            for (let j = 0; j < obj[i].questions.length; j++) {
              quest += obj[i].questions[j].number + ',';
              str += ',';
            }
          }
        }
        document.getElementById('ans').value = str.substr(0, str.length - 1);
        document.getElementById('all_questions_in_string').value = quest.substr(0, quest.length - 1);
        document.getElementById("quiz_submit_button").click()
        clearInterval(completecheck);
        clearInterval(t);
      }
    });


    const obj = objects.Quiz_data,
      questiontype = objects.qtype,
      timetype = objects.ttype;

    let answerEls = document.querySelectorAll('.answer'),
      answerElmul = document.querySelectorAll('.answermul');

    const quiz = document.getElementById('quiz'),
      sub = document.getElementById('subject');

    if (timetype == 'i') {
      document.getElementsByClassName('time')[0].children[0].style.display = "none";
    } else {
      document.getElementsByClassName('time')[0].children[1].style.display = "none";
    }

    let arr = new Array,
      clicked = new Array;
    var questiontotal = new Array,
      Questions = new Array;

    let questionmap = new Map();
    let sticky = document.querySelectorAll('.stick')[0];

    var ul = document.getElementById("chance");
    for (let i = 0; i < obj.length; i++) {
      var li = document.createElement("p");
      ul.appendChild(li);
      li.insertAdjacentHTML('afterend', `<button class="choose" id='chance${i}'><h5>${obj[i].section}</h5></button>`);
    }

    let tempmap = new Map();

    for (let i = 0; i < obj.length; i++) {
      tempmap.set(i, true);
    }

    function ck(k) {
      clearInterval(t);
      document.getElementById(`chance${k}`).disabled = 'true';
      questiontotal = obj[k].questions;
      Questions = obj[k].questions;
      work(k);
    }

    let checkit = false;

    for (let i = 0; i < obj.length; i++) {
      checkit = false;
      document.getElementById(`chance${i}`).addEventListener('click', function () {
        ck(i);
        checkit = true;
      });
    }

    

    function work(k) {
      document.getElementById('reltime').textContent = "00:40";
      const questionEl1 = document.getElementById('question1'),
        questionEl2 = document.getElementById('question2'),
        questionEl3 = document.getElementById('question3'),
        btn = document.getElementById('submit'),
        progressBarFull = document.getElementById('progressBarFull');

      let mcqmap = new Map();
      let numericmap = new Map();
      let multimap = new Map();

      let totalQuestions = questiontotal.length;
      let currentQuiz = 0,
        questionCounter = 0;
      document.getElementById('chance').style.display = 'none';
      document.getElementById('hide').style.display = "inline";
      document.getElementById('hide1').style.display = "inline";
      document.getElementById('left').textContent = 0;
      document.getElementById('missed').textContent = 0;
      document.getElementById('attempted').textContent = 0;

      //ALL DATA STORED IN MAPS
      {
        for (let i = 0; i < Questions.length; i++) {
          if (Questions[i].type == "s") {
            mcqmap.set(Questions[i], Questions[i].number);
          }
          if (Questions[i].type == "m") {
            multimap.set(Questions[i], Questions[i].number);
          }
          if (Questions[i].type == "i") {
            numericmap.set(Questions[i], Questions[i].number);
          }
        }
      }

      //SHUFFLE ARRAY
      function shuffle(array) {
        var currentIndex = array.length,
          randomIndex;

        while (0 !== currentIndex) {
          randomIndex = Math.floor(Math.random() * currentIndex);
          currentIndex--;
          [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
        }
        return array;
      }

      function loadQuiz() {
        const one = mcqmap.get(questiontotal[currentQuiz]);
        const two = numericmap.get(questiontotal[currentQuiz]);
        const three = multimap.get(questiontotal[currentQuiz]);

        let image = questiontotal[currentQuiz].img;
        const MAX_QUESTIONS = totalQuestions;
        document.getElementById('left').textContent = MAX_QUESTIONS - questionCounter;
        progressBarFull.style.width = `${(questionCounter/MAX_QUESTIONS) * 100}%`;
        questionCounter++;
        if (one) {
          if (image.length) {
            document.getElementsByTagName('img')[0].style.display = "block";
            document.getElementsByTagName('img')[0].src = "../../../media/" + image;
          } else {
            document.getElementsByTagName('img')[0].style.display = "none";
          }
          document.getElementById('singleCorrect').style.display = "inline";
          document.getElementById('numerical').style.display = "none";
          document.getElementById('multiCorrect').style.display = "none";
          document.getElementById("list").innerHTML = "";
          document.getElementById("listmul").innerHTML = "";
          deselectAnswers();
          const currentQuizData = questiontotal[currentQuiz];
          questionEl1.innerText = currentQuizData.question;
          let charcode = 97;
          for (let i = 0; i < Object.keys(currentQuizData.options).length; i++) {
            var ul = document.getElementById("list");
            var li = document.createElement("li");
            ul.appendChild(li);
            let avar = String.fromCharCode(charcode);
            li.insertAdjacentHTML('afterend', `<input type="radio" name="answer" id="${avar}" class="answer"/><label for="${avar}" class="optionbox"><p class="ptag">${Object.values(currentQuizData.options)[i]}</p></label>`);
            charcode++;
          }
        } else if (two) {
          if (image.length) {
            document.getElementsByTagName('img')[1].style.display = "block";
            document.getElementsByTagName('img')[1].src = "../../../media/" + image;
          } else {
            document.getElementsByTagName('img')[1].style.display = "none";
          }
          document.getElementById('singleCorrect').style.display = "none";
          document.getElementById('numerical').style.display = "inline";
          document.getElementById('multiCorrect').style.display = "none";
          const currentQuizData = questiontotal[currentQuiz];
          questionEl2.innerText = currentQuizData.question;
        } else if (three) {
          if (image.length) {
            document.getElementsByTagName('img')[2].style.display = "block";
            document.getElementsByTagName('img')[2].src = "../../../media/" + image;
          } else {
            document.getElementsByTagName('img')[2].style.display = "none";
          }
          document.getElementById('singleCorrect').style.display = "none";
          document.getElementById('numerical').style.display = "none";
          document.getElementById('multiCorrect').style.display = "inline";
          document.getElementById("list").innerHTML = "";
          document.getElementById("listmul").innerHTML = "";
          deselectAnswersMul();
          const currentQuizData = questiontotal[currentQuiz];
          questionEl3.innerText = currentQuizData.question;
          let charcode = 97;
          for (let i = 0; i < Object.keys(currentQuizData.options).length; i++) {
            var ul = document.getElementById("listmul");
            var li = document.createElement("li");
            ul.appendChild(li);
            let avar = String.fromCharCode(charcode);
            li.insertAdjacentHTML('afterend', `<input type="checkbox" name="answer" id="${avar}" class="answermul" /><label for="${avar}" class="optionbox"><p class="ptag">${Object.values(currentQuizData.options)[i]}</p></label>`);
            charcode++;
          }
        }
      }

      //DESELECTING ANSWERS 
      function deselectAnswers() {
        answerEls = document.querySelectorAll('.answer');
        answerEls.forEach((answerEl) => (answerEl.checked = false));
      }

      //DESELECTING ANSWERS MULTIPLE
      function deselectAnswersMul() {
        answerElmul = document.querySelectorAll('.answermul');
        answerElmul.forEach((answerEl) => (answerEl.checked = false));
      }

      //SELECTING ANSWERS SINGLE CORRECT
      function getSelectedMcq() {
        let answer;
        answerEls = document.querySelectorAll('.answer');
        answerEls.forEach((answerEl) => {
          if (answerEl.checked) {
            answer = answerEl.id;
          }
        });
        return answer;
      }
      //SELECTING ANSWERS MULTIPLE CORRECT
      function getSelectedMul() {
        let answer = new Array;
        answerElmul = document.querySelectorAll('.answermul');
        answerElmul.forEach((answerEl) => {
          if (answerEl.checked) {
            answer.push(answerEl.id);
          }
        });
        return answer;
      }

      function singlesel() {
        answerEls = document.querySelectorAll('.answer');
        for (let i = 0; i < answerEls.length; i++) {
          if (answerEls[i].checked) {
            document.getElementsByClassName('ptag')[i].style.color = "white";
            document.getElementsByClassName('ptag')[i].style.background = "green";
            document.getElementsByClassName('ptag')[i].style.fontWeight = "bold";
          } else {
            document.getElementsByClassName('ptag')[i].style.color = "black";
            document.getElementsByClassName('ptag')[i].style.fontWeight = "normal";
            document.getElementsByClassName('ptag')[i].style.background = "#f0f0f0";
          }
        }
      }

      function multiplesel() {
        answerEls = document.querySelectorAll('.answermul');
        for (let i = 0; i < answerEls.length; i++) {
          if (answerEls[i].checked) {
            document.getElementsByClassName('ptag')[i].style.color = "white";
            document.getElementsByClassName('ptag')[i].style.background = "green";
            document.getElementsByClassName('ptag')[i].style.fontWeight = "bold";
          } else {
            document.getElementsByClassName('ptag')[i].style.color = "black";
            document.getElementsByClassName('ptag')[i].style.fontWeight = "normal";
            document.getElementsByClassName('ptag')[i].style.background = "#f0f0f0";
          }
        }
      }

      let optionsel = setInterval(function () {
        singlesel();
        multiplesel();
      }, 10);

      function checkanswer() {
        let one = mcqmap.get(questiontotal[currentQuiz]);
        let two = numericmap.get(questiontotal[currentQuiz]);
        let three = multimap.get(questiontotal[currentQuiz]);
        if (one) {
          let answer = getSelectedMcq();
          if (answer == undefined) {
            let ans = Number(document.getElementById('missed').textContent);
            ans++;
            document.getElementById('missed').textContent = ans;
          } else {
            let ans = Number(document.getElementById('attempted').textContent);
            ans++;
            document.getElementById('attempted').textContent = ans;
          }
          clicked.push([one, answer]);
        } else if (two) {
          let answer = document.getElementById('numericalAns').value;
          if (answer == "") {
            let ans = Number(document.getElementById('missed').textContent);
            ans++;
            document.getElementById('missed').textContent = ans;
          } else {
            let ans = Number(document.getElementById('attempted').textContent);
            ans++;
            document.getElementById('attempted').textContent = ans;
          }
          document.getElementById('numericalAns').value = "";
          clicked.push([two, answer]);
        } else if (three) {
          let answer = getSelectedMul();
          if (answer.length == 0) {
            let ans = Number(document.getElementById('missed').textContent);
            ans++;
            document.getElementById('missed').textContent = ans;
          } else {
            let ans = Number(document.getElementById('attempted').textContent);
            ans++;
            document.getElementById('attempted').textContent = ans;
          }
          clicked.push([three, answer]);
        }
      }
      let x, y;

      function time() {
        // questionTimeLeft.textContent = perTime;
        checkanswer();
        clearInterval(x);
        currentQuiz++;
        if (tempmap.get(k) == true) {
          if (currentQuiz < totalQuestions) {
            let timer = Number(questiontotal[currentQuiz].time),
              minutes, seconds;
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            document.querySelector('#questionTimeLeft').textContent = minutes + ":" + seconds;
            loadQuiz();
            resetTimer();
          } else {
            clearInterval(y);
            clearInterval(optionsel);
            document.getElementById('chance').style.display = 'inline';
            document.getElementById('hide').style.display = "none";
            document.getElementById('hide1').style.display = "none";
            tempmap.set(k, false);
            checkit = false;
            reltime = document.querySelector('#reltime');
            relTime(39, reltime);
          }
        }
      }

      shuffle(questiontotal);
      loadQuiz();
      //QUESTION TIME LEFT
      function startTimerQuestion(duration, display) {
        let timer = duration,
          minutes, seconds;
        x = setInterval(function () {
          minutes = parseInt(timer / 60, 10);
          seconds = parseInt(timer % 60, 10);
          minutes = minutes < 10 ? "0" + minutes : minutes;
          seconds = seconds < 10 ? "0" + seconds : seconds;
          display.textContent = minutes + ":" + seconds;
    
          if(timer < 10){
            document.getElementById("questionTimeLeft").style.color = "red";
          }
          if (timer < 1) {
            document.getElementById("questionTimeLeft").style.color = "black";
            checkanswer();
          }
          if (--timer < 0) {
            clearInterval(x);
            currentQuiz++;
            if (currentQuiz < totalQuestions) {
              loadQuiz();
              resetTimer();
            } else {
              clearInterval(optionsel); //----DIFF----//
              clearInterval(y);
              document.getElementById('chance').style.display = 'inline';
              document.getElementById('hide').style.display = "none";
              document.getElementById('hide1').style.display = "none";
              tempmap.set(k, false);
              checkit = false;
              reltime = document.querySelector('#reltime');
              relTime(39, reltime);
            }
          }
        }, 1000);
      }
      //TOTAL TIME LEFT
      function startTimer(duration, display) {

        let timer = duration,
          minutes, seconds, hours;

        y = setInterval(function () {
          hours = parseInt(timer / 3600, 10);
          minutes = parseInt(timer % 3600 / 60, 10);
          seconds = parseInt(timer % 3600 % 60, 10);
          hours = hours < 10 ? "0" + hours : hours;
          minutes = minutes < 10 ? "0" + minutes : minutes;
          seconds = seconds < 10 ? "0" + seconds : seconds;
          display.textContent = hours + ":" + minutes + ":" + seconds;
          if (timer < 1) {//----DIFF----//
            checkanswer();
          }
          if (--timer < -1) {
            clearInterval(y);
            clearInterval(optionsel);
            document.getElementById('chance').style.display = 'inline';
            document.getElementById('hide').style.display = "none";
            tempmap.set(k, false);
            checkit = false;
            reltime = document.querySelector('#reltime');
            relTime(39, reltime);
          }
        }, 1000);
      }
      totalTime = "99:00";

      if (timetype == 'i') {
        let pertime = Number(questiontotal[currentQuiz].time);
        let display1 = document.querySelector('#questionTimeLeft');
        let timer = pertime,
          minutes, seconds;
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        document.querySelector('#questionTimeLeft').textContent = minutes + ":" + seconds;
        startTimerQuestion(pertime - 1, display1);
      } else {
        totalTime = obj[k].section_time;
        document.getElementById("timeLeft").textContent = obj[k].section_time;
        let hours = totalTime.substr(0, 2),
          minutes = totalTime.substr(3, 2),
          seconds = totalTime.substr(6);
        let ttime = (3600 * Number(hours)) + (60 * Number(minutes)) + Number(seconds);
        let display = document.querySelector('#timeLeft');
        startTimer(ttime - 1, display);
      }

      //RESET TIME
      function resetTimer() {
        const pertime = Number(questiontotal[currentQuiz].time);
        let display1 = document.querySelector('#questionTimeLeft');
        let minutes = parseInt(pertime / 60, 10);
        let seconds = parseInt(pertime % 60, 10);
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        display1.textContent = minutes + ":" + seconds;
        startTimerQuestion(pertime - 1, display1);
      }

      //NEXT BUTTON FEATURE
      btn.addEventListener('click', function (e) {
        time();
      });

      //ENTER BUTTON FEATURE
      document.addEventListener('keydown', function (key) {
        if (key.code === 'Enter') {
          time();
        }
      });
    }

    //COMPLETED RELTIME
    var t;
    let count = 0;

    function relTime(duration, display) {
      let timer = duration,
        minutes, seconds;
      t = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        display.textContent = minutes + ":" + seconds;
        if (--timer < 0) {
          if (!checkit) {
            for (let i = 0; i < obj.length; i++) {
              if (tempmap.get(i) == true) {
                ck(i);
                break;
              }
            }
          }
          clearInterval(t);
        }
      }, 1000);
    }

    // ON RELOADING

    if (window.performance) {
      console.info("window.performance work's fine on this browser");
    }
    if (performance.navigation.type == 1) {
      let str = new String,
        quest = new String;
      for (let i = 0; i < obj.length; i++) {
        for (let j = 0; j < obj[i].questions.length; j++) {
          quest += obj[i].questions[j].number + ',';
          str += ',';
        }
      }
      document.getElementById('ans').value = str.substr(0, str.length - 1);
      document.getElementById('all_questions_in_string').value = quest.substr(0, quest.length - 1);
      document.getElementById('quiz_submit_button').click();
    } else {
      console.info("This page is reloaded");
    }
    //ON RELOADING
    let reltime = document.querySelector('#reltime');
    relTime(19, reltime);

    let completecheck = setInterval(finishcheck, 100);

    function finishcheck() {
      let count = 0;
      for (let i = 0; i < obj.length; i++) {
        if (tempmap.get(i) == false) count++;
      }
      if (count == obj.length) {
        quiz.innerHTML = ``;
        let str = new String,
          quest = new String;
        for (const [x, y] of clicked) {
          quest += x + ',';
          if (y != undefined) {
            let muls = new String;
            if (typeof y === "object") {
              for (let i = 0; i < y.length; i++) {
                muls += y[i] + '+';
              }
              str += muls.substr(0, muls.length - 1) + ',';
            } else str += y + ',';
          } else str += ',';
        }
        document.getElementById('ans').value = str.substr(0, str.length - 1);
        document.getElementById('all_questions_in_string').value = quest.substr(0, quest.length - 1);
        document.getElementById("quiz_submit_button").click()
        clearInterval(completecheck);
        clearInterval(t);
      }
    }
  })
  .catch((err) => {
    console.log('rejected', err);
  })



