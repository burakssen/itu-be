function create_stars(temp){
   var index = Number(String(temp).replace("stars-",""));

   var stars = document.querySelector("#stars-"+index);

   
    

   for(var i = 0; i < index + 1; i++){
    var span = document.createElement("SPAN");
    var div = document.createElement("DIV");
 
    span.appendChild(div);
    span.classList.add("fas");
    span.classList.add("fa-star");
    stars.append(span);
   }

   for(var i = 0; i < 4 - index; i++){
    
    var span = document.createElement("SPAN");
    var div = document.createElement("DIV");
 
    span.appendChild(div);
    span.classList.add("far");
    span.classList.add("fa-star");
    stars.append(span);
    stars.append(span);
   }
}