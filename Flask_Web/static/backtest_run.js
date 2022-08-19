/* VARIABLE SETTING */
let get_backtestData_URL="http://127.0.0.1:5000/backtest/get_backtestData"
let backtest_chartInfo={
  "candletimeKST":[],
  "high_price":[],
  "opening_price":[],
  "timestamp":[],
  "trade_price":[]
};

/* DOM SETTING */
console.log("setting js",document.location.href);





console.log("url splti");
console.log( get_targetID_from_CurURL());
console.log("url splti");

let backtest_run__btn_DOM=document.querySelector(".backtest_test_run__btn");

let backtest_market__val_DOM=document.querySelector(".backtest_market__val")
let backtest_data_unit__val_DOM=document.querySelector(".backtest_data_unit__val")
let backtest_data_number__val_DOM=document.querySelector(".backtest_data_number__val")
let backtest_speed__val_DOM=document.querySelector(".backtest_speed__val")

let backtest_maxPrice__val_DOM=document.querySelector(".backtest_maxPrice__val")
let backtest_minPrice__val_DOM=document.querySelector(".backtest_minPrice__val")
let backtest_averagePrice__val_DOM=document.querySelector(".backtest_averagePrice__val")

let backtest_dataNumber__val_DOM=document.querySelector(".backtest_dataNumber__val");

/* CHART SETTING */
const chart_dom = document.getElementById('backtest_Chart').getContext('2d');

const backtestChart = new Chart(chart_dom, {
    type: 'line',

    data: {
        labels: backtest_chartInfo["timestamp"],

        datasets: [
            { // DATA1 : 선택된 코인의 현재가
            label: backtest_market__val_DOM.innerText,
            data: backtest_chartInfo["trade_price"], // Y axis data1
            fill: false,
            borderColor: CHART_INFO.graph_line_color[0],//'rgb(75, 192, 192)',
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
                  text: 'Trade Price(KRW)'
                },
                beginAtZero: false,

            }
        }
    }
}); // chart setting


// Define Simualtion Function
function simulate_backtest(){
  $.getJSON(
    // (1) Request URL
    get_backtestData_URL,
    // (2) Request Parameter
    {
      target_coin_id:get_targetID_from_CurURL(), // 현재 URL로부터 Target id 추출
      market:backtest_market__val_DOM.innerText,
      data_unit:backtest_data_unit__val_DOM.innerText,
      data_number:backtest_data_number__val_DOM.innerText
    },
    // (3) Data Handling Function
    function(data){
      // 1. Receive Data from python view function responnd
      backtest_chartInfo["candletimeKST"]=data["candle_date_time_kst"];
      backtest_chartInfo["high_price"]=data["high_price"];
      backtest_chartInfo["low_price"]=data["low_price"];
      backtest_chartInfo["opening_price"]=data["opening_price"];
      backtest_chartInfo["timestamp"]=data["timestamp"];
      backtest_chartInfo["trade_price"]=data["trade_price"];

      // 2. Updaye Chart Data
      backtestChart["data"]["labels"]=backtest_chartInfo["candletimeKST"];

      // 1st data updayr => chart_index : 0
      backtestChart["data"]["datasets"][0]["data"]=backtest_chartInfo["trade_price"];

      // update chart UI
      backtestChart.update();

      // 3. Update Monitoring Data
      backtest_maxPrice__val_DOM.innerText=Math.max(...backtest_chartInfo["trade_price"]);
      backtest_minPrice__val_DOM.innerText=Math.min(...backtest_chartInfo["trade_price"]);
      backtest_averagePrice__val_DOM.innerText=get_AVG(backtest_chartInfo["trade_price"]);
      
    }
  )


}


// Execute Simulation Function
simulate_backtest();
