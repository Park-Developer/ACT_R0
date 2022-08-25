/* ___________[ VARIABLE SETTING ]___________ */
let get_backtestData_URL="http://127.0.0.1:5000/backtest/get_backtestData"
let backtest_chartInfo={
  "candletimeKST":[],
  "high_price":[],
  "opening_price":[],
  "timestamp":[],
  "trade_price":[]
};

let training_chartInfo={
  "candletimeKST":[],
  "high_price":[],
  "opening_price":[],
  "timestamp":[],
  "trade_price":[]
};

/* ___________[ DOM SETTING ]___________ */
let backtest_run__btn_DOM=document.querySelector(".backtest_test_run__btn");

// (1) User Setting DOM
let backtest_usersetting__market__val_DOM=document.querySelector(".backtest_usersetting__market__val");
let backtest_usersetting_unit__val_DOM=document.querySelector(".backtest_usersetting__unit__val");
let backtest_usersetting_period__val_DOM=document.querySelector(".backtesting_usersetting_period__val");
let backtest_usersetting_monitoringtime__val_DOM=document.querySelector(".backtesting_usersetting_monitoringtime__val");
let backtest_usersetting_datanumber__val_DOM=document.querySelector(".backtesting_usersetting_datanumber__val");

// (2) Training Data DOM
let backtest_trainingdata_period__val =document.querySelector(".backtest_trainingdata_period__val");
let backtest_trainingdata_dataUnit__val=document.querySelector(".backtest_trainingdata_dataUnit__val");
let backtest_trainingdata_dataNumber_val=document.querySelector(".backtest_trainingdata_dataNumber_val");

let training_starttime__val=document.querySelector(".backtest_trainingdata_starttime__val");
let training_endtime__val=document.querySelector(".backtest_trainingdata_endtime__val");

let training_maxPrice__val_DOM=document.querySelector(".backtest_trainingdata_maxPrice__val");
let training_minPrice__val_DOM=document.querySelector(".backtest_trainingdata_minPrice__val");
let training_avgPrice__val_DOM=document.querySelector(".backtest_trainingdata_averagePrice__val");

// (3) Simulation Data DOM
let simulation_starttime__val=document.querySelector(".backtest_simulationdata_starttime__val");
let simulation_endtime__val=document.querySelector(".backtest_simulationdata_endtime__val");

let simulation_maxPrice__val_DOM=document.querySelector(".backtest_simulationdata_maxPrice__val");
let simulation_minPrice__val_DOM=document.querySelector(".backtest_simulationdata_minPrice__val");
let simulation_avgPrice__val_DOM=document.querySelector(".backtest_simulationdata_averagePrice__val");


/*  ___________[ CHART SETTING ] ___________ */
const backtest_chart_dom = document.getElementById('backtest_Chart').getContext('2d');

