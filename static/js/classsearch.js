<<<<<<< HEAD
function create_stars(temp){
   
=======
function create_stars(temp){
   var index = Number(String(temp).replace("stars-",""));

   var stars = document.querySelector("#stars-"+index);


   for(var i = 0; i < 5 - index; i++){
    
      var span = document.createElement("SPAN");
      var div = document.createElement("DIV");
   
      span.appendChild(div);
      span.classList.add("fas");
      span.classList.add("fa-star");
      stars.append(span);
      stars.append(span);
   }

   for(var i = 0; i < index; i++){
      var span = document.createElement("SPAN");
      var div = document.createElement("DIV");
   
      span.appendChild(div);
      span.classList.add("far");
      span.classList.add("fa-star");
      stars.append(span);
   }

   

   

   
>>>>>>> caff39109f269eb0aef996fa34fc65fd8c5b9c9b
}