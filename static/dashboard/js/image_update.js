document.addEventListener('DOMContentLoaded', function() {
  // Handle avatar upload
  document.getElementById('id_avatar').addEventListener('change', function() {
      var file = this.files[0];
      if (file) {
          var reader = new FileReader();
          reader.onload = function(e) {
              var image = document.querySelector('.circular-avatar');
              image.src = e.target.result;
          };
          reader.readAsDataURL(file);
      }
  });
});