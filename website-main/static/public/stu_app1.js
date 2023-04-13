find = window.location.href


fetch(find.substr(0, find.length - 4) + 'get_question/',).then(response => response.json())
  .then(objects => {
    

    'use strict mode'
    var totalTime = "20:00";
    var perTime = "00:00";
    var subject = "General";


    let answerEls = document.querySelectorAll('.answer'),
      answerElmul = document.querySelectorAll('.answermul');

    const quiz = document.getElementById('quiz'),
      sub = document.getElementById('subject');

    let arr = new Array,
      clicked = new Array;
    var questiontotal = new Array,
      Questions = new Array;

    let questionmap = new Map();

    var ul = document.getElementById("chance");
    for (let i = 0; i < obj.length; i++) {
      var li = document.createElement("p");
      ul.appendChild(li);
      li.insertAdjacentHTML('afterend', `<button class="choose" id='chance${i}'><h2>${obj[i].section}</h2></button>`);
    }

    let tempmap = new Map();

    for (let i = 0; i < 4; i++) {
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
    document.getElementById('chance0').addEventListener('click', function () {
      ck(0);
      checkit = true;
    });
      document.getElementById('chance1').addEventListener('click', function(){
        ck(1);
        checkit = true;
      });
    // document.getElementById('chance2').addEventListener('click', function(){
    //   ck(2);
    //   checkit = true;
    // });
    // document.getElementById('chance3').addEventListener('click', function(){
    //   ck(3);
    //   checkit = true;
    // });


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

      let totalQuestions = questiontotal.length;//BUG IMPORTANT
      let currentQuiz = 0,
        questionCounter = 0,
        questionTimeLeft = document.getElementById("questionTimeLeft"),
        minutes = totalTime.substr(0, 2),
        seconds = totalTime.substr(3);
      document.getElementById('chance').style.display = 'none';
      document.getElementById('hide').style.display = "inline";
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

      //QUIZ CHECK
      function loadQuiz() {
        const one = mcqmap.get(questiontotal[currentQuiz]);
        const two = numericmap.get(questiontotal[currentQuiz]);
        const three = multimap.get(questiontotal[currentQuiz]);
        const MAX_QUESTIONS = totalQuestions;
        document.getElementById('left').textContent = MAX_QUESTIONS - questionCounter;
        questionCounter++;
        progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;
        if (one) {
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
            li.insertAdjacentHTML('afterend', `<p class="optionbox"><input type="radio" name="answer" id="${String.fromCharCode(charcode)}" class="answer" /><label for="${String.fromCharCode(charcode)}">${Object.values(currentQuizData.options)[i]}</label></p>`);
            charcode++;
          }
        } else if (two) {
          document.getElementById('singleCorrect').style.display = "none";
          document.getElementById('numerical').style.display = "inline";
          document.getElementById('multiCorrect').style.display = "none";
          const currentQuizData = questiontotal[currentQuiz];
          questionEl2.innerText = currentQuizData.question;
        } else if (three) {
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
            li.insertAdjacentHTML('afterend', `<p class="optionbox"><input type="checkbox" name="answer" id="${String.fromCharCode(charcode)}" class="answermul" /><label for="${String.fromCharCode(charcode)}">${Object.values(currentQuizData.options)[i]}</label></p>`);
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
        questionTimeLeft.textContent = perTime;
        checkanswer();
        clearInterval(x);
        currentQuiz++;
        if (tempmap.get(k) == true) {
          if (currentQuiz < totalQuestions) {
            loadQuiz();
            resetTimer();
          } else {
            clearInterval(y);
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
            // document.getElementById('ans').value = str.substr(0, str.length - 1);
            // document.getElementById('all_questions_in_string').value = quest.substr(0, quest.length - 1);
            document.getElementById('chance').style.display = 'inline';
            document.getElementById('hide').style.display = "none";
            tempmap.set(k, false);
            checkit = false;
            reltime = document.querySelector('#reltime');
            relTime(9, reltime);
          }
        }
      }

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
          if (timer < 1) {
            checkanswer();
          }
          if (--timer < 0) {
            clearInterval(x);
            currentQuiz++;
            if (currentQuiz < totalQuestions) {
              loadQuiz();
              resetTimer();
            } else {
              clearInterval(y);

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
              document.getElementById('chance').style.display = 'inline';
              document.getElementById('hide').style.display = "none";
              tempmap.set(k, false);

              reltime = document.querySelector('#reltime');
              relTime(39, reltime);
            }
          }
        }, 1000);
      }
      //TOTAL TIME LEFT
      function startTimer(duration, display) {
        shuffle(questiontotal);
        loadQuiz();
        let timer = duration,
          minutes, seconds;

        y = setInterval(function () {
          minutes = parseInt(timer / 60, 10);
          seconds = parseInt(timer % 60, 10);
          minutes = minutes < 10 ? "0" + minutes : minutes;
          seconds = seconds < 10 ? "0" + seconds : seconds;
          display.textContent = minutes + ":" + seconds;
          if (--timer < -1) {
            clearInterval(y);
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
            // document.getElementById('ans').value = str.substr(0, str.length - 1);
            // document.getElementById('all_questions_in_string').value = quest.substr(0, quest.length - 1);
            quiz.innerHTML = `
      <h1>Thanks . Your Response has been submitted</h1>
      `;
          }
        }, 1000);
      }

      let ttime = (60 * Number(minutes)) + Number(seconds),
        display = document.querySelector('#timeleft');
      startTimer(ttime, display);

      const pertime = Number(questiontotal[currentQuiz].time);
      let display1 = document.querySelector('#questionTimeLeft');
      startTimerQuestion(pertime, display1);
      //RESET TIME
      function resetTimer() {
        const pertime = Number(questiontotal[currentQuiz].time);
        let display1 = document.querySelector('#questionTimeLeft');
        startTimerQuestion(pertime - 1, display1);
      }

      //NEXT BUTTON FEATURE
      btn.addEventListener('click', time());

      //ENTER BUTTON FEATURE
      document.addEventListener('keydown', function (key) {
        if (key.code === 'Enter') {
          time();
        }
      });
    }


    //COMPLETED RELTIME
    var t;
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
          clearInterval(t);
          if (!checkit) {
            for (let i = 0; i < obj.length; i++) {
              console.log(tempmap);
              if (tempmap.get(i) == true) {
                ck(i);
                break;
              }
            }
          }
        }
      }, 1000);
    }
    //ON RELOADING

    let reltime = document.querySelector('#reltime');
    relTime(9, reltime);
    var xa = setInterval(finishcheck, 100);
    function finishcheck() {
      let count = 0;
      for (let i = 0; i < obj.length; i++) {
        if (tempmap.get(i) == false) count++;
      }
      if (count == obj.length) {
        quiz.innerHTML = `<h1>Thanks . Your Response has been submitted</h1>
        ${clicked}`;
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
        document.getElementById('quiz_submit_button').click();
        clearInterval(xa);
      }
    }




  })
  .catch((err) => {
    console.log('rejected', err);
  });
  