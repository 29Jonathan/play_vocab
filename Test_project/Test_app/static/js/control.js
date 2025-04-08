document.addEventListener("DOMContentLoaded", function () {
    const highlightedWord = document.getElementById("highlighted-word");
    if (highlightedWord) {
      highlightedWord.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });

  function menubar() {
    var hihu = document.querySelector('.menu-data');
    var element = document.getElementById('Menu-bar');

    if (hihu) {
        hihu.classList.remove('animate__fadeOut');
        element.style.display = 'none';
        hihu.style.zIndex = '1';
        hihu.classList.add('animate__fadeIn');
    }
}

function closebar() {
    var hihu = document.querySelector('.menu-data');
    var element = document.getElementById('Menu-bar');
    if (hihu) {
        hihu.classList.remove('animate__fadeIn');
        hihu.style.zIndex = '-20';
        element.style.display = 'block';
        hihu.classList.add('animate__fadeOut');
    }
}
