const fileInput = document.getElementById("id_avatar");
    fileInput.addEventListener("change", function() {
      
      const uploadedImage = document.getElementById("uploaded-image");
      uploadedImage.src = URL.createObjectURL(this.files[0]);
      uploadedImage.style.display = "block";
    });

