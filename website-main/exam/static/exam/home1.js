// loader javascript  

var preload = document.getElementById("loader_container");
var navbar = document.getElementById("navbar");
var slider = document.getElementById("slider");
function myfunction() {
    preload.style.display = "none";
    navbar.classList.toggle("active");
   

}


// Javascript for navbar 

const mainMenu = document.querySelector('.mainMenu');
const closeMenu = document.querySelector('.closeMenu');
const openMenu = document.querySelector('.openMenu');




openMenu.addEventListener('click',show);
closeMenu.addEventListener('click',close);

function show(){
    mainMenu.style.display = 'flex';
    mainMenu.style.top = '0';
}
function close(){
    mainMenu.style.top = '-100%';
}

// javascript of why us section

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides((slideIndex += n));
}

function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) { 
  var i; 
  var slides = document.getElementsByClassName("mySlides"); 
  var dots = document.getElementsByClassName("dot"); 
  if (n > slides.length) { 
    slideIndex = 1; 
  } 
  if(slideIndex<1) { 
    slideIndex = slides.length; 
  } 
  for (i = 0; i < slides.length; i++) { 
    slides[i].style.display = "none"; 
  } 
  for (i = 0; i < dots.length; i++) { 
    dots[i].className = dots[i].className.replace(" active", ""); 
  } 
  slides[slideIndex - 1].style.display = "block"; 
  dots[slideIndex - 1].className += " active"; 
}

function none(){
  slideIndex+=1
  showSlides(slideIndex);
}

setInterval(none,8000);



