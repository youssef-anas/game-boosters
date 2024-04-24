/*=============== SWIPER JS ===============*/
let gamesSwiperCards = new Swiper('.games-swiper', {
  // loop: true,
  spaceBetween: 32,
  grabCursor: true,
  slidesPerView: 1,

  navigation: {
    nextEl: '.games-swiper-button-next',
    prevEl: '.games-swiper-button-prev',
  },

  breakpoints: {
    200: {
      slidesPerView: 1.3,
    },
    450: {
      slidesPerView: 2.3,
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