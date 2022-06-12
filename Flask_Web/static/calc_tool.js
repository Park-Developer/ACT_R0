function get_AVG(array){ // 평균 계산 함수
  let result = array.reduce(
    function add(sum, currValue) {
      return sum + currValue;
    },
    0);

  result=result/(array.length);
  return result.toFixed(3); // 소수점 자릿수 지정
}