const backtestChart = new Chart(backtest_chart_dom, {
    type: 'line',

    data: {
        labels: backtest_chartInfo["timestamp"],

        datasets: [
            { // DATA1 : 선택된 코인의 현재가
            label: backtest_usersetting__market__val_DOM.innerText,
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

const training_chart_dom = document.getElementById('training_Chart').getContext('2d');

const trainingChart = new Chart(training_chart_dom, {
    type: 'line',

    data: {
        labels: training_chartInfo["timestamp"],

        datasets: [
            { // DATA1 : 선택된 코인의 현재가
            label: backtest_usersetting__market__val_DOM.innerText,
            data: training_chartInfo["trade_price"], // Y axis data1
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



/*  ___________[ Define Function ]___________*/
function simulate_backtest(){
  $.getJSON(
    // (1) Request URL
    get_backtestData_URL,
    // (2) Request Parameter
    {
      target_coin_id:get_targetID_from_CurURL(), // 현재 URL로부터 Target id 추출
      market:backtest_usersetting__market__val_DOM.innerText,
      data_unit:backtest_usersetting_unit__val_DOM.innerText,
      data_number:backtest_usersetting_datanumber__val_DOM.innerText,
      monitoring_time:backtest_usersetting_monitoringtime__val_DOM.innerText,
      training_end_time:training_endtime__val.innerText,
      simulation_end_time:simulation_endtime__val.innerText
    },
    // (3) Data Handling Function
    function(data){
      /* < BACKTEST CHART UPDATE > */
      // 1. Receive Data from python view function(backtest.get_backtestData()) responnd
      backtest_chartInfo["candletimeKST"]=data["backtest_data"]["candle_date_time_kst"];
      backtest_chartInfo["high_price"]=data["backtest_data"]["high_price"];
      backtest_chartInfo["low_price"]=data["backtest_data"]["low_price"];
      backtest_chartInfo["opening_price"]=data["backtest_data"]["opening_price"];
      backtest_chartInfo["timestamp"]=data["backtest_data"]["timestamp"];
      backtest_chartInfo["trade_price"]=data["backtest_data"]["trade_price"];

      // 2. Updaye Chart Data
      backtestChart["data"]["labels"]=backtest_chartInfo["candletimeKST"];

      // 1st data updayr => chart_index : 0
      backtestChart["data"]["datasets"][0]["data"]=backtest_chartInfo["trade_price"];

      // update chart UI
      backtestChart.update();

      // 3. Update Monitoring Data
      simulation_maxPrice__val_DOM.innerText=Math.max(...backtest_chartInfo["trade_price"]);
      simulation_minPrice__val_DOM.innerText=Math.min(...backtest_chartInfo["trade_price"]);
      simulation_avgPrice__val_DOM.innerText=get_AVG(backtest_chartInfo["trade_price"]);

      /* < TRAINING CHART UPDATE > */
      // 1. Receive Data from python view function(backtest.get_backtestData()) responnd
      training_chartInfo["candletimeKST"]=data["training_data"]["candle_date_time_kst"];
      training_chartInfo["high_price"]=data["training_data"]["high_price"];
      training_chartInfo["low_price"]=data["training_data"]["low_price"];
      training_chartInfo["opening_price"]=data["training_data"]["opening_price"];
      training_chartInfo["timestamp"]=data["training_data"]["timestamp"];
      training_chartInfo["trade_price"]=data["training_data"]["trade_price"];

      // 2. Updaye Chart Data
      trainingChart["data"]["labels"]=training_chartInfo["candletimeKST"];

      // 1st data updayr => chart_index : 0
      trainingChart["data"]["datasets"][0]["data"]=training_chartInfo["trade_price"];

      // update chart UI
      trainingChart.update();

      // 3. Update Monitoring Data
      training_maxPrice__val_DOM.innerText=Math.max(...training_chartInfo["trade_price"]);
      training_minPrice__val_DOM.innerText=Math.min(...training_chartInfo["trade_price"]);
      training_avgPrice__val_DOM.innerText=get_AVG(training_chartInfo["trade_price"]);
    }
  )

}



function calc_Simul_endTime(start_time, period_setting,endtime_DOM){ // start_time form : 2022-03-05 05:04:00
  let start_list=start_time.split(" ");

  let date_info=start_list[0].split("-");
  let time_info=start_list[1].split(":");

  // Create start_time_obj
  let start_time_obj={
    "start_year":date_info[0],
    "start_month":date_info[1],
    "start_day":date_info[2],
    "start_hour":time_info[0],
    "start_minute":time_info[1],
  }

  end_time_obj=calc_endtime(start_time_obj=start_time_obj, period_setting=period_setting);

  let endtime_year=adjust_digit(end_time_obj["end_year"]);
  let endtime_month=adjust_digit(end_time_obj["end_month"]);
  let endtime_day=adjust_digit(end_time_obj["end_day"]);

  let endtime_hour=adjust_digit(end_time_obj["end_hour"]);
  let endtime_minute=adjust_digit(end_time_obj["end_minute"]);


  end_time=endtime_year+"-"+endtime_month+"-"+endtime_day+" "+endtime_hour+":"+endtime_minute+":00";

  endtime_DOM.innerText= end_time;

}


function init_backRun(){
  // [1] Calc Data Number

  // (1-1) Calc User Setting Data Number
  let user_Setting_period=backtest_usersetting_period__val_DOM.innerText;
  let monitoring_time=backtest_usersetting_monitoringtime__val_DOM.innerText

  let simul_dataNum=calc_dataNumber(user_Setting_period, monitoring_time);

  backtest_usersetting_datanumber__val_DOM.innerText=simul_dataNum;

  // (1-2)
  let training_period= backtest_trainingdata_period__val.innerText;
  let training_dataUnit=backtest_trainingdata_dataUnit__val.innerText;
  console.log("calc_dataNumbe",training_period, training_dataUnit);
  let training_dataNum=calc_dataNumber(training_period, training_dataUnit);

  backtest_trainingdata_dataNumber_val.innerText=training_dataNum;


  // [2] Calc Training End time
  let training_start_time=training_starttime__val.innerText;
  let training_period_setting=backtest_usersetting_period__val_DOM.innerText;

  calc_Simul_endTime(start_time=training_start_time, period_setting= training_period_setting,endtime_DOM=training_endtime__val);


  // [3] Calc Simulation End time
  let simulation_start_time=simulation_starttime__val.innerText;
  let simulation_period_setting=backtest_usersetting_period__val_DOM.innerText;

  calc_Simul_endTime(start_time=simulation_start_time, period_setting=simulation_period_setting, endtime_DOM=simulation_endtime__val);
}


/* ___________[ Execute Simulation Function ]___________ */
init_backRun();
simulate_backtest();
