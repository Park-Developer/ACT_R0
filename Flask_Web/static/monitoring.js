// [DOM 객체 선언]
let monotoring_time_val_DOM=document.querySelector(".TARGET_MONITORING__time__val");
let monotoring_curPrice_val_DOM=document.querySelector(".TARGET_MONITORING__curPrice__val");
let monotoring_avgPrice_val_DOM=document.querySelector(".TARGET_MONITORING__avgPrice__val");
let monotoring_maxPrice_val_DOM=document.querySelector(".TARGET_MONITORING__maxPrice__val");
let monotoring_minPrice_val_DOM=document.querySelector(".TARGET_MONITORING__minPrice__val");

// [설정 변수]
let CHART_INFO={
  graph_line_color:[
    'rgb(57, 106, 177)', // blue
    'rgb(218, 124, 48)', // orange
    'rgb(62, 150, 81)',  // green
    'rgb(204, 37, 41)',  // red
    'rgb(83, 81, 84)',   // gray
    'rgb(107, 76, 154)', // purple
    'rgb(146, 36, 40)',  // wine
    'rgb(148, 139, 61)'  // gold
  ],

  monitoring_time:1500, // 모니터팅 시간
  view_func : "get_curPrice", // request 요청하는 파이썬 함수 이름
  first_moving_average_count : 20, // 첫번째 이평선 계산 기준
}

// [Button 설정]
let BUTTON_SET={
  clicked_btn_Class: "clicked_btn_style",
  unclicked_btn_Class: "unclicked_btn_style",
}


// [전역 변수 설정]
let ACTIVATED_BTN_NUMBER=1;
let ACTIVATED_COIN_TICKER=DEFAULT_TICKER;


// <Chart 관련 전역변수>

let cur_price_list=[];
let moving_avg1_list=[]; // 이평선1(기준 미정)
let moving_avg2_list=[]; // 이평선2(기준 미정)
let record_time_list=[];
let chart_time=0; // chart의 X축 변수(record time)

// HTML 반영
monotoring_time_val_DOM.innerHTML=CHART_INFO.monitoring_time.toString();


// [CHART GENERATION]
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',

    data: {
        labels: record_time_list,

        datasets: [
            { // DATA1 : 선택된 코인의 현재가
            label: ACTIVATED_COIN_TICKER,
            data: cur_price_list, // Y axis data1
            fill: false,
            borderColor: CHART_INFO.graph_line_color[0],//'rgb(75, 192, 192)',
            tension: 0.1
            },
            { // DATA2 : 선택된 코인의 현재 가격의 평균
            label: ACTIVATED_COIN_TICKER+" - MV Avg("+CHART_INFO.first_moving_average_count.toString()+")", // 선택된 코인의 현재가 실시간 그래프화
            data: moving_avg1_list, // Y axis data2
            fill: false,
            borderColor: CHART_INFO.graph_line_color[1],
            tension: 0.1
            }
        ]
    },
    options: {
        scales: {
            x: {
                title: {
                  display: true,
                  text: 'Time'
                },
            },
            y: {
                title: {
                  display: true,
                  text: 'Current Price'
                },
                beginAtZero: false,

            }
        }
    }
}); // chart setting

function change_clicked_Style(btn_cls_name, clicked_style_cls){
    let clicked_btn=document.querySelector(btn_cls_name);

    clicked_btn.classList.add(clicked_style_cls); // add click style

}

function change_Unclicked_Style(btn_cls_name, clicked_style_cls){
    let unclicked_btn=document.querySelector(btn_cls_name);

    unclicked_btn.classList.remove(clicked_style_cls); // remove click style

}


// [BUTTON EVENT FUNCTION BEGIN]
let Btn_click=function(event){
    let Btn_ClsList=event.target.classList; // <button class="{{coin_ticker}} coin_{{loop.index}}_Btn">show</button>

    let coin_ticker=Btn_ClsList[0]; // new click
    let btn_idx=parseInt(Btn_ClsList[1].split('_')[1]);

    console.log("debug",btn_idx,coin_ticker,"  click!");

    // [1] Change Coin(= Button Change)
    past_clicked_Btn_ticker=ACTIVATED_COIN_TICKER
    past_clicked_Btn_idx=ACTIVATED_BTN_NUMBER

    ACTIVATED_COIN_TICKER=coin_ticker;
    ACTIVATED_BTN_NUMBER=btn_idx;

    let unclicked_Btn_cls="."+"coin_"+past_clicked_Btn_idx+"_Btn"; // Past clicked Button
    let clicked_Btn_cls="."+"coin_"+btn_idx+"_Btn";

    // Now clicked Button
    change_clicked_Style(btn_cls_name=clicked_Btn_cls,clicked_style_cls=BUTTON_SET.clicked_btn_Class);
    change_Unclicked_Style(btn_cls_name=unclicked_Btn_cls,clicked_style_cls=BUTTON_SET.clicked_btn_Class);

    // [2] Change Chart
    // [2-1] chart name change
        myChart["data"]["datasets"][0]["label"]=ACTIVATED_COIN_TICKER;
        myChart["data"]["datasets"][1]["label"]=ACTIVATED_COIN_TICKER+" - MV Avg("+CHART_INFO.first_moving_average_count.toString()+")"
    // [2-2] chart data change
        record_time_list=[];
        chart_time=0; // 이름바꾸자

        cur_price_list=[];
        moving_avg1_list=[]
        moving_avg2_list=[]

        myChart["data"]["labels"]=record_time_list;
        myChart["data"]["datasets"][0]["data"]=cur_price_list; // 첫 번쨰 데이터
        myChart["data"]["datasets"][1]["data"]=moving_avg1_list; // 두 번쨰 데이터

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


// [UPBIT API BEGIN]____________________________________________________________________
var get_current_priceFunc='load_coinInfo';

console.log("Current Address", document.location.href+get_current_priceFunc );


// The getJSON() method is used to get JSON data using an AJAX HTTP GET request.
// 현재 가격 조회(Unit : 1 초)


setInterval(function() {
    $.getJSON($SCRIPT_ROOT + CHART_INFO.view_func, // Request URL Function
    {
        coin_ticker: ACTIVATED_COIN_TICKER,//"KRW-BTC",
        //b: $('input[name="b"]').val()
    },
    function(data) {
          console.log(data);

          // (1) Current Time Record
          chart_time=chart_time+1;
          record_time_list.push(chart_time);

          // (2) Current Price Record
          cur_price_list.push(data);
          monotoring_curPrice_val_DOM.innerHTML=data;
          monotoring_avgPrice_val_DOM.innerHTML=get_AVG(cur_price_list);

          // (3) Moving Averageg1 Record
          if(chart_time<CHART_INFO.first_moving_average_count){
            moving_avg1_list.push(get_AVG(cur_price_list));
          }else{
            let mv_avg_range=cur_price_list.slice(chart_time-CHART_INFO.first_moving_average_count+1);
            moving_avg1_list.push(get_AVG(mv_avg_range));
          }

        $("#result").text(data.result);
        myChart.update(); // chart update
        if (chart_time>=1001){
            cur_price_list=[];
            record_time_list=[];
        }
    })},
    CHART_INFO.monitoring_time
);
// [UPBIT API END]____________________________________________________________________
