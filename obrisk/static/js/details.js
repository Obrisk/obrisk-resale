//Common js for classifieds and posts details pages

function goToEdit () {
    window.location.href=editUrl;
}

function shareMe(title, text) {
    navigator.share({
      title: title,
      text: text,
      url: location.href,
    });
}
