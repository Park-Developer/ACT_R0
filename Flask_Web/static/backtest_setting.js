// ___________[ DOM Setting ]___________
// (1) start time setting
let backtest_starttime_year_val_DOM=document.querySelector(".backtest_starttime_year_val");
let backtest_starttime_month_select_DOM=document.querySelector(".backtest_starttime_month_select");
let backtest_starttime_day_select_DOM=document.querySelector(".backtest_starttime_day_select");

let backtest_starttime_hour_select_DOM=document.querySelector(".backtest_starttime_hour_select");
let backtest_starttime_minute_select_DOM=document.querySelector(".backtest_starttime_minute_select");


// (2) end time setting
let backtest_endtime_year_val_DOM=document.querySelector(".backtest_endtime_year_val");
let backtest_endtime_month_val_DOM=document.querySelector(".backtest_endtime_month_val");
let backtest_endtime_day_val_DOM=document.querySelector(".backtest_endtime_day_val");

let backtest_endtime_hour_val_DOM=document.querySelector(".backtest_endtime_hour_val");
let backtest_endtime_minute_val_DOM=document.querySelector(".backtest_endtime_minute_val");

// (3) user setting
let backtesting_period_val_DOM=document.querySelector(".backtesting_period_val");
let backtesting_monitoringtime_val_DOM=document.querySelector(".backtesting_monitoringtime_val");
let backtesting_dataNum_val_DOM=document.querySelector(".backtesting_dataNum_val");



// ___________[ Global Variable Setting ]___________
let start_time_input={
  "input_month":0,
  "input_day":0,
  "input_hour":0,
  "input_minute":0
}


// ___________[ Definition Function]___________
function get_monthDate(month){
  let date = new Date();
  let this_year=date.getFullYear(); // 올해년도 구하기

  let month_date=new Date(this_year,month,0).getDate();   // 해당월의 일수 구하기

  return month_date;
}


function check_starttime_dateinput(input_month, input_day){
  // (1) select 입력여부 확인
  if (input_month==0 || input_day==0){
    return false;
  }

  // (2) 유효한 날짜인지 확인
  let month_date= get_monthDate(input_month);

  if (input_day<=month_date){
    return true;
  }else{
    return false;
  }
}


function set_endtime(){
  let regex=/[^0-9]/g;
  let date = new Date();

  let start_minute=parseInt(backtest_starttime_minute_select_DOM.value.replace(regex,""));
  let start_hour=parseInt(backtest_starttime_hour_select_DOM.value.replace(regex,""));
  let start_day= parseInt(backtest_starttime_day_select_DOM.value.replace(regex,""));
  let start_month=parseInt(backtest_starttime_month_select_DOM.value.replace(regex,""));
  let start_year=date.getFullYear()

  let end_minute=start_minute;
  let end_hour=0;
  let end_day=0;
  let end_month=0;
  let end_year=start_year;

  let period_setting=backtesting_period_val_DOM.innerText;

  if (period_setting.indexOf("Hour")!==-1 || period_setting.indexOf("hour")!==-1){ // Period Unit : Hour
      let period_hour_val=parseInt(period_setting.replace(regex,""));

      end_hour=start_hour+period_hour_val;
      end_day=start_day;
      end_month=start_month;

  }else if(period_setting.indexOf("Day")!==-1 || period_setting.indexOf("day")!==-1){
      let period_day_val=parseInt(period_setting.replace(regex,""));

      end_hour=start_hour;
      end_day=start_day+period_day_val;
      end_month=start_month;
  }else if(period_setting.indexOf("Week")!==-1 || period_setting.indexOf("week")!==-1){
      let period_day_val=parseInt(period_setting.replace(regex,""))*7; // X 7 해주기

      end_hour=start_hour;
      end_day=start_day+period_day_val;
      end_month=start_month;
  }


  // 시간 계산
  if(end_hour>=24){
    end_day=end_day+1;
    end_hour=end_hour-24;
  }

  if(end_day>get_monthDate(end_month)){
    end_day=end_day-get_monthDate(end_month);
    end_month=end_month+1;
  }

  if(end_month>12){
    end_month=1;
    end_month=start_month+1;
  }

  // HTML Write
  backtest_endtime_year_val_DOM.innerText=end_year;
  backtest_endtime_month_val_DOM.innerText=end_month;
  backtest_endtime_day_val_DOM.innerText= end_day;
  backtest_endtime_hour_val_DOM.innerText= end_hour;
  backtest_endtime_minute_val_DOM.innerText=end_minute
}

