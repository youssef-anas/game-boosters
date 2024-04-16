function extractOrderFrom(text) {
  const startMarker = "From ";
  const endMarker = " To";
  const startIndex = text.indexOf(startMarker);
  const endIndex = text.indexOf(endMarker, startIndex + startMarker.length);
  
  if (startIndex !== -1 && endIndex !== -1) {
    return text.substring(startIndex + startMarker.length, endIndex);
  } else {
    return "";
  }
}

function extractOrderTo(text) {
  const startMarker = "To ";
  const startIndex = text.indexOf(startMarker);

  if (startIndex !== -1) {
    return text.substring(startIndex + startMarker.length);
  } else {
    return "";
  }
}
