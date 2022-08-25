// ___________[ DOM Setting ]___________
// (1) user setting
let usersetting_period_val_DOM=document.querySelector(".usersetting_period_val");
let usersetting_monitoringtime_val_DOM=document.querySelector(".usersetting_monitoringtime_val");
let usersetting_dataNum_val_DOM=document.querySelector(".usersetting_dataNum_val");

// (2) Training Setting
let training_starttime_year_val_DOM=document.querySelector(".training_starttime_year_val");
let training_starttime_month_select_DOM=document.querySelector(".training_starttime_month_select");
let training_starttime_day_select_DOM=document.querySelector(".training_starttime_day_select");

let training_starttime_hour_select_DOM=document.querySelector(".training_starttime_hour_select");
let training_starttime_minute_select_DOM=document.querySelector(".training_starttime_minute_select");


let training_endtime_year_val_DOM=document.querySelector(".training_endtime_year_val");
let training_endtime_month_val_DOM=document.querySelector(".training_endtime_month_val");
let training_endtime_day_val_DOM=document.querySelector(".training_endtime_day_val");

let training_endtime_hour_val_DOM=document.querySelector(".training_endtime_hour_val");
let training_endtime_minute_val_DOM=document.querySelector(".training_endtime_minute_val");


let training_period_select_DOM=document.querySelector(".training_period_select");
let training_dataunit_select_DOM=document.querySelector(".training_dataunit_select");

let training_datanumber_val_DOM=document.querySelector(".training_datanumber_val");


// (3) Backtesting Setting
let backtest_starttime_year_val_DOM=document.querySelector(".backtest_starttime_year_val");
let backtest_starttime_month_select_DOM=document.querySelector(".backtest_starttime_month_select");
let backtest_starttime_day_select_DOM=document.querySelector(".backtest_starttime_day_select");

let backtest_starttime_hour_select_DOM=document.querySelector(".backtest_starttime_hour_select");
let backtest_starttime_minute_select_DOM=document.querySelector(".backtest_starttime_minute_select");

// (5) Backtesting End Time Setting
let backtest_endtime_year_val_DOM=document.querySelector(".backtest_endtime_year_val");
let backtest_endtime_month_val_DOM=document.querySelector(".backtest_endtime_month_val");
let backtest_endtime_day_val_DOM=document.querySelector(".backtest_endtime_day_val");

let backtest_endtime_hour_val_DOM=document.querySelector(".backtest_endtime_hour_val");
let backtest_endtime_minute_val_DOM=document.querySelector(".backtest_endtime_minute_val");


// ___________[ Global Variable Setting ]___________
let back_starttime_input={ // for .addEventListener("change", select_changeEvent);
  "input_month":0,
  "input_day":0,
  "input_hour":0,
  "input_minute":0
};

let train_starttime_input={ // for .addEventListener("change", select_changeEvent);
  "input_month":0,
  "input_day":0,
  "input_hour":0,
  "input_minute":0
};

let train_period="";
let train_dataunit="";

// ___________[ Definition Function]___________
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


function init(){
  // (1) Display Year
  let today=new Date();
  backtest_starttime_year_val_DOM.innerText=today.getFullYear();
  training_starttime_year_val_DOM.innerText=today.getFullYear();

  // (2-1) Create Select Month Ootions : Training, Backtest
  for(let month=1;month<=today.getMonth()+1;month++){
    // <Create Training Month Selector>
    let month_tr_option=document.createElement("option");

    month_tr_option.value=`trainstart_month_${month}`;
    month_tr_option.innerText=month;

    training_starttime_month_select_DOM.append(month_tr_option);

    // <Create Backtest Month Selector>
    let month_bt_option=document.createElement("option");

    month_bt_option.value=`backstart_month_${month}`;
    month_bt_option.innerText=month;

    backtest_starttime_month_select_DOM.append(month_bt_option);
  }

  // (2-2) Create Select Day Ootions : Training, Backtest
  for(let day=1; day<=31; day++){
    // <Create Training Month Selector>
    let day_tr_option=document.createElement("option");

    day_tr_option.value=`trainstart_day_${day}`;
    day_tr_option.innerText=day;

    training_starttime_day_select_DOM.append(day_tr_option);


    // <Create Backtest Month Selector>
    let day_bt_option=document.createElement("option");

    day_bt_option.value=`backstart_day_${day}`;
    day_bt_option.innerText=day;

    backtest_starttime_day_select_DOM.append(day_bt_option);
  }

  // (2-3) Create Select Hour Ootions : Training, Backtest
  for(let hour=0; hour<=23; hour++){
    // <Create Training Month Selector>
    let hour_tr_option=document.createElement("option");

    hour_tr_option.value=`trainstart_hour_${hour}`;
    hour_tr_option.innerText=hour;

    training_starttime_hour_select_DOM.append(hour_tr_option);

    // <Create Backtest Month Selector>
    let hour_bt_option=document.createElement("option");

    hour_bt_option.value=`backstart_hour_${hour}`;
    hour_bt_option.innerText=hour;

    backtest_starttime_hour_select_DOM.append(hour_bt_option);

  }

  // (2-4) Create Select Minute Ootions : Training, Backtest
  for(let minute=0; minute<=59; minute++){
    // <Create Training Month Selector>
    let minute_tr_option=document.createElement("option");

    minute_tr_option.value=`trainstart_minute_${minute}`;
    minute_tr_option.innerText=minute;

    training_starttime_minute_select_DOM.append(minute_tr_option);

    // <Create Backtest Month Selector>
    let minute_bt_option=document.createElement("option");

    minute_bt_option.value=`backstart_minute_${minute}`;
    minute_bt_option.innerText=minute;

    backtest_starttime_minute_select_DOM.append(minute_bt_option);
  }


  // (3) Calculate Backtesting Data Number
  usersetting_dataNum_val_DOM.innerText=calc_dataNumber(trading_period=usersetting_period_val_DOM.innerText,
                                                        monitoring_time=usersetting_monitoringtime_val_DOM.innerText);



}


