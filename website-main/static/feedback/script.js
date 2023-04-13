
 

   let ele1 = document.getElementsByClassName("fa fa-star star");
   for (let i = 0; i < ele1.length; i++) {
     ele1[i].addEventListener('click', function () {
       for (let j = 0; j < ele1.length; j++) {
         ele1[j].style.color = "black";
       }
       for (let j = 0; j <= i; j++) {
         ele1[j].style.color = "orange";
       }
       document.getElementsByName("star1")[0].innerText = String(parseInt(i) + 1);
     });
   }
   let ele2 = document.getElementsByClassName("fa fa-star star2");
   for (let i = 0; i < ele2.length; i++) {
     ele2[i].addEventListener('click', function () {
       for (let j = 0; j < ele2.length; j++) {
         ele2[j].style.color = "black";
       }
       for (let j = 0; j <= i; j++) {
         ele2[j].style.color = "orange";
       }
       document.getElementsByName("star2")[0].innerText = String(parseInt(i) + 1);
     });
   }

//    let score = 0,
//      totalquestions = 0,
//      rot = "unknown",
//      attempted = 0,
//      notattempted = totalquestions - attempted,
//      correct = 0;
//    document.getElementById('score').textContent = `${score}/${totalquestions}`;
//    document.getElementById('rot').textContent = `Result opening time: ${rot}`;
//    document.getElementById('totalquestions').textContent = `Total number of questions: ${totalquestions}`;
//    document.getElementById('attempted').textContent = `Attempted questions: ${attempted}`;
//    document.getElementById('notattempted').textContent = `Questions not attempted: ${notattempted}`;
//    document.getElementById('correct').textContent = `Correctly answered questions: ${correct}`;
  
