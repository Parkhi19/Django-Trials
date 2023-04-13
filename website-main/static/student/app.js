fetch(window.location.href + 'get_question/').then(response => response.json())
      .then(obj => {
        document.addEventListener("visibilitychange", event => {
            if (document.visibilityState == "visible") {
              console.log("tab is active")
            } else {
              alert('Test will be submitted if you change the tab again')
            }
          })
        var totalTime = "05:00";
        var perTime = "01:00";
        var subject = "General";
        var totalQuestions = 5;
        console.log(obj)
        'use strict mode'

        //HELP BUTTON
        {
          const showModal = document.querySelector('#helpme');
          const closeModal = document.querySelector('.close-modal');
          const modal = document.querySelector('.modal');
          const overlay = document.querySelector('.overlay');

          const addHidden = function () {
            modal.classList.remove('hidden');
            overlay.classList.remove('hidden');
          };

          showModal.addEventListener('click', addHidden);

          const removeHidden = function () {
            modal.classList.add('hidden');
            overlay.classList.add('hidden');
          };

          closeModal.addEventListener('click', removeHidden);
          overlay.addEventListener('click', removeHidden);

          document.addEventListener('keydown', function (key) {
            if (key.code === 'Escape') {
              if (!modal.classList.contains('hidden')) {
                removeHidden();
              }
            }
          });
        }

        const quiz = document.getElementById('quiz'),
          answerEls = document.querySelectorAll('.answer'),
          answerElmul = document.querySelectorAll('.answermul'),
          questionEl1 = document.getElementById('question1'),
          questionEl2 = document.getElementById('question2'),
          questionEl3 = document.getElementById('question3'),
          a_text = document.getElementById('a_text'),
          b_text = document.getElementById('b_text'),
          c_text = document.getElementById('c_text'),
          d_text = document.getElementById('d_text'),
          btn = document.getElementById('submit'),
          progressBarFull = document.getElementById('progressBarFull'),
          a_mul = document.getElementById('a_mul'),
          b_mul = document.getElementById('b_mul'),
          c_mul = document.getElementById('c_mul'),
          d_mul = document.getElementById('d_mul'),
          sub = document.getElementById('subject');

        let currentQuiz = 0,
          questionCounter = 0,
          score = 0,
          questionNumber = 0,
          timeLeft = document.getElementById("timeLeft").textContent,
          questionTimeLeft = document.getElementById("questionTimeLeft"),
          minutes = totalTime.substr(0, 2),
          seconds = totalTime.substr(3);

        let arr = new Array,
          clicked = new Array;
        let questiontotal = obj.ques;

        let Questions = obj.ques;

        let mcqmap = new Map();
        let numericmap = new Map();
        let multimap = new Map();

        let questionmap = new Map();

        // sub.textContent = `${subject} Quiz`;

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
            deselectAnswers();
            const currentQuizData = questiontotal[currentQuiz];
            questionEl1.innerText = currentQuizData.question;
            a_text.innerText = currentQuizData.options.opt_1;
            b_text.innerText = currentQuizData.options.opt_2;
            c_text.innerText = currentQuizData.options.opt_3;
            d_text.innerText = currentQuizData.options.opt_4;
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
            deselectAnswersMul();
            const currentQuizData = questiontotal[currentQuiz];
            questionEl3.innerText = currentQuizData.question;
            a_mul.innerText = currentQuizData.options.opt_1;
            b_mul.innerText = currentQuizData.options.opt_2;
            c_mul.innerText = currentQuizData.options.opt_3;
            d_mul.innerText = currentQuizData.options.opt_4;
          }
        }

        //DESELECTING ANSWERS 
        function deselectAnswers() {
          answerEls.forEach((answerEl) => (answerEl.checked = false));
        }

        //DESELECTING ANSWERS MULTIPLE
        function deselectAnswersMul() {
          answerElmul.forEach((answerEl) => (answerEl.checked = false));
        }

        //SELECTING ANSWERS SINGLE CORRECT
        function getSelectedMcq() {
          let answer;
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
            arr.push(answer);
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

        var x, y;
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
              }
              else {
                console.log(clicked);
                clearInterval(y);
                // removeHidden();
                quiz.innerHTML = `
      <h2>Thanks . Your Response has been submitted</h2>
      `;
              }
            }
          }, 1000);
        }

        //TOTAL TIME LEFT
        function startTimer(duration, display) {
          shuffle(questiontotal);
          console.log('doing')
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
              // removeHidden();
              quiz.innerHTML = `
      <h2>Thanks . Your Response has been submitted</h2>
      `;
              console.log(clicked);
            }
          }, 1000);
        }

        //ON RELOADING
          const pertime = Number(questiontotal[currentQuiz].time);
          let display1 = document.querySelector('#questionTimeLeft');
          startTimerQuestion(pertime, display1);

          let time = (60 * Number(minutes)) + Number(seconds),
            display = document.querySelector('#timeLeft');
          startTimer(time, display);

        //RESET TIME
        function resetTimer() {
          // const pertime = 60*Number(perTime.substr(0,2)) + Number(perTime.substr(3));
          const pertime = Number(questiontotal[currentQuiz].time);
          let display1 = document.querySelector('#questionTimeLeft');
          startTimerQuestion(pertime - 1, display1);
        }

        //NEXT BUTTON FEATURE
        btn.addEventListener('click', function () {
          questionTimeLeft.textContent = perTime;
          checkanswer();
          clearInterval(x);
          currentQuiz++;
          if (currentQuiz < totalQuestions) {
            loadQuiz();
            resetTimer();
          }
          else {
            clearInterval(y);
            console.log(clicked);
            quiz.innerHTML = `
      <h2>Thanks . Your Response has been submitted</h2>
      `;
          }
        });
      })
      .catch((err) => {
        console.log('rejected', err);
      });