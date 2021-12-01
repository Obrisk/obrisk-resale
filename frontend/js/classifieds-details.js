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
                      title="Share this classified" id="share">
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


const ui = {
  showMask() {
    if (document.querySelector('.m-share-mask')) {
      return;
    }
    const $div = document.createElement('div');
    $div.className = 'm-share-mask';
    $div.addEventListener('click', () => {
      this.hideRightTips();
      this.hideMask();
    });
    document.body.appendChild($div);
    window.setTimeout(() => {
      $div.style.opacity = 0.7;
    }, 0);
  },
  hideMask() {
    const domList = document.querySelectorAll('.m-share-mask');
    for (let i = 0; i < domList.length; i++) {
      const item = domList[i];
      const removeDom = () => item.remove();
      // 渐变消失
      // item.addEventListener('webkitTransitionend', removeDom);
      // item.addEventListener('transitionend', removeDom);
      // item.style.cssText = 'opacity: 0';
      removeDom();
    }
  },
  showRightTopTips() {
    this.showMask();
    const $tips = document.createElement('div');
    $tips.className = 'm-share-tips';
    $tips.innerHTML = `
      <div class="m-share-tips-w">
        <div class="m-share-tips-p">Please tap the 3 dots“<i class="m-share-iconfont m-share-iconfont-dots"></i>”</div>
        <div class="m-share-tips-p">On the upper right corner</div>
      </div>
      <div class="m-share-tips-arrow"></div>
    `;
    document.body.appendChild($tips);
    window.setTimeout(() => {
      this.hideMask();
      this.hideRightTips();
    }, 1400);
  },
  hideRightTips() {
    const domList = document.querySelectorAll('.m-share-tips');
    for (let i = 0; i < domList.length; i++) {
      const item = domList[i];
      item.remove();
    }
  }
};


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

      const shareBtn = document.getElementById('share');

      if( shareBtn !== null) {
          shareBtn.addEventListener('click', () => {
              if (wechat_browser) {
                 ui.showRightTopTips();
              }else {
                 navigator.share({
                  title: title, 
                  text: str_price + " " + descr,
                  url: location.href,
                });
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
