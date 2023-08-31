
    const inputs = document.querySelectorAll('.custom_input, .form-check-input');

    inputs.forEach(input => {
      input.addEventListener('click', function handleClick(event) {
        input.classList.remove("error");
        $(input).closest(".form-floating").find(".formlab").removeClass("error")
        $(input).closest(".forms-inputs").find(".error-span").removeClass("error")
          $(input).closest(".form-check-label").find("span").removeClass("error")
      });
    });