function calc_dataNumber(trading_period, monitoring_time){
  // (1) Get Trading Period (Unit : Minute)
  let regex=/[^0-9]/g;

  if (trading_period.indexOf("Minute")!== -1){ // Training Data Unit : Minute
      period_time_Minute=parseInt(trading_period.replace(regex,""));

  }else if(trading_period.indexOf("Hour")!== -1){  // Training Data Unit : Hour
      period_time_Minute=parseInt(trading_period.replace(regex,""))*60;

  }else if(trading_period.indexOf("Day")!== -1){  // Training Data Unit : Day
      period_time_Minute=parseInt(trading_period.replace(regex,""))*60*24;

  }else if(trading_period.indexOf("Week")!== -1){  // Training Data Unit : Week
      period_time_Minute=parseInt(trading_period.replace(regex,""))*60*24*7;

  }else if(trading_period.indexOf("Month")!== -1){  // Training Data Unit : Month
      period_time_Minute=parseInt(trading_period.replace(regex,""))*60*24*30;;

  }

  // (2) Get Monotiroing Time (Unit : Minute)
  monitoring_time_Minute=parseInt(monitoring_time);


  // return
  return (period_time_Minute*monitoring_time_Minute);
}


function init(){
  // (1) Display Year
  let today=new Date();
  backtest_starttime_year_val_DOM.innerText=today.getFullYear();

  // (2-1) Create Select Month Ootions
  for(let month=1;month<=today.getMonth()+1;month++){
    let month_option=document.createElement("option");

    month_option.value=`backstart_month_${month}`;
    month_option.innerText=month;

    backtest_starttime_month_select_DOM.append(month_option);

  }

  // (2-2) Create Select Hour Ootions
  for(let hour=0; hour<=23; hour++){
    let hour_option=document.createElement("option");

    hour_option.value=`backstart_hour_${hour}`;
    hour_option.innerText=hour;

    backtest_starttime_hour_select_DOM.append(hour_option);

  }

  // (2-3) Create Select Minute Ootions
  for(let minute=0; minute<=59; minute++){
    let minute_option=document.createElement("option");

    minute_option.value=`backstart_minute_${minute}`;
    minute_option.innerText=minute;

    backtest_starttime_minute_select_DOM.append(minute_option);

  }

  // (3) Calculate Backtesting Data Number
  backtesting_dataNum_val_DOM.innerText=calc_dataNumber(trading_period=backtesting_period_val_DOM.innerText,
                                                        monitoring_time=backtesting_monitoringtime_val_DOM.innerText);

}


// ___________[ Event Setting ]___________

function select_changeEvent(event){
  let time_type=event.target.name.split("_")[2];
  let regex=/[^0-9]/g;


  if (event.target.value!==`backstart_${time_type}_None`){ // 유효한 선택인지 확인
    start_time_input[`input_${time_type}`]=parseInt(event.target.value.replace(regex,""));
  }else if(event.target.value==`backstart_${time_type}_None`){
    start_time_input[`input_${time_type}`]=0;
  }


  if (start_time_input["input_month"]>0 && start_time_input["input_day"]>0 && start_time_input["input_hour"]>0 && start_time_input["input_minute"]>0){
    if (check_starttime_dateinput(start_time_input["input_month"], start_time_input["input_day"])==true){
      console.log("set_endtime();");
      set_endtime();
    }
  }

}

backtest_starttime_month_select_DOM.addEventListener("change", select_changeEvent);
backtest_starttime_day_select_DOM.addEventListener("change", select_changeEvent);
backtest_starttime_hour_select_DOM.addEventListener("change", select_changeEvent);
backtest_starttime_minute_select_DOM.addEventListener("change", select_changeEvent);


// ___________[ Function Execution ]___________
init();
