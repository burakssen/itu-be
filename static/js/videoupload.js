function previewFile(src,dst) {
  var preview = document.querySelector("#video-image-placeholder");
  var file    = document.querySelector("#video-thumbnail").files[0];
  var reader  = new FileReader();
 
  reader.onloadend = function () {
    preview.src = reader.result;
  }
 
  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
  } 
}