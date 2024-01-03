

    inputs = document.querySelectorAll('.custom_input, .form-check-input');

    inputs.forEach(input => {
      input.addEventListener('click', function handleClick(event) {
        input.classList.remove("error");
        $(input).closest(".form-floating").find(".formlab").removeClass("error")
        $(input).closest(".forms-inputs").find(".error-span").removeClass("error")
          $(input).closest(".forms-inputs").find(".error-span").html("")
          $(input).closest(".form-check-label").find("span").removeClass("error")
      });
    });


    function onSubmit(token) {
         document.getElementById("auth-form").submit();
       }