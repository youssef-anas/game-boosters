// ----------------------------- Arena 2x2 Boost ---------------------------------
var currentArena2x2 = document.getElementById('currentArena2x2');
var currentArena2x2Value = document.getElementById('currentArena2x2Value');
var desiredArena2x2 = document.getElementById('desiredArena2x2');
var desiredArena2x2Value = document.getElementById('desiredArena2x2Value');

// Initail Values
currentArena2x2.value = 0
desiredArena2x2.value = 0
var currentArena2x2_InputValue = parseFloat(currentArena2x2Value.value);
var desiredArena2x2_InputValue = parseFloat(desiredArena2x2Value.value);

function getArena2x2Price() {
  let result = (desiredArena2x2Value.value - currentArena2x2Value.value) * 0.02

  // Apply extra charges to the result
  result += result * total_Percentage;
  result = parseFloat(result.toFixed(2)); 

  // From Value
  $('.arena-boost input[name="current_RP"]').val(currentArena2x2Value.value);
  $('.arena-boost input[name="desired_RP"]').val(desiredArena2x2Value.value);
  $('.arena-boost input[name="price"]').val(result);
}

getArena2x2Price()

// Current Arena 2x2
currentArena2x2.addEventListener('input', function() {
  currentArena2x2Value.value = currentArena2x2.value;
  getArena2x2Price()
});
currentArena2x2Value.addEventListener('input', function() {
  if (!isNaN(currentArena2x2_InputValue)) {
    currentArena2x2.value = currentArena2x2_InputValue;
    getArena2x2Price()
  }
});
currentArena2x2Value.addEventListener('input', function() {
  currentArena2x2.value = currentArena2x2Value.value;
  getArena2x2Price()
});

// Desired Arena 2x2
desiredArena2x2.addEventListener('input', function() {
  desiredArena2x2Value.value = desiredArena2x2.value;
  getArena2x2Price()
});
desiredArena2x2Value.addEventListener('input', function() {
  if (!isNaN(desiredArena2x2_InputValue)) {
    desiredArena2x2.value = desiredArena2x2_InputValue;
    getArena2x2Price()
  }
});
desiredArena2x2Value.addEventListener('input', function() {
  desiredArena2x2.value = desiredArena2x2Value.value;
  getArena2x2Price()
});
