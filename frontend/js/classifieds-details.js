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


document.addEventListener('DOMContentLoaded', function () {
    const chatBtn = document.getElementById('chat-button-id');

    if( chatBtn !== null) {
	  chatBtn.addEventListener('click', () => {
	      if (currentUser !== undefined) {
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
});
