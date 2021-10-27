//This function is called inside HTML File, inlined onclick event
function callpay() {
    if (isNaN(price) || price  === "0.00") {
        document.getElementById('payError').innerHTML = "Only priced items can accept payments";        
        setTimeout(() => {  
             document.getElementById('payError').innerHTML = "";
        }, 7000);
        return;
    }

    const sg = encodeURIComponent(slug);
    window.location.href = orderUrl + sg;
}

function onSale(element) {
      const sibling = document.getElementById('meta-info');
      if (element.checked) {
          const template = `
              <div class="action-wrapper" id=actions">
                  <a class="button action-button chat-button" href="${editItem}"
                      title="Edit this classified">
                      ✎Edit
                  </a>
                  <a class="button action-button pay-button" href="#"
                      title="Edit this classified">
                      📤Share
                  </a>
              </div>`
          sibling.nextElementSibling.remove();
          sibling.insertAdjacentHTML('afterend', template);
  
      } else {
          const template = `
              <div class="notification is-warning" id="unavailable">
                This item is no longer available
              </div>`
          sibling.nextElementSibling.remove();
          sibling.insertAdjacentHTML('afterend', template);
      }
}

document.addEventListener('DOMContentLoaded', function () {
    wx.ready(function(){
      try {
          wx.onMenuShareAppMessage({ 
                title: title, 
                desc: str_price + " " + descr, 
                link: location.href, 
                imgUrl: thumbnail, 
                trigger: function (res) {
                    console.log(JSON.stringify(res));
                },
                success: function (res) {
                    console.log(JSON.stringify(res));
                },
                fail: function (res) {
                    console.log(JSON.stringify(res));
                }
            });

          wx.onMenuShareTimeline({ 
                title: title, 
                desc: str_price + " " + descr, 
                link: location.href, 
                imgUrl: thumbnail, 
                trigger: function (res) {
                    console.log(JSON.stringify(res));
                },
                success: function (res) {
                    console.log(JSON.stringify(res));
                },
                fail: function (res) {
                    console.log(JSON.stringify(res));
                }
            });
        }catch (e) {
            console.log(e);
        }
      });

      wx.error(function(res){
        console.log(res);
      });


      const chatBtn = document.getElementById('chat-button-id');

      if( chatBtn !== null) {
          chatBtn.addEventListener('click', () => {
              if (typeof currentUser !== 'undefined') {
                  window.location.href = chatUrl;
              }else {
                  if (wechat_browser) {
                    window.location.href = wechatAuth;
                  }else {
                    window.location.href = loginUrl;
                  }
              }
          });
      }

      const tags = document.getElementById('tags');
      if (tags !== null) {
          tags.addEventListener('click', () => {
              sessionStorage["restoreScroll"] = "false";
          });
      }
});

if (typeof toggler !== 'undefined') {
  window.onbeforeunload = function () {
      let stat = 'E';

      if (toggler.checked !== switch_value) {
          if (toggler.checked === true) {
              stat = 'A';
          } else {
              stat = 'E';
          }

          fetch(removeUrl, {
              method : "POST",
              body: JSON.stringify({
                  sg:slug,
                  st:stat
              }),
              headers: {
                 "X-Requested-With": "XMLHttpRequest",
                 "Content-Type": "application/json"
              },
              credentials: 'same-origin',
              redirect: 'follow'
            }).then (resp => {
                 ;
            }).catch ((e) => {
                console.error('failure to toggle item availability', e);
            })
      } else {
         ;
      }
  };
}
