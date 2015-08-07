function isThisWorking(data) {
  if (data == "correct") {
   console.log("hooray");
  } else {
   console.log("booooo");
  }
}

function check_answer_clicked(e) {
  e.preventDefault();
  console.log("hey");
  $.post("/science", {"answerofuser": $("#userans").val(), "question_id": $("#question_id").text() , }, function (data){
    console.log("I am in my function");
    alert(data);
  });
}

console.log("ahahaha")

$(document).ready(function(){
  console.log("bbbbjsjsjsjjbbbbb");
  $('#check_answer').click(check_answer_clicked);
});
