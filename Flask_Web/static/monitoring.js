console.log("Monitoring ON!");

var xhr = new XMLHttpRequest();
xhr.open('GET', "{{ url_for('./monitoring/load_coinInfo') }}");

xhr.onreadystatechange = function() {

    var all_lines = xhr.responseText; // delimiter
    console.log("all_lines : ", all_lines);

    if (xhr.readyState == XMLHttpRequest.DONE) {
        alert("The End of Stream");

    }
}

xhr.send();
