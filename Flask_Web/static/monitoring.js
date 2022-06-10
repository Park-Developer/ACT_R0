console.log("Monitoring ON!");





// [CHART BEGIN]____________________________________________________________________
document.addEventListener("DOMContentLoaded", function(){
    let monitoring_time=1500 // 모니터팅 시간
    let view_func="get_curPrice" // View Function 이름
    //let coint_ticker="KRW-BTC"  // Coin ticker 정보

    let cur_price_list=[]
    let record_time_list=[]
    let time=0

    //dom is fully loaded, but maybe waiting on images & css files
    console.log("ADDLISTSTs");
    const ctx = document.getElementById('myChart').getContext('2d');

    const myChart = new Chart(ctx, {
        type: 'line',

        data: {
            labels: record_time_list,//['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],

            datasets: [{
                label: 'My First Dataset',
                data: cur_price_list,//[65, 59, 80, 81, 56, 55],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }

        }); // chart setting

// [CHART END]____________________________________________________________________

// [UPBIT API BEGIN]____________________________________________________________________
var get_current_priceFunc='load_coinInfo';

console.log("Current Address", document.location.href+get_current_priceFunc );


// The getJSON() method is used to get JSON data using an AJAX HTTP GET request.
// 현재 가격 조회(Unit : 1 초)


// target 코인만큼 setinverval 하는 기능 구현
setInterval(function() {
    $.getJSON($SCRIPT_ROOT + view_func,
    {
        coin_ticker: "KRW-BTC",
        //b: $('input[name="b"]').val()
    },
    function(data) {
          console.log(data)
          // Current Price Record
          cur_price_list.push(data)

          // Current Time Record
          time=time+1
          record_time_list.push(time)
        $("#result").text(data.result);
        myChart.update(); // chart update
        if (time>=1001){
            cur_price_list=[]
            record_time_list=[]
        }
    })},
    monitoring_time);
// [UPBIT API END]____________________________________________________________________


});
