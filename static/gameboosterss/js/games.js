/*=============== SWIPER JS ===============*/
let gamesSwiperCards = new Swiper('.games-swiper', {
  loop: true,
  grabCursor: true,
  slidesPerView: 1,

  navigation: {
    nextEl: '.games-swiper-button-next',
    prevEl: '.games-swiper-button-prev',
  },

  breakpoints: {
    200: {
      slidesPerView: 3,
      spaceBetween: 12,
    },
    800: {
      slidesPerView: 6,
      spaceBetween: 24,
    },
    1200: {
      slidesPerView: 6,
      spaceBetween: 32,
    },
  },

  // Control how much of the next slide is visible
  slidesOffsetAfter: 10, // Adjust this value as needed
});