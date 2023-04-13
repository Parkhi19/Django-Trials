var totalTime = "05:00";
var perTime = "01:00";
var subject = "General";
var totalQuestions = 5;



  getresponse = fetch(window.location.href + 'get_question/').then(response => response.json())
  .then(data => {
      var obj = data


  })
  .catch((err) => {
      console.log('rejected', err);
  });