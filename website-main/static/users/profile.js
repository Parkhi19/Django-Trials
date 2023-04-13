

//PROFILES
const showModal = document.querySelectorAll('.show-modal');
const closeModal = document.querySelector('.close-modal');
const modal = document.querySelector('.modal');
const overlay = document.querySelector('.overlay');

let node = document.getElementById('txtarea').value;
if (node == 1) {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/dxjqoygy.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
} else if (node == 2) {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/eszyyflr.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
} else if (node == 3) {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/bwnhdkha.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
} else if (node == 4) {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/ntformof.json" trigger="loop"  colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
} else if (node == 5) {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/nobciafz.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
}

document.getElementById('1th').addEventListener('click', function () {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/dxjqoygy.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
    document.getElementById('txtarea').value = 1;
    removeHidden();
});
document.getElementById('2th').addEventListener('click', function () {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/eszyyflr.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
    document.getElementById('txtarea').value = 2;
    removeHidden();
});
document.getElementById('3th').addEventListener('click', function () {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/bwnhdkha.json" trigger="loop"  colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
    document.getElementById('txtarea').value = 3;
    removeHidden();
});
document.getElementById('4th').addEventListener('click', function () {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/ntformof.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
    document.getElementById('txtarea').value = 4;
    removeHidden();
});
document.getElementById('5th').addEventListener('click', function () {
    document.getElementById('mainprofile').innerHTML = '<lord-icon src="https://cdn.lordicon.com/nobciafz.json" trigger="loop"   colors="primary:#ffffff,secondary:#ffffff" style="width:250px;height:250px"></lord-icon>';
    document.getElementById('txtarea').value = 5;
    removeHidden();
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
