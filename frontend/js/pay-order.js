function wxpayFail() {
      document.getElementsByClassName('notification')[0].classList.remove('is-hidden'); 
      document.getElementById(
              'notf-msg'
          ).innerHTML = "Sorry payments feature is now unavailable, contact the seller directly";

      setTimeout(() => {  
          window.location.href=slugURL;
      }, 7000);
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

                  if (!getCookie('classified-order-is-offline')) {
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
                         "X-Requested-With": "XMLHttpRequest"
                      },
                      credentials: 'same-origin',
                      redirect: 'follow'
                    }).then (resp => resp.json())
                      .then (strData => {
                      let data = JSON.parse(strData);
                      if (data.success === true) {
                          window.location.replace= 'classifieds/orders/wsguatpotlfwccdi/' + data.order_slug;
                      }
                  })
                },
                fail: function (res) {
                    wxpayFail();
                    console.log(JSON.stringify(res));
                },
                cancel: function (res) {
                  window.location.replace=slugURL;
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
