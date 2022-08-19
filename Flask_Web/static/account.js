let trading_account_table_DOM=document.querySelector(".PERFORMANCE_trading_table");
const setting_coin_number = trading_account_table_DOM.rows.length;


function init(){
  /*  [Remain Time 계산 (Unit : Min) ]  */

  for(coin_idx=1; coin_idx<=setting_coin_number;coin_idx++)
  {
    console.log("idccc",coin_idx)

    let coin_endtime=document.querySelector(`.personal_TT__trading_end_${coin_idx}`);
    let coin_remaintime=document.querySelector(`.personal_TT__trading_remain_${coin_idx}`);

    let end_time=new Date(coin_endtime.innerText);

    let today = new Date();
    let difference=(end_time.getTime()-today.getTime())/(1000*60);

    coin_remaintime.innerText=difference.toFixed(1)+" Min";
  }

}



init();
