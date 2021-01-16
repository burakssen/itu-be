function setStars(number_of_stars,class_code){
   var star = document.querySelector(".star_id"+String(class_code));

   for(var i = 0; i < Math.round(number_of_stars); i++ ){
      var span = document.createElement("SPAN");
      var div = document.createElement("DIV");

      span.appendChild(div);
      span.classList.add("fas");
      span.classList.add("fa-star");
      star.append(span);
      star.append(span);
   }

   for(var i = 0; i < 5 - Math.round(number_of_stars); i++ ){
      var span = document.createElement("SPAN");
      var div = document.createElement("DIV");
      span.appendChild(div);
      span.classList.add("far");
      span.classList.add("fa-star");
      star.append(span);
      star.append(span);
   }
}