// ___________[ Event Setting ]___________

function select_changeEvent(event){

  /*  <Backtesting Event >  */
  if(event.target.name.indexOf("backtest")!==-1){
    let time_type=event.target.name.split("_")[2];
    let regex=/[^0-9]/g;


    if (event.target.value!==`backstart_${time_type}_None`){ // 유효한 선택인지 확인
      back_starttime_input[`input_${time_type}`]=parseInt(event.target.value.replace(regex,""));
    }else if(event.target.value==`backstart_${time_type}_None`){
      back_starttime_input[`input_${time_type}`]=0;
    }


    if (back_starttime_input["input_month"]>0 && back_starttime_input["input_day"]>0 && back_starttime_input["input_hour"]>0 && back_starttime_input["input_minute"]>0){
      if (check_starttime_dateinput(back_starttime_input["input_month"], back_starttime_input["input_day"])==true){

        let period_setting=usersetting_period_val_DOM.innerText;

        let back_start_time_obj={
              "start_minute":back_starttime_input["input_minute"],
              "start_hour":back_starttime_input["input_hour"],
              "start_day":back_starttime_input["input_day"],
              "start_month":back_starttime_input["input_month"],
              "start_year":new Date().getFullYear() // 올해년도 구하기
            }


        let end_time_obj=calc_endtime(start_time_obj=back_start_time_obj, period_setting=period_setting);

        backtest_endtime_year_val_DOM.innerText=end_time_obj["end_year"];
        backtest_endtime_month_val_DOM.innerText=end_time_obj["end_month"];
        backtest_endtime_day_val_DOM.innerText= end_time_obj["end_day"];
        backtest_endtime_hour_val_DOM.innerText= end_time_obj["end_hour"];
        backtest_endtime_minute_val_DOM.innerText=end_time_obj["end_minute"];
      }
    }

  }


  /*  <Training Event >  */
  if(event.target.name.indexOf("training")!==-1){
    let time_type=event.target.name.split("_")[2];
    let regex=/[^0-9]/g;


    if (event.target.value!==`training_${time_type}_None`){ // 유효한 선택인지 확인
      train_starttime_input[`input_${time_type}`]=parseInt(event.target.value.replace(regex,""));
    }else if(event.target.value==`training_${time_type}_None`){
      train_starttime_input[`input_${time_type}`]=0;
    }


    if (train_starttime_input["input_month"]>0 && train_starttime_input["input_day"]>0 && train_starttime_input["input_hour"]>0 && train_starttime_input["input_minute"]>0){
      if (check_starttime_dateinput(train_starttime_input["input_month"], train_starttime_input["input_day"])==true){

        let period_setting=usersetting_period_val_DOM.innerText;

        let train_start_time_obj={
              "start_minute":train_starttime_input["input_minute"],
              "start_hour":train_starttime_input["input_hour"],
              "start_day":train_starttime_input["input_day"],
              "start_month":train_starttime_input["input_month"],
              "start_year":new Date().getFullYear() // 올해년도 구하기
            }


        let end_time_obj=calc_endtime(start_time_obj=train_start_time_obj, period_setting=period_setting);

        training_endtime_year_val_DOM.innerText=end_time_obj["end_year"];
        training_endtime_month_val_DOM.innerText=end_time_obj["end_month"];
        training_endtime_day_val_DOM.innerText= end_time_obj["end_day"];
        training_endtime_hour_val_DOM.innerText= end_time_obj["end_hour"];
        training_endtime_minute_val_DOM.innerText=end_time_obj["end_minute"];
      }
    }

  }

}

// Add Event to DOM
training_starttime_month_select_DOM.addEventListener("change", select_changeEvent);
training_starttime_day_select_DOM.addEventListener("change", select_changeEvent);
training_starttime_hour_select_DOM.addEventListener("change", select_changeEvent);
training_starttime_minute_select_DOM.addEventListener("change", select_changeEvent);

backtest_starttime_month_select_DOM.addEventListener("change", select_changeEvent);
backtest_starttime_day_select_DOM.addEventListener("change", select_changeEvent);
backtest_starttime_minute_select_DOM.addEventListener("change", select_changeEvent);
backtest_starttime_hour_select_DOM.addEventListener("change", select_changeEvent);



function calc_training_dataNum(){
  if(event.target.name.indexOf("period")!==-1){
    if(event.target.value==="Required"){
      train_period="";
    }else{
      train_period=training_period_select_DOM.value;
    }

  }else if(event.target.name.indexOf("dataunit")!==-1){
    if(event.target.value==="Required"){
      train_dataunit="";
    }else{
      train_dataunit=training_dataunit_select_DOM.value;
    }
  }
  console.log("sexS");
  // (3) Calculate Training Data Number
  if(train_dataunit!=="" && train_period!==""){
       // (3) Calculate Training Data Number
       if (check_timeSize(train_period, train_dataunit)==true){
         training_datanumber_val_DOM.innerText=calc_dataNumber(trading_period=training_period_select_DOM.value,
                                                               monitoring_time=training_dataunit_select_DOM.value);
       }else{
         alert("유효하지 않은 시간설정입니다!");
       }

  }


}

training_period_select_DOM.addEventListener("change", calc_training_dataNum);
training_dataunit_select_DOM.addEventListener("change", calc_training_dataNum);

// ___________[ Function Execution ]___________
init();
