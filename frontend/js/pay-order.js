function wxpayFail(pay_complete=false) {
    document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 

    if (pay_complete === true) {
        document.getElementById(
              'notf-msg'
          ).innerHTML = "Payment done✌️. We'll get in touch soon to confirm the logistics😊";
    } else {
        document.getElementById(
              'notf-msg'
          ).innerHTML = "Sorry payments feature is now unavailable, contact the seller directly🙇";
    }

    setTimeout(() => {  
      window.location.href=slugURL;
    }, 9000);
}

document.addEventListener('DOMContentLoaded', function () {

    wx.ready(function(){
        if (dataError.length > 1) {
           wxpayFail();
           console.log(dataError);
        }else {
	      try {
		    wx.chooseWXPay({
                timestamp: timestamp, 
                nonceStr: nonceStr,
                package: packge, 
                signType: signType,
                paySign: paySign,
                trigger: function (res) {
                    console.log(JSON.stringify(res));
                },
                success: function (res) {
                  let phone = null;
                  let addr = null; 

                  if (getCookie('classified-order-is-offline') === "false") {
                      phone = getCookie('classified-order-phone');
                      addr = getCookie('classified-order-address');
                  }

                  fetch(paySuccessURL, {
                      method : "POST",
                      body: JSON.stringify({
                          addr:addr,
                          phone: phone,
                          sg:slug
                      }),
                      headers: {
                         "X-Requested-With": "XMLHttpRequest",
                         "Content-Type": "application/json"
                      },
                      credentials: 'same-origin',
                      redirect: 'follow'
                    }).then (resp => resp.json())
                      .then (data => {
                          if (data.success === true) {
                              window.location.replace('https://obrisk.com/i/orders/wsguatpotlfwccdi/' + data.order_slug);
                          } else {
                              wxpayFail(pay_complete=true);
                          }
                    }).catch ((e) => {
                        wxpayFail(pay_complete=true);
                        console.error('failure to init payments, exception happened', e);
                    })
                },
                fail: function (res) {
                    wxpayFail();
                    console.log(JSON.stringify(res));
                },
                cancel: function (res) {
                  window.location.replace(slugURL);
                }
		    });
	      } catch {
              wxpayFail();
              console.log('failure to init payments, exception happened');
	      }
       }
   });

    wx.error(function(res){
        wxpayFail();
        console.log(res);
    });

});
