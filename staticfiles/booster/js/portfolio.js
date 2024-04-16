/*=============== SWIPER JS ===============*/
let portfolioSwiperCards = new Swiper('.portfolio-swiper', {
  // loop: true,
  spaceBetween: 32,
  grabCursor: true,

  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  breakpoints: {
    700: {
      slidesPerView: 1,
    },
    810: {
      slidesPerView: 2,
    },
    1200: {
      slidesPerView: 3,
    },
  },

});