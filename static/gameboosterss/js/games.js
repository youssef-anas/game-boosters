/*=============== SWIPER JS ===============*/
let gamesSwiperCards = new Swiper('.games-swiper', {
  // loop: true,
  spaceBetween: 32,
  grabCursor: true,
  slidesPerView: 1, // Start with 1 slide per view

  navigation: {
    nextEl: '.games-swiper-button-next',
    prevEl: '.games-swiper-button-prev',
  },

  breakpoints: {
    700: {
      slidesPerView: 2,
    },
    810: {
      slidesPerView: 4,
    },
    1200: {
      slidesPerView: 6,
    },
  },

  // Control how much of the next slide is visible
  slidesOffsetAfter: 10, // Adjust this value as needed
});