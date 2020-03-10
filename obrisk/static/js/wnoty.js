/**
 * wnoty.js v0.1
 * https://qcode.site
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 */
!(function($, win, doc) {
  "use strict";
  var _doc = $(doc),
    _win = $(win),
    wnoty = doc.createElement("div"),
    notify = "wnoty",
    _notify = "#",
    error = function(e) {
      throw "error: Cannot Notify => " + e;
    },
    warn = function(l) {
      console.warn == "undefiend"
        ? console.log("Notify Warning: " + l)
        : console.warn("Notify Warning: " + l);
    },
    in_array = function(array, value) {
      for (var i = 0; i < array.length; i++) {
        if (array[i] === value) return true;
      }
      return false;
    },
    PrefixedEvent = function(element, type, callback) {
      var pfx = ["webkit", "moz", "MS", "o", ""];
      for (var p = 0; p < pfx.length; p++) {
        if (!pfx[p]) type = type.toLowerCase();
        _doc.on(pfx[p] + type, element, callback);
      }
    },
    closeNotify = function(button) {
      button
        .parents("." + notify + "-notification")
        .removeClass("" + notify + "-show");
      setTimeout(function() {
        button
          .parents("." + notify + "-notification")
          .addClass("" + notify + "-hide");
      }, 25);
    },
    initialize = function(set) {
      var main = doc.createElement("div"),
        wrapper = doc.createElement("div"),
        icon = doc.createElement("i"),
        text = doc.createElement("p"),
        close = doc.createElement("span");
      for (var g = 0; g < $("." + notify + "-notification").length; g++) {
        var g = g;
      }
      wnoty.className = "" + notify + "-block " + notify + "-" + set.position;
      main.className =
        "" +
        notify +
        "-notification " +
        notify +
        "-" +
        set.type +
        " leight-" +
        g;
      main.id = "leight-" + g;
      wrapper.className = notify + "-wrapper";
      if (set.type == "error") {
        icon.className = notify + "-icon fa fa-times-circle";
      } else if (set.type == "success") {
        icon.className = notify + "-icon fa fa-check-circle";
      } else if (set.type == "warning") {
        icon.className = notify + "-icon fa fa-exclamation-triangle";
      } else if (set.type == "info") {
        icon.className = notify + "-icon fas fa-info-circle";
      }
      close.className = "wnoty-close";
      doc.body.append(wnoty);
      wnoty.prepend(main);
      main.appendChild(wrapper);
      main.appendChild(close);
      wrapper.appendChild(icon);
      wrapper.appendChild(text);
      text.innerHTML = set.message;
      $("." + notify + "-notification").removeClass("wnoty-show");
      $("#leight-" + g).addClass("wnoty-show");
      if (set.autohide == true) {
        setTimeout(function() {
          closeNotify($(close));
        }, set.autohideDelay);
      }
    };
  $.wnoty = function(options) {
    var positions = ["top-left", "bottom-left", "top-right", "bottom-right"],
      types = ["error", "success", "warning", "info"],
      defaults = {
        position: positions[2]
      },
      settings = {
        message: "",
        type: "",
        autohide: true,
        autohideDelay: 2500,
        position: positions[2]
      };
    $.extend(settings, options);
    if (settings.type == "" && !settings.type.length)
      error("Type is not defined!");
    if (!in_array(types, settings.type)) error("Uhh, invalid notify type!");
    if (settings.message == "" && !settings.message.length)
      error("Hmmm, Message seems to be empty or not defined!");
    if (!in_array(positions, settings.position)) {
      warn("Oh, Invalid position switching to default!");
      settings.position = defaults.position;
    }
    if ($("." + notify + "-notification").length >= 10) {
      $("." + notify + "-notification:last").remove();
    }
    initialize(settings);
  };
  PrefixedEvent($("." + notify + "-notification"), "AnimationEnd", function() {
    $(".wnoty-notification.wnoty-hide").remove();
  });
  _doc.on("click", ".wnoty-close", function() {
    closeNotify($(this));
  });
  console.log(
    "Notify by WOLK! %c qcode.site ",
    "background:#7266ba;color:#fff"
  );
})(window.jQuery, window, document);
