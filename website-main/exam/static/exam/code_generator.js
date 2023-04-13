function gotolink() {
    code = document.getElementById("link_box").value
    if (code.length == 12){
        address = '../c/'+code+'/test'
        console.log(address)
        document.getElementById("botton1").href = address
        document.getElementById("botton1").style.color = "red"
        document.getElementById("botton1").style.display = "inline-block"
    }
}