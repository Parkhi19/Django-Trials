
 let ele = document.getElementsByClassName("fa fa-star star"); 
 for(let i=0;i<ele.length;i++) 
 { 
     ele[i].addEventListener('click',function(){ 
         for(let j=0;j<ele.length;j++) 
         { 
             ele[j].style.color = "black"; 
         } 
         for(let j=0;j<=i;j++) 
         { 
             ele[j].style.color = "orange"; 
         } 
     }); 
 } 
 let ele2 = document.getElementsByClassName("fa fa-star star2"); 
 for(let i=0;i<ele.length;i++) 
 { 
     ele2[i].addEventListener('click',function(){ 
         for(let j=0;j<ele2.length;j++) 
         { 
             ele2[j].style.color = "black"; 
         } 
         for(let j=0;j<=i;j++) 
         { 
             ele2[j].style.color = "orange"; 
         } 
     }); 
 } 