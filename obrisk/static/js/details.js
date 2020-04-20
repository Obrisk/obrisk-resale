//Common js for classifieds and posts details
//

function shareMe(title, text) {
    navigator.share({
      title: title,
      text: text,
      url: location.href,
    });
}
