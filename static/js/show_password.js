function showPassword(inputId) {
  var pass_field = document.getElementById(inputId);
  if (pass_field.type === "password") {
    pass_field.type = "text";
  } else {
    pass_field.type = "password";
  }
}
