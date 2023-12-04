$(document).ready(function () {
  const radioButtonsRank = $('input[name="radio-group-ranks"]');
  const sliderEl = $("#game-count");
  const sliderValue = $(".value");
  const gameCounterInitial = Number(sliderEl.val())

  const initiallyCheckedIndexRank = $('input[name="radio-group-ranks"]').index($('input[name="radio-group-ranks"]:checked'));
  const initiallyCheckedRank = $('input[name="radio-group-ranks"]').eq(initiallyCheckedIndexRank);
  const initiallyCheckedIndexRankPrice = initiallyCheckedRank.data('price');

  let rank = initiallyCheckedIndexRank
  let rank_price = initiallyCheckedIndexRankPrice
  let gameCounter = gameCounterInitial

  const getPrices = () => {
    const price = parseFloat((rank_price * gameCounter).toFixed(2));
    console.log("Final Price", price)
    const pricee = $('.price-data.placements-boost').eq(0);
    pricee.html(`
    <p class='fs-5 text-uppercase my-4'>Boosting of <span class='fw-bold'>${gameCounter} Placement Games</span></p>
    <h4>$${price}</h4>
`);
  }
  getPrices()


  radioButtonsRank.each(function (index, radio) {
    $(radio).on('change', function () {
      const selectedIndex = radioButtonsRank.index(radio);
      console.log('Selected index:', selectedIndex);
      rank = selectedIndex;
      rank_price = $(radio).data('price');
      getPrices()
    });
  });


  sliderEl.on("input", function (event) {
    gameCounter = Number(event.target.value);
    console.log('count', gameCounter);

    sliderValue.text(gameCounter);

    const progress = (gameCounter / sliderEl.prop("max")) * 100;

    sliderEl.css("background", `linear-gradient(to right, var(--main-color) ${progress}%, #ccc ${progress}%)`);

    sliderEl.css("--thumb-rotate", `${(gameCounter / 100) * 2160}deg`);

    getPrices()
  });
});
