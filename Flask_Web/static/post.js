window.addEventListener('DOMContentLoaded', function()
{
  let post_find__input_DOM=document.querySelector(".post_find__input");
  let post_find__button=document.querySelector(".post_find__button");

  post_find__button.addEventListener("click", find_post);
  
  function find_post(){
  console.log("find btn click!")
  }

});
