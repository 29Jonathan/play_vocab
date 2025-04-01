document.addEventListener("DOMContentLoaded", function () {
    const highlightedWord = document.getElementById("highlighted-word");
    if (highlightedWord) {
      highlightedWord.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });

function checkAnswer() {
    const userInput = document.getElementById('userInput').value.trim();
    const correctAnswer = "{{ selected_word }}";
    const alertBox = document.getElementById('alertBox');
    const nextRoundButton = document.getElementById('nextRoundButton');

    if (userInput === correctAnswer) {
        alertBox.classList.remove('alert-danger');
        alertBox.classList.add('alert-success');
        alertBox.innerText = "Correct! You guessed the word.";
        nextRoundButton.style.display = "block"; // Show the Next Round button
    } else {
        alertBox.classList.remove('alert-success');
        alertBox.classList.add('alert-danger');
        alertBox.innerText = `Incorrect! The correct word was: ${correctAnswer}`;
        nextRoundButton.style.display = "block"; // Show the Next Round button
    }
}

function nextRound() {
    location.reload(); // Reload the page to start the next round
}