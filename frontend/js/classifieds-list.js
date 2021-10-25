let page = 1;
let empty_page = false;
let block_request = false;
let lastScrollTop = 0;
let is_search = false;

function renderClassifieds(classifieds) {
  for (const cls of classifieds) {
      let img, price, template; 
      let t = typeof(cls.thumbnail); 

      if (t != "null" && t != "object" && cls.thumbnail != "" ) {
        img = `<img decoding="async" loading="lazy" class="card-img"
          src="${oss_url}/${cls.thumbnail}" width="154px" height="154px">`;
      }else {
        img = `<img decoding="async" loading="lazy"  width='154' height='154'
         class='card-img' src='${window.location.origin}/static/img/nophoto.jpg'>`;
      }

      if (cls.price == 0.00){
          price = "<p class='card-subtitle'> FREE </p>";
      } else if (typeof(cls.price) == 'object') {
          price = "<p class='card-subtitle'> BID PRICE </p>";
      } else {
          price = `<p class="card-subtitle"> ¥${cls.price} </p>`;
      }

      if (cls.status === "E" ) {
          template = `
            <div class="card classified-card expired">
              <a href="${window.location.origin}/classifieds/${cls.slug}"
                  class="black-link">

                <div class="card-img-top img-responsive">
                    ${img}
                </div>

                <div class="card-body">
                  <h6 class="card-title"> ${cls.title} </h6>
                   ${price}

                <span class="card-text small "><small>📍</small> ${ cls.city}</span>

                </div>
              </a>
            </div>
                `;
      } else {
          template = `
            <div class="card classified-card">
              <a href="${window.location.origin}/classifieds/${cls.slug}"
                  class="black-link">

                <div class="card-img-top img-responsive">
                    ${img}
                </div>

                <div class="card-body">
                  <h6 class="card-title"> ${cls.title} </h6>
                   ${price}

                <span class="card-text small "><small>📍</small> ${ cls.city}</span>

                </div>
              </a>
            </div>
                `;
      }

      document.getElementById('classifieds').insertAdjacentHTML('beforeend', template);
   }
 }

function searchSubmit(e, formInput) {
  e.preventDefault();                                                                                                          
  if (formInput.value.length > 1) {
  try{
      fetch(search_url + formInput.value, {
        credentials: 'same-origin',
        headers: {
        "X-Requested-With": "XMLHttpRequest"
        },
        redirect: 'follow',
      }).then (resp => resp.json())
        .then (data => {
            if (data.code == 201) {
                document.getElementById('not-found').style.display = 'none';
                document.getElementById('classifieds').remove();
                document.querySelector(
                        '.classifieds-list-wrapper'
                    ).insertAdjacentHTML(
                        'afterbegin', '<div id="classifieds" class="small-cards-listing">'
                );
                renderClassifieds(data.classifieds);
                is_search = true;
            } else {
                if (data.code == 602) {
                    document.getElementById('not-found').style.display = 'flex';
                }
            }
        })
  }catch (e){
      console.log(e);
      document.getElementById('not-found').style.display = 'flex';
     }
  }
}

if ( !iPhone && sessionStorage["restoreScroll"] === "true" ) {
    page = parseInt(sessionStorage["page"]);
    is_search = JSON.parse(sessionStorage["is_search"]);
    document.getElementById('classifieds').remove();
    document.querySelector(
            '.classifieds-list-wrapper'
        ).innerHTML = JSON.parse(localStorage.getItem('loadedPosts'));
    
    const end = document.querySelector('.end-classifieds')
    if (end !== null) end.remove();

    document.body.scrollTop = sessionStorage.getItem("scrollPosition");
    document.documentElement.scrollTop = sessionStorage.getItem("scrollPosition");
    sessionStorage.removeItem("restoreScroll");
    sessionStorage.setItem("scrollPosition", "0");
    sessionStorage.setItem("page", "0");
    sessionStorage.setItem("page", "false");
}

document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.classifieds-list-wrapper').addEventListener('click', e => {
       sessionStorage.setItem("restoreScroll", true);
    });


   window.addEventListener('scroll', function () {
      if (!iPhone && document.getElementById('navbarBottom').style.display === 'none'){
         document.getElementById('navbarBottom').style.display = 'block';
      }

      if (document.getElementById('search-input').value === "" || is_search === false) {
          let st = window.pageYOffset || document.documentElement.scrollTop;

          if (empty_page == false && block_request == false && st > lastScrollTop) {
            block_request = true;
            page += 1;
            document.querySelector('.loading').classList.remove('is-hidden')

            window.requestAnimationFrame(function() {
                fetch(`${window.location.href.split('#')[0]}?page=${page}`,
                {
                  headers: {
                "X-Requested-With": "XMLHttpRequest"
                  }
                }).then (resp => resp.json())
                .then (data => {

                    document.querySelector('.loading').classList.add('is-hidden');
                    block_request = false;
                    renderClassifieds(data.classifieds) 

                      if (data.end === "end") {
                        empty_page = true;
                        document.querySelector('.loading').classList.add('is-hidden');
                      } 

                }).catch (err => {
                   console.log(err);
                });
            });
          }
          lastScrollTop = st <= 0 ? 0 : st;
     }
    });

    const searchForm = document.getElementById('search-form');
    const formInput = document.getElementById("search-input");

  window.onbeforeunload = function (event) {
      sessionStorage.setItem(
          "scrollPosition",
          Math.max(document.body.scrollTop, document.documentElement.scrollTop)
      );
      sessionStorage.setItem(
          "page",
           page
      );
      sessionStorage.setItem(
          "is_search",
           is_search
      );
    const htmlContents = document.querySelector(
            '.classifieds-list-wrapper'
        ).innerHTML;
    localStorage.setItem('loadedPosts', JSON.stringify(htmlContents));
  }

  searchForm.addEventListener('submit', function(e) {
      searchSubmit(e, formInput);
  });

  wx.ready(function(){
      try {
          wx.onMenuShareAppMessage({ 
                title: "Obrisk Secondhand Marketplace", 
                desc: "Check out lots of stuff selling right now or post yours", 
                link: location.href, 
                imgUrl: share_img, 
                trigger: function (res) {
                    console.log(JSON.stringify(res));
                },
                success: function (res) {
                    console.log(JSON.stringify(res));
                },
                fail: function (res) {
                    console.log(JSON.stringify(res));
                }
            })

          wx.onMenuShareTimeline({ 
                title: "Obrisk Secondhand Marketplace", 
                desc: "Check out lots of stuff selling right now or post yours", 
                link: location.href, 
                imgUrl: share_img, 
                trigger: function (res) {
                    console.log(JSON.stringify(res));
                },
                success: function (res) {
                    console.log(JSON.stringify(res));
                },
                fail: function (res) {
                    console.log(JSON.stringify(res));
                }
            })
        }catch (e) {
            console.log(e);
        }
  });

  wx.error(function(res){
    console.log(res);
  });
});

