function get_monthDate(month){
  let date = new Date();
  let this_year=date.getFullYear(); // 올해년도 구하기

  let month_date=new Date(this_year,month,0).getDate();   // 해당월의 일수 구하기

  return month_date;
}


function calc_endtime(start_time_obj, period_setting){
  let regex=/[^0-9]/g;

  // start time set
  let start_minute=parseInt(start_time_obj["start_minute"]);
  let start_hour=parseInt(start_time_obj["start_hour"]);
  let start_day= parseInt(start_time_obj["start_day"]);
  let start_month=parseInt(start_time_obj["start_month"]);
  let start_year=parseInt(start_time_obj["start_year"]);

  // end time set
  let end_minute=0;
  let end_hour=0;
  let end_day=0;
  let end_month=0;
  let end_year=start_year;

  // period time에 따라서 end time 계산
  if (period_setting.indexOf("Minute")!==-1 || period_setting.indexOf("minute")!==-1){ // => Period Unit : Minute
      let period_minute_val=parseInt(period_setting.replace(regex,""));

      end_minute=start_minute+period_minute_val;
      end_hour=start_hour
      end_day=start_day;
      end_month=start_month;

  }else if (period_setting.indexOf("Hour")!==-1 || period_setting.indexOf("hour")!==-1){ // => Period Unit : Hour
      let period_hour_val=parseInt(period_setting.replace(regex,""));

      end_minute=start_minute;
      end_hour=start_hour+period_hour_val;
      end_day=start_day;
      end_month=start_month;

  }else if(period_setting.indexOf("Day")!==-1 || period_setting.indexOf("day")!==-1){ // => Period Unit : Day
      let period_day_val=parseInt(period_setting.replace(regex,""));

      end_minute=start_minute;
      end_hour=start_hour;
      end_day=start_day+period_day_val;
      end_month=start_month;
  }else if(period_setting.indexOf("Week")!==-1 || period_setting.indexOf("week")!==-1){ // => Period Unit : Week
      let period_day_val=parseInt(period_setting.replace(regex,""))*7; // X 7 해주기

      end_minute=start_minute;
      end_hour=start_hour;
      end_day=start_day+period_day_val;
      end_month=start_month;
  }

  // 유효시간 계산
  if(end_minute>=60){
    end_hour=end_hour+1;
    end_minute=end_minute-60;
  }

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

  // Return
  end_time_obj={
    "end_minute":end_minute,
    "end_hour":end_hour,
    "end_day":end_day,
    "end_month":end_month,
    "end_year":end_year
  }

  return end_time_obj;
}

function convert_minute_Number(time){ // form : ~ Minute, ~ Hour, ~ Day, ~ Week, ~ Month
  let regex=/[^0-9]/g;

  if (time.indexOf("Minute")!== -1){ // Training Data Unit : Minute
      minute_unit=parseInt(time.replace(regex,""));

  }else if(time.indexOf("Hour")!== -1){  // Training Data Unit : Hour
      minute_unit=parseInt(time.replace(regex,""))*60;

  }else if(time.indexOf("Day")!== -1){  // Training Data Unit : Day
    minute_unit=parseInt(time.replace(regex,""))*60*24;

  }else if(time.indexOf("Week")!== -1){  // Training Data Unit : Week
      minute_unit=parseInt(time.replace(regex,""))*60*24*7;

  }else if(time.indexOf("Month")!== -1){  // Training Data Unit : Month
      minute_unit=parseInt(time.replace(regex,""))*60*24*30;;
  }

  return minute_unit;
}

function convert_period_To_minute(time){ // form : ~ Minute, ~ Hour, ~ Day, ~ Week, ~ Month
  let regex=/[^0-9]/g;
  let minute_unit=0;
  
  if (time.indexOf("Minute")!== -1){ // Training Data Unit : Minute
      minute_unit=parseInt(time.replace(regex,""));

  }else if(time.indexOf("Hour")!== -1){  // Training Data Unit : Hour
      minute_unit=parseInt(time.replace(regex,""))*60;

  }else if(time.indexOf("Day")!== -1){  // Training Data Unit : Day
    minute_unit=parseInt(time.replace(regex,""))*60*24;

  }else if(time.indexOf("Week")!== -1){  // Training Data Unit : Week
      minute_unit=parseInt(time.replace(regex,""))*60*24*7;

  }else if(time.indexOf("Month")!== -1){  // Training Data Unit : Month
      minute_unit=parseInt(time.replace(regex,""))*60*24*30;;
  }

  return minute_unit;
}

function convert_dataUnit_To_minute(time){ // form : ~ Minute, ~ Hour, ~ Day, ~ Week, ~ Month
  let regex=/[^0-9]/g;
  let minute_unit=0;

  if (time.indexOf("Minute")!== -1){ // Training Data Unit : Minute
      minute_unit=1

  }else if(time.indexOf("Hour")!== -1){  // Training Data Unit : Hour
      minute_unit=60

  }else if(time.indexOf("Day")!== -1){  // Training Data Unit : Day
    minute_unit=60*24;

  }else if(time.indexOf("Week")!== -1){  // Training Data Unit : Week
      minute_unit=60*24*7;

  }else if(time.indexOf("Month")!== -1){  // Training Data Unit : Month
      minute_unit=60*24*30;
  }

  return minute_unit;
}

function calc_dataNumber(period, monitoring_time){
  // 분단위로 데이터 개수 계산
  console.log("period, monitoring_time");
  // (1) Get Trading Period (Unit : Minute)
  let period_time_Minute=0;

  if(isNaN(period)==false){ // 숫자형 문자열인 경우
    period_time_Minute=parseInt(period);
  }
  else{  // 숫자형 문자열이 아닌 경우
    period_time_Minute=convert_period_To_minute(period);
  }


  let monitoring_time_Minute=0;
  // (2) Get Monotiroing Time (Unit : Minute)
  if(isNaN(monitoring_time)==false){ // 숫자형 문자열인 경우
    monitoring_time_Minute=parseInt(monitoring_time);
  }
  else{  // 숫자형 문자열이 아닌 경우
    monitoring_time_Minute=convert_dataUnit_To_minute(monitoring_time);
  }

  console.log("period_time_Minute",period_time_Minute);
  console.log("  monitoring_time_Minute",  monitoring_time_Minute);

  return (period_time_Minute/monitoring_time_Minute);
}

function check_timeSize(period_time, data_unit){
  // define func
  function get_timeSize(time){
    if (time.indexOf("Minute")!== -1){ //  Minute Time Size : 1
      return 1;
    }else if(time.indexOf("Hour")!== -1){  // Hour Time Size : 2
      return 2;
    }else if(time.indexOf("Day")!== -1){  // Day Time Size : 3
      return 3;
    }else if(time.indexOf("Week")!== -1){  // Week Time Size : 4
      return 4;
    }else if(time.indexOf("Month")!== -1){  // Month Time Size : 5
      return 5;
    }
  }

  period_size=get_timeSize(period_time);
  unit_size=get_timeSize(data_unit);

  if (period_size>=unit_size){
    return true;
  }else {
    return false;
  }

}

function adjust_digit(time_info){

  if(typeof time_info !=="string"){
    time_info=time_info.toString();
  }

  if(typeof time_info ==="string"){
    if(time_info.length<2){
        time_info="0"+time_info;
      }
  }

  return time_info;
}
