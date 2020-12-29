function previewFile() {
  var preview = document.querySelector("#video-image-placeholder");
  var file    = document.querySelector("#video-thumbnail").files[0];
  var reader  = new FileReader();
 
  reader.onloadend = function () {
    preview.src = reader.result;
  }
 
  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "https://via.placeholder.com/1024x720.png";
  }
} 
  
function previewFileName() {
  var preview = document.querySelector(".file-name");
  var file    = document.querySelector("#video").files[0];
  var reader  = new FileReader();

  reader.onloadend = function () {
    preview.innerHTML = file.name;
  }
 
  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
  }
   
  console.log(file);
}
    
