let slideIndex = 1; // 初始化为1
let slideInterval;

function plusSlides(n) {
  showSlides(slideIndex + n);
}

function currentSlide(n) {
  showSlides(n);
}

function showSlides(n) {
  const slides = document.getElementsByClassName("mySlides");
  const dots = document.getElementsByClassName("dot");

  if (n > slides.length) {
    slideIndex = 1;
  } else if (n < 1) {
    slideIndex = slides.length;
  }

  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    dots[i].classList.remove("active");
  }

  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].classList.add("active");
}

function startAutoSlide() {
  slideInterval = setInterval(() => plusSlides(1), 5000);
}

function pauseAutoSlide() {
  clearInterval(slideInterval);
}

const slides = document.getElementsByClassName("mySlides");

for (let i = 0; i < slides.length; i++) {
  slides[i].addEventListener("mouseenter", pauseAutoSlide);
  slides[i].addEventListener("mouseleave", startAutoSlide);
}

window.onload = function () {
  startAutoSlide();
}
// 关闭模态框
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}