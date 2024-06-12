/*=============== SWIPER JS ===============*/
let swiperCards = new Swiper('.orders-swiper', {
  spaceBetween: 40,
  grabCursor: true,
  slidesPerView: 1, // Start with 1 slide per view

  breakpoints: {
    700: {
      slidesPerView: 2,
    },
    810: {
      slidesPerView: 2,
    },
    1000: {
      slidesPerView: 3,
    },
    1200: {
      slidesPerView: 4,
    },
  },

  // Control how much of the next slide is visible
  slidesOffsetAfter: 40, // Adjust this value as needed
});