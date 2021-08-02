var xDown = null;                                                        
var yDown = null;

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

function handleTouchMove(evt) {
if ( ! xDown || ! yDown ) {
    return;
}

var xUp = evt.touches[0].clientX;                                    
var yUp = evt.touches[0].clientY;

var xDiff = xDown - xUp;
var yDiff = yDown - yUp;
                                                                     
if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {
    new Promise(resolve => setTimeout(resolve, 700)).then(() => {
          const height = Math.min(
             document.querySelector('.is-active.is-visible .classified-image').offsetHeight,
             visualViewport.height * 0.7
          );

         document.getElementById('image-overlay').style.top =  height - 34 + 'px';
         document.getElementById('image-section').style.maxHeight = height + 'px';
    });
 }
 xDown = null;
 yDown = null;                                             
};

function handleTouchStart(evt) {
    const firstTouch = evt.touches[0];                                      
    xDown = firstTouch.clientX;                                      
    yDown = firstTouch.clientY;                                      
};

document.addEventListener('DOMContentLoaded', function () {
    wx.ready(function(){
      try {
          wx.onMenuShareAppMessage({ 
                title: title, 
                desc: str_price + descr, 
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
                desc: str_price + descr, 
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
