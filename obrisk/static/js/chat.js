/*! chat.js | Friendkit | © Css Ninja. 2018-2019 */
$(document).ready((function(){"use strict";$(".close-chat, .open-chat").on("click",(function(){$(".chat-wrapper").toggleClass("is-active"),$("body").toggleClass("is-frozen")})),$("#chat-panel .panel-close").on("click",(function(){$("#chat-body, #chat-panel").removeClass("is-opened")})),$("#chat-sidebar .user-item").on("click",(function(){var a=$(this).attr("data-chat-user"),e=$(this).find("img").attr("src"),s=$(this).attr("data-full-name"),t=$(this).attr("data-status");$(".user-item.is-active").removeClass("is-active"),$(this).addClass("is-active"),$("#chat-body, #chat-panel").addClass("is-opened"),$(".chat-body-inner").addClass("is-hidden"),$("#"+a+"-conversation").removeClass("is-hidden"),$(".panel-body").addClass("is-hidden"),$("#"+a+"-details").removeClass("is-hidden"),$(".recipient-block").find(".user-avatar").attr("src",e),$(".recipient-block").find(".username span:first-child").text(s),$(".recipient-block").find(".username span span").text("| "+t)}))}));