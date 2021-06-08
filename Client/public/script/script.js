var blobFile = "dsfsd";
function post_req(url, data){
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    xmlhttp.onreadystatechange = function($evt){
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
            // console.log(xmlhttp.responseText);
            let res = JSON.parse(xmlhttp.responseText);
            console.log("response: ");
            console.log(res);
            resp_data = res;
        }
    }
    xmlhttp.open("POST", url, false);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(data));
}

function openFile(event) {
    var input = event.target;
    console.log(input.files);
    blobFile = input.files[0];

    
    
};


function begin(){
    var formData = new FormData();
    formData.append("image", blobFile);
    console.log(blobFile);
    $.ajax({
        url: "http://0.0.0.0:5000/api/test",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // .. do something
            console.log(response);
            let speech = new SpeechSynthesisUtterance();
            speech.lang = "en";
            speech.text = response.caption;
            window.speechSynthesis.speak(speech);
        },
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        }
    });
}