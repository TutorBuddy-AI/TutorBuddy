function showPassword() {
  var pass_field = document.getElementById("password");
  if (pass_field.type === "password") {
    pass_field.type = "text";
  } else {
    pass_field.type = "password";
  }
}
