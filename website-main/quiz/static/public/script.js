const finish = document.getElementById('btn'),
mcq = document.getElementById('S'),
mul = document.getElementById('M'),
num = document.getElementById('I');

function addingoption(){
    
}


try{
document.getElementById('type').addEventListener('click',function(){
    if(document.getElementById('type').value == 's')
    {
        document.getElementById('options_doing').style.display = "inline";
        document.getElementById('options_all').innerText = ''
    }
    if(document.getElementById('type').value == 'm')
    {
        document.getElementById('options_doing').style.display = "inline";
        document.getElementById('options_all').innerText = ''
    }
    if(document.getElementById('type').value == 'i')
    {
        document.getElementById('options_doing').style.display = "none";
        document.getElementById('options_all').innerText = '_null_';    
    }
});
}
catch{
}

