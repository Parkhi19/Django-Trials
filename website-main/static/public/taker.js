function copyurl() {
    var dummy = document.createElement('input'),
        text = window.location.href+'test';
        
               alert ("Link is copied");
       
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);
}
