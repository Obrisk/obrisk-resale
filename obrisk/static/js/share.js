navigator.share =
  navigator.share ||
  (function() {
    if (navigator.share) {
      return navigator.share;
    }

    let android = navigator.userAgent.match(/Android/i);
    let ios = navigator.userAgent.match(/iPhone|iPad|iPod/i);
    let isDesktop = !(ios || android); // on those two support "mobile deep links", so HTTP based fallback for all others.

    // sms on ios 'sms:;body='+payload, on Android 'sms:?body='+payload
    let shareUrls = {
      whatsapp: payload =>
        (isDesktop
          ? "https://api.whatsapp.com/send?text="
          : "whatsapp://send?text=") + payload,
      facebook: (payload, fbid, url) =>
        !fbid
          ? ""
          : (isDesktop
              ? "https://www.facebook.com/dialog/share?app_id=" +
                fbid +
                "&display=popup&href=" +
                url +
                "&redirect_uri=" +
                encodeURIComponent(location.href) +
                "&quote="
              : "fb-messenger://share/?message=") + payload,
      email: (payload, title) =>
        "mailto:?subject=" + title + "&body=" + payload,
      sms: payload => "sms:?body=" + payload
    };

    class WebShareUI {
      /*async*/
      _init() {
        if (this._initialized) return Promise.resolve();
        this._initialized = true;

        const template = `<div class="web-share" style="display: none">
      <div class="web-share-container web-share-grid">
        <div class="web-share-title">SHARE VIA</div>
        <a class="web-share-item web-share-whatsapp" data-action="share/whatsapp/share" target="_blank">
          <div class="web-share-icon-whatsapp"></div>
          <div class="web-share-item-desc">Whatsapp</div>
        </a>
        <a class="web-share-item web-share-email">
          <div class="web-share-icon-email"></div>
          <div class="web-share-item-desc">Email</div>
        </a>
        <a class="web-share-item web-share-sms">
          <div class="web-share-icon-sms"></div>
          <div class="web-share-item-desc">SMS</div>
        </a>
        <a class="web-share-item web-share-copy">
          <div class="web-share-icon-copy"></div>
          <div class="web-share-item-desc">Copy</div>
        </a>
      </div>
      <div class="web-share-container web-share-cancel">Cancel</div>
    </div>`;

        const el = document.createElement("div");
        el.innerHTML = template;

        this.$root = el.querySelector(".web-share");
        this.$whatsapp = el.querySelector(".web-share-whatsapp");
        this.$email = el.querySelector(".web-share-email");
        this.$sms = el.querySelector(".web-share-sms");
        this.$copy = el.querySelector(".web-share-copy");
        this.$copy.onclick = () => this._copy();
        this.$root.onclick = () => this._hide();
        this.$root.classList.toggle("desktop", isDesktop);

        document.body.appendChild(el);
      }

      _setPayload(payloadObj) {
        let payload = payloadObj.text + " " + payloadObj.url;
        let title = payloadObj.title;
        this.url = payloadObj.url;
        payload = encodeURIComponent(payload);
        title = encodeURIComponent(title);
        this.$whatsapp.href = shareUrls.whatsapp(payload);
        this.$email.href = shareUrls.email(payload, title);
        this.$sms.href = shareUrls.sms(payload);
      }

      _copy() {
        // A <span> contains the text to copy
        const span = document.createElement("span");
        span.textContent = this.url;
        span.style.whiteSpace = "pre"; // Preserve consecutive spaces and newlines

        // Paint the span outside the viewport
        span.style.position = "absolute";
        span.style.left = "-9999px";
        span.style.top = "-9999px";

        const win = window;
        const selection = win.getSelection();
        win.document.body.appendChild(span);

        const range = win.document.createRange();
        selection.removeAllRanges();
        range.selectNode(span);
        selection.addRange(range);

        let success = false;
        try {
          success = win.document.execCommand("copy");
        } catch (err) {}

        selection.removeAllRanges();
        span.remove();

        return success;
      }

      /*async*/
      show(payloadObj) {
        this._init();
        clearTimeout(this._hideTimer);
        this._setPayload(payloadObj);
        this.$root.style.display = "flex";
        this.$root.offsetWidth; // style update
        this.$root.style.background = "rgba(0,0,0,.4)";
        document.querySelectorAll(".web-share-container").forEach(el => {
          el.style.transform = "translateY(0)";
          el.style.opacity = 1;
        });
      }

      _hide() {
        this.$root.style.background = null;
        document.querySelectorAll(".web-share-container").forEach(el => {
          el.style.transform = null;
          el.style.opacity = null;
        });
        this._hideTimer = setTimeout(
          () => (this.$root.style.display = null),
          400
        );
      }
    }

    const shareUi = new WebShareUI();

    /* async */
    return data => shareUi.show(data);
  })();

/* Todo: auto select value to open native copy/share dialog */

/* Todo: facebook share message dialog for desktops
http://www.facebook.com/dialog/send
	?app_id=123456789
		&link=http://www.nytimes.com/
		&redirect_uri=https://www.domain.com/
	*/

// See also: http://chriswren.github.io/native-social-interactions/

// See also: https://www.sharethis.com/platform/share-buttons/
