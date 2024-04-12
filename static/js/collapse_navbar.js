function collapse_navbar() {
  let side_bar = document.getElementById("side-bar");
  let toggle = document.getElementById("logo-name__button");
  let wrapper = document.getElementById("page-wrapper");
  side_bar.classList.toggle('collapse');
  toggle.classList.toggle('rotate-icon');
  wrapper.classList.toggle('extended');
}