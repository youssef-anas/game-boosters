function applyReadMore(element) {
  let messageContent = element.textContent.trim();
  if (messageContent.length > 200) {
    let readMoreLink = document.createElement("span");
    readMoreLink.classList.add("read-more-link");
    readMoreLink.innerHTML = "<span class='dots'> ...</span>Read more";
    element.textContent = messageContent.substring(0, 200);
    element.appendChild(readMoreLink);

    readMoreLink.addEventListener("click", function () {
      element.textContent = messageContent;
    });
  }
}

document.querySelectorAll(".message").forEach(function (element) {
  applyReadMore(element);
});
