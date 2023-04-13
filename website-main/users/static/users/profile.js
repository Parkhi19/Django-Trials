// Javascript for navbar 

const mainMenu = document.querySelector('.mainMenu');
const closeMenu = document.querySelector('.closeMenu');
const openMenu = document.querySelector('.openMenu');


openMenu.addEventListener('click', show);
closeMenu.addEventListener('click', close);

function show() {
    mainMenu.style.display = 'flex';
    mainMenu.style.top = '0';
}

function close() {
    mainMenu.style.top = '-100%';
}

//PROFILES
const showModal = document.querySelectorAll('.show-modal');
const closeModal = document.querySelector('.close-modal');
const modal = document.querySelector('.modal');
const overlay = document.querySelector('.overlay');

document.getElementById('first').addEventListener('click', function () {
    console.log(1);c
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/dxjqoygy.json" trigger="loop"  colors="primary:#ffffff,secondary:#ffffff" ></lord-icon>';
    removeHidden()
});
document.getElementById('second').addEventListener('click', function () {
    console.log(1);
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/eszyyflr.json" trigger="loop" colors="primary:#ffffff,secondary:#ffffff" ></lord-icon>';
    removeHidden()
});
document.getElementById('third').addEventListener('click', function () {
    console.log(1);
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/bwnhdkha.json" trigger="loop" colors="primary:#ffffff,secondary:#ffffff"  ></lord-icon>';
    removeHidden()
});
document.getElementById('fourth').addEventListener('click', function () {
    console.log(1);
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/ntformof.json" trigger="loop"  colors="primary:#ffffff,secondary:#ffffff" ></lord-icon>';
    removeHidden()
});
document.getElementById('fifth').addEventListener('click', function () {
    console.log(1);
    
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/nobciafz.json" trigger="loop"  colors="primary:#ffffff,secondary:#ffffff" ></lord-icon>';
    removeHidden()
});

const addHidden = function () {
    modal.classList.remove('hidden');
    overlay.classList.remove('hidden');
};

for (let i = 0; i < showModal.length; i++) {
    showModal[i].addEventListener('click', addHidden);
}

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