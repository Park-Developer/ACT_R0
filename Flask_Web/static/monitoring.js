//console.log("Monitoring ON!" , asd);
// [전역 변수 설정]
let ACTIVATED_BTN_NUMBER=1;
let ACTIVATED_COIN_TICKER=DEFAULT_TICKER;

// target 코인만큼 setinverval 하는 기능 구현

// <Chart 관련 전역변수>
let monitoring_time=1500; // 모니터팅 시간
let view_func="get_curPrice"; // View Function 이름
let cur_price_list=[];
let record_time_list=[];
let time=0;

const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',

    data: {
        labels: record_time_list,//['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],

        datasets: [{
            label: ACTIVATED_COIN_TICKER,
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


// [BUTTON EVENT FUNCTION BEGIN]
let Btn_click=function(event){
    let Btn_ClsList=event.target.classList; // <button class="{{coin_ticker}} coin_{{loop.index}}_Btn">show</button>

    let coin_ticker=Btn_ClsList[0];
    let btn_idx=parseInt(Btn_ClsList[1].split('_')[1]);

    console.log("debug",btn_idx,coin_ticker,"  click!");

    // [1] Change Coin
    ACTIVATED_COIN_TICKER=coin_ticker;
    ACTIVATED_BTN_NUMBER=btn_idx;

    // [2] Change Chart
    // [2-1] chart name change
        myChart["data"]["datasets"][0]["label"]=ACTIVATED_COIN_TICKER;

    // [2-2] chart data change
        cur_price_list=[];
        record_time_list=[];
        myChart["data"]["labels"]=record_time_list;
        myChart["data"]["datasets"][0]["data"]=cur_price_list;

    // [3] chart update
    myChart.update();
}

coin_btnList={}
for(let btn_idx=1; btn_idx<=COIN_NUMBER;btn_idx++){
    //console.log("index" , btn_idx);
    let cls_name=".coin_"+btn_idx.toString()+"_Btn"; // class name (.) 주의
    //console.log("NAME",cls_name);

    // DOM Selection
    coin_btnList["Coin_Btn"+btn_idx.toString()]=document.querySelector(cls_name);
    // console.log("deg", document.querySelector(cls_name));

   // Click Event Setting
   coin_btnList["Coin_Btn"+btn_idx.toString()].addEventListener("click",  Btn_click.bind(event));


}


console.log("[DEBUG]"+ coin_btnList["Coin_Btn1"]);
// [BUTTON EVENT FUNCTION END]

//

//

// [CHART BEGIN]____________________________________________________________________
/*


    //let coint_ticker="KRW-BTC"  // Coin ticker 정보



    //dom is fully loaded, but maybe waiting on images & css files
    const ctx = document.getElementById('myChart').getContext('2d');
    myChart = new Chart(ctx, {
        type: 'line',

        data: {
            labels: record_time_list,//['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],

            datasets: [{
                label: ACTIVATED_COIN_TICKER,
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
*/
// [CHART END]____________________________________________________________________

// [UPBIT API BEGIN]____________________________________________________________________
var get_current_priceFunc='load_coinInfo';

console.log("Current Address", document.location.href+get_current_priceFunc );


// The getJSON() method is used to get JSON data using an AJAX HTTP GET request.
// 현재 가격 조회(Unit : 1 초)




setInterval(function() {
    $.getJSON($SCRIPT_ROOT + view_func, // Request URL Function
    {
        coin_ticker: ACTIVATED_COIN_TICKER,//"KRW-BTC",
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
