// const finish = document.getElementById('btn'),
//     mcq = document.getElementById('S'),
//     mul = document.getElementById('M'),
//     num = document.getElementById('I');

// function addingoption(x) {
//     add_new_btn = document.getElementById("BUTTON")
//     x = x + 1
//     add_new_btn.outerHTML = option(x)
//     return x
// }

// function option(x) {
//     html = '<input data-row=0 class="options resize fix" id="options_'+x+'" placeholder="Option '+x+'"><button class="boton2" id="BUTTON" onclick=addingoption('+x+')>Add option</button>'
//     return html
// }

// try {
//     document.getElementById('type').addEventListener('click', function () {
//         if (document.getElementById('type').value == 's') {
//             document.getElementById('options_doing').style.display = "inline";
//             let j = 1
//             while (true) {
//                 try {
//                     document.getElementById('options_' + j).outerHTML = '<textarea data-row=0 name="options" class="options" id="options_1" placeholder="Options"></textarea>'
//                 } catch {
//                     break
//                 }
//             }
//         }
//         if (document.getElementById('type').value == 'm') {
//             document.getElementById('options_doing').style.display = "inline";
//             while (true) {
//                 try {
//                     document.getElementById('options_' + j).outerHTML = '<textarea data-row=0 name="options" class="options" id="options_1" placeholder="Options"></textarea>'
//                 } catch {
//                     break
//                 }
//             }
//         }
//         if (document.getElementById('type').value == 'i') {
//             document.getElementById('options_doing').style.display = "none";
//             document.getElementById('options_all').outerHTML = '<textarea data-row=0 name="options" class="options" id="options_1" placeholder="Options">_null_</textarea>';
//         }
//     });
// }
// catch {

// }
// setInterval(() => {
//     k = 0
//     while (1) {
//         try {
//             if (k != 1) {
//                 statement += '/.\\';
//             }
//             statement += document.getElementById('options_' + k).innerText;
//         } catch {
//             break;
//         }
//         k += 1
//         k++;
//     }
//     document.getElementById("options_all").innerText = statement
// },10000);
// document.getElementById('save_btn').addEventListener('click',function(){
//     var x = document.getElementsByClassName('options');
//     let ans = new String;
//     for(let i=0;i<x.length;i++)
//     {
//         ans += x[i].value + "/.\\";
//     }
//     console.log(ans);
// });
// let y = document.getElementsByClassName("correct");
// let x = document.getElementsByClassName("options");
// let z = document.getElementsByClassName("options_section");

// for (let i = 0; i < z.length; i++) {
//   let your = z[i].children[z[i].children.length - 3].textContent,
//     real = z[i].children[z[i].children.length - 2].textContent;
//   if(isFinite(real))
//   {
//     if(real == your)
//     {
//       z[i].children[0].style.backgroundColor = "#15bf15";
//       z[i].children[0].style.color = "white";
//       z[i].children[0].value = real;
//     }
//     else 
//     {
//       z[i].children[0].style.backgroundColor = "#f44444";
//       z[i].children[0].value = real;
//     }
//     z[i].children[1].textContent = `Correct Answer : ${real}`;
//   }
//   else{    
//     z[i].children[z[i].children.length - 3].style.display = "none";
//     z[i].children[z[i].children.length - 2].style.display = "none";
//     if(your.length){
//       let yours = your.split("+");
//       for (let j = 0; j < yours.length; j++) {
//         // console.log(z[i].children[yours[j].charCodeAt() - 97].children[0]);
//         z[i].children[yours[j].charCodeAt() - 97].children[0].checked = true;
//         z[i].children[yours[j].charCodeAt() - 97].style.backgroundColor = "#f44444";
//         z[i].children[yours[j].charCodeAt() - 97].style.color = "white";
//       }
//     }
//       let reals = real.split("+");
//       for (let j = 0; j < reals.length; j++) {
//         if(z[i].children[reals[j].charCodeAt() - 97].style.backgroundColor == "#f44444")z[i].children[reals[j].charCodeAt() - 97].style.backgroundColor = "#15bf15";
//         else z[i].children[reals[j].charCodeAt() - 97].style.backgroundColor = "#15bf15";
//         z[i].children[reals[j].charCodeAt() - 97].style.color = "white";
//       }
//   }
// }

const finish = document.getElementById("btn"),
  mcq = document.getElementById("S"),
  mul = document.getElementById("M"),
  num = document.getElementById("I");

function addingoption() {}

try {
  document.getElementById("type").addEventListener("click", function () {
    if (document.getElementById("type").value == "s") {
      document.getElementById("options_doing").style.display = "inline";
      document.getElementById("options_all").innerText = "";
    }
    if (document.getElementById("type").value == "m") {
      document.getElementById("options_doing").style.display = "inline";
      document.getElementById("options_all").innerText = "";
    }
    if (document.getElementById("type").value == "i") {
      document.getElementById("options_doing").style.display = "none";
      document.getElementById("options_all").innerText = "_null_";
    }
  });
} catch {}

let y = document.getElementsByClassName("correct");
let x = document.getElementsByClassName("options");
let z = document.getElementsByClassName("options_section");

for (let i = 0; i < z.length; i++) {
  let your = z[i].children[z[i].children.length - 3].textContent,
    real = z[i].children[z[i].children.length - 2].textContent;
  if(isFinite(real))
  {
    if(real == your)
    {
      z[i].children[0].style.backgroundColor = "#15bf15";
      z[i].children[0].style.color = "white";
      z[i].children[0].value = real;
    }
    else 
    {
      z[i].children[0].style.backgroundColor = "#f44444";
      z[i].children[0].value = real;
    }
    z[i].children[1].textContent = `Correct Answer : ${real}`;
  }
  else{    
    z[i].children[z[i].children.length - 3].style.display = "none";
    z[i].children[z[i].children.length - 2].style.display = "none";
    if(your.length){
      let yours = your.split("+");
      for (let j = 0; j < yours.length; j++) {
        // console.log(z[i].children[yours[j].charCodeAt() - 97].children[0]);
        z[i].children[yours[j].charCodeAt() - 97].children[0].checked = true;
        z[i].children[yours[j].charCodeAt() - 97].style.backgroundColor = "#f44444";
        z[i].children[yours[j].charCodeAt() - 97].style.color = "white";
      }
    }
      let reals = real.split("+");
      for (let j = 0; j < reals.length; j++) {
        if(z[i].children[reals[j].charCodeAt() - 97].style.backgroundColor == "#f44444")z[i].children[reals[j].charCodeAt() - 97].style.backgroundColor = "#15bf15";
        else z[i].children[reals[j].charCodeAt() - 97].style.backgroundColor = "#15bf15";
        z[i].children[reals[j].charCodeAt() - 97].style.color = "white";
      }
  }
}
