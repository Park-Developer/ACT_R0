// 배열에 대해서 평균값 반환
function get_AVG(array){ // 평균 계산 함수
  let result = array.reduce(
    function add(sum, currValue) {
      return sum + currValue;
    },
    0);

  result=result/(array.length);
  return result.toFixed(1); // 소수점 자릿수 지정
}


// 현제 URL에서 target coin 번호 반환
function get_targetID_from_CurURL(){
  let url_split=document.location.href.split("/");
  //(6) ['http:', '', '127.0.0.1:5000', 'backtest', 'target_1', 'run']

  for(let idx=0; idx<url_split.length; idx++){

    if (url_split[idx].indexOf("Target_")!==-1 || url_split[idx].indexOf("target_")!==-1){
      let regex=/[^0-9]/g;
      target_data=url_split[idx].replace(regex, "");

      if (isNaN(target_data)==false){ // 추출한 문자열이 숫자인지 확인
        let target_num=parseInt(target_data);

        if (target_num>=1 && target_num<=4){ // 1 ~ 4인지 확인
          return target_num;
        }
      }
    }
  } //for loop


  return -1;
}
