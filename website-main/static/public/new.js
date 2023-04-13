
    //Correct Option Code
    corr = document.getElementsByClassName("correct")
    A = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for (i = 0; i < corr.length; i++) {
        corr[i].value = A[i]
    }

    //Add Option Code
    document.getElementById("BUTTON").addEventListener('click', () => {
        let check = true;
        let i = 0;
        for (i = 0; i < document.getElementsByClassName('options_written').length; i++) {
            if (document.getElementsByClassName('options_written')[i].value == "") {
                check = false;
                break;
            }
        }
        if (check) {
            ma = document.createElement('div')
            ma.className = "option_line"
            if (document.getElementById('type').value == 's') {
                ma.innerHTML = `<input type="radio" class="correct" name="selection">
            <input class="options_written" value="" placeholder="Option">
            <button type="button" class="delete_opt"><i class="bx bx-trash"></i></button>`
            } else {
                ma.innerHTML = `<input type="checkbox" class="correct" name="selection">
            <input class="options_written" value="" placeholder="Option">
            <button type="button" class="delete_opt"><i class="bx bx-trash"></i></button>`
            }
        } else {
            alert(`Option ${String.fromCharCode(65 + i)} is empty.`);
        }

        document.getElementById("options_doing").append(ma)
        for (i = 0; i < corr.length; i++) {
            corr[i].value = A[i]
        }
    });

    //Question auto size code
    function autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }
    textarea = document.querySelector("#question");
    some = textarea
    some.style.height = 'auto';
    some.style.height = some.scrollHeight + 'px';
    textarea.addEventListener('input', autoResize, false);
    scnd = document.querySelector("#exp");
    some = scnd
    some.style.height = 'auto';
    some.style.height = some.scrollHeight + 'px';
    scnd.addEventListener('input', autoResize, false);


    //Option Deletion Code

    ultag = document.getElementById("options_doing")
    ultag.addEventListener('click', function (e) {
        if (e.target.className == "bx bx-trash") {
            let li = e.target.parentElement.parentElement;
            ultag.removeChild(li);
        }
        for (i = 0; i < corr.length; i++) {
            corr[i].value = A[i]
        }
    });

    sent = ""
    options_wrote = document.getElementsByClassName("options_written")
    for (i = 0; i < options_wrote.length; i++) {
        sent += options_wrote[i].value + '/.\\'
    }
    document.getElementsByClassName("options_all")[0].innerText = sent
    cors = document.getElementsByClassName("correct")
    for (j = 0; j < cors.length; j++) {
        if (cors[j].value == "{{questiondata.correct}}") {
            cors[j].checked = true
        }
    }
    document.getElementById("save_btn").addEventListener("click", (e) => {
        sent = ""
        for (i = 0; i < options_wrote.length; i++) {
            sent += options_wrote[i].value + '/.\\'
        }
//         console.log(sent)
        sent = sent.substr(0, sent.length - 3)
        document.getElementsByClassName("options_all")[0].innerText = sent
        if(document.getElementsByName("type")[0].value != 'i'){
        cor = document.getElementsByClassName("correct")
        state = ""
        for (j = 0; j < cor.length; j++) {
            if (cor[j].checked) {
                state += String.fromCharCode(97 + j) + "+";
            }
        }
        
        for(let i=0;i<options_wrote.length;i++)
        {
            if(options_wrote[i].value == '')
            {
                e.preventDefault();
                alert(`Option ${String.fromCharCode(65 + i)} is empty.`);
            }
        }
        
        if (state == "" && document.getElementById('type').value != "i") {
            e.preventDefault();
            alert("Please choose a correct option");
        }
        document.getElementsByName("correct")[0].value = state.substr(0, state.length - 1)
        // document.getElementById("ending_options").innerHTML = " <textarea data-row=0 class='options_all' name='options' style='display: none;'placeholder='Option'>" + sent.substr(0,sent.length-3) + "</textarea>"
    
        }
        })


    

    function typeselector(indx){
        if (indx == 2) {
            document.getElementsByName("type")[0].selectedIndex = 2;
            document.getElementById("options_doing").style = "display:none";
            document.getElementById("BUTTON").style.display = "none";
            document.getElementById("hide").style.display = "block";
        }
        if (indx == 1) {
            document.getElementsByName("type")[0].selectedIndex = 1;
            document.getElementById("options_doing").style = "display:flex; flex-direction:column;";
            document.getElementById("BUTTON").style.display = "block";
            document.getElementById("hide").style.display = "none";
            document.getElementById("hide").value = "";
            for (let i = 0; i < document.getElementById('options_doing').children.length; i++) {
                let value = document.getElementsByClassName('options_written')[i].value;
                document.getElementById('options_doing').children[i].innerHTML = `<input type="checkbox" class="correct" name="selection"> <input class="options_written" value="${value}" placeholder="Option"> <button type="button" class="delete_opt"><i class="bx bx-trash"></i></button>`;
            }
        }
        if (indx == 0) {
            document.getElementsByName("type")[0].selectedIndex = 0;
            document.getElementById("options_doing").style = "display:flex; flex-direction:column;";
            document.getElementById("BUTTON").style.display = "block";
            document.getElementById("hide").style.display = "none";
            document.getElementById("hide").value = "";
            for (let i = 0; i < document.getElementById('options_doing').children.length; i++) {
                let value = document.getElementsByClassName('options_written')[i].value;
                document.getElementById('options_doing').children[i].innerHTML = `<input type="radio" class="correct" name="selection"> <input class="options_written" value="${value}" placeholder="Option"> <button type="button" class="delete_opt"><i class="bx bx-trash"></i></button>`;
            }
        }
    }
    mai = document.getElementsByName("type")[0]
    mai.addEventListener("change", ()=>{
        typeselector(mai.selectedIndex)
    })
    mai.addEventListener("click", ()=>{typeselector(mai.selectedIndex)})



    //Image Code
    // const file = this.files[0];
    // const  fileType = file['type'];
    // const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
    // if (!validImageTypes.includes(fileType)) {
    //     // invalid file type code goes here.
    // }


