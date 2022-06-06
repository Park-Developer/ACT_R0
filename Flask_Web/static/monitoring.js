console.log("Monitoring ON!");

var get_current_priceFunc='load_coinInfo';

console.log("Current Address", document.location.href+get_current_priceFunc );




setTimeout(function() {
console.log("RUN INFO")
var load_funcURL= document.location.href+get_current_priceFunc;
var xhr = new XMLHttpRequest();
xhr.overrideMimeType("application/json");
xhr.open('GET', load_funcURL);

xhr.onreadystatechange = function() {
    // [1] Text를 받는 경우
    /*
    var all_lines = xhr.responseText; // delimiter
    console.log("all_lines : ", all_lines);
    if (xhr.readyState == XMLHttpRequest.DONE) {
        alert("The End of Stream");
    }
    */
    var json_info2 = xhr.responseText;
    console.log("asdg" , json_info2);

    if (xhr.readyState == XMLHttpRequest.DONE) {
      // [2] JSON을 받는 경우
    var json_info = xhr.responseText;
    var parsed_data=JSON.parse(json_info);

    console.log("[json info] : ", parsed_data);
    //console.log("[json info] : ", parsed_data.birth);
     //   console.log("[json info] : ", parsed_data.age);
        alert("The End of Stream");
    }
}
xhr.send();


}, 6000);