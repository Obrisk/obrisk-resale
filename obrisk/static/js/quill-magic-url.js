!(function(t, e) {
  if ("object" == typeof exports && "object" == typeof module)
    module.exports = e();
  else if ("function" == typeof define && define.amd) define([], e);
  else {
    var r = e();
    for (var n in r) ("object" == typeof exports ? exports : t)[n] = r[n];
  }
})(window, function() {
  return (function(t) {
    var e = {};
    function r(n) {
      if (e[n]) return e[n].exports;
      var o = (e[n] = { i: n, l: !1, exports: {} });
      return t[n].call(o.exports, o, o.exports, r), (o.l = !0), o.exports;
    }
    return (
      (r.m = t),
      (r.c = e),
      (r.d = function(t, e, n) {
        r.o(t, e) || Object.defineProperty(t, e, { enumerable: !0, get: n });
      }),
      (r.r = function(t) {
        "undefined" != typeof Symbol &&
          Symbol.toStringTag &&
          Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
          Object.defineProperty(t, "__esModule", { value: !0 });
      }),
      (r.t = function(t, e) {
        if ((1 & e && (t = r(t)), 8 & e)) return t;
        if (4 & e && "object" == typeof t && t && t.__esModule) return t;
        var n = Object.create(null);
        if (
          (r.r(n),
          Object.defineProperty(n, "default", { enumerable: !0, value: t }),
          2 & e && "string" != typeof t)
        )
          for (var o in t)
            r.d(
              n,
              o,
              function(e) {
                return t[e];
              }.bind(null, o)
            );
        return n;
      }),
      (r.n = function(t) {
        var e =
          t && t.__esModule
            ? function() {
                return t.default;
              }
            : function() {
                return t;
              };
        return r.d(e, "a", e), e;
      }),
      (r.o = function(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e);
      }),
      (r.p = ""),
      r((r.s = 16))
    );
  })([
    function(t, e, r) {
      "use strict";
      var n = Object.prototype.hasOwnProperty,
        o = Object.prototype.toString,
        i = function(t) {
          return "function" == typeof Array.isArray
            ? Array.isArray(t)
            : "[object Array]" === o.call(t);
        },
        s = function(t) {
          if (!t || "[object Object]" !== o.call(t)) return !1;
          var e,
            r = n.call(t, "constructor"),
            i =
              t.constructor &&
              t.constructor.prototype &&
              n.call(t.constructor.prototype, "isPrototypeOf");
          if (t.constructor && !r && !i) return !1;
          for (e in t);
          return void 0 === e || n.call(t, e);
        };
      t.exports = function t() {
        var e,
          r,
          n,
          o,
          a,
          h,
          u = arguments[0],
          l = 1,
          f = arguments.length,
          c = !1;
        for (
          "boolean" == typeof u && ((c = u), (u = arguments[1] || {}), (l = 2)),
            (null == u || ("object" != typeof u && "function" != typeof u)) &&
              (u = {});
          l < f;
          ++l
        )
          if (null != (e = arguments[l]))
            for (r in e)
              (n = u[r]),
                u !== (o = e[r]) &&
                  (c && o && (s(o) || (a = i(o)))
                    ? (a
                        ? ((a = !1), (h = n && i(n) ? n : []))
                        : (h = n && s(n) ? n : {}),
                      (u[r] = t(c, h, o)))
                    : void 0 !== o && (u[r] = o));
        return u;
      };
    },
    function(t, e, r) {
      var n = Array.prototype.slice,
        o = r(13),
        i = r(12),
        s = (t.exports = function(t, e, r) {
          return (
            r || (r = {}),
            t === e ||
              (t instanceof Date && e instanceof Date
                ? t.getTime() === e.getTime()
                : !t || !e || ("object" != typeof t && "object" != typeof e)
                ? r.strict
                  ? t === e
                  : t == e
                : (function(t, e, r) {
                    var u, l;
                    if (a(t) || a(e)) return !1;
                    if (t.prototype !== e.prototype) return !1;
                    if (i(t))
                      return (
                        !!i(e) && ((t = n.call(t)), (e = n.call(e)), s(t, e, r))
                      );
                    if (h(t)) {
                      if (!h(e)) return !1;
                      if (t.length !== e.length) return !1;
                      for (u = 0; u < t.length; u++)
                        if (t[u] !== e[u]) return !1;
                      return !0;
                    }
                    try {
                      var f = o(t),
                        c = o(e);
                    } catch (t) {
                      return !1;
                    }
                    if (f.length != c.length) return !1;
                    for (f.sort(), c.sort(), u = f.length - 1; u >= 0; u--)
                      if (f[u] != c[u]) return !1;
                    for (u = f.length - 1; u >= 0; u--)
                      if (((l = f[u]), !s(t[l], e[l], r))) return !1;
                    return typeof t == typeof e;
                  })(t, e, r))
          );
        });
      function a(t) {
        return null === t || void 0 === t;
      }
      function h(t) {
        return (
          !(!t || "object" != typeof t || "number" != typeof t.length) &&
          "function" == typeof t.copy &&
            "function" == typeof t.slice &&
            !(t.length > 0 && "number" != typeof t[0])
        );
      }
    },
    function(t, e, r) {
      "use strict";
      var n = function(t) {
        switch (typeof t) {
          case "string":
            return t;
          case "boolean":
            return t ? "true" : "false";
          case "number":
            return isFinite(t) ? t : "";
          default:
            return "";
        }
      };
      t.exports = function(t, e, r, a) {
        return (
          (e = e || "&"),
          (r = r || "="),
          null === t && (t = void 0),
          "object" == typeof t
            ? i(s(t), function(s) {
                var a = encodeURIComponent(n(s)) + r;
                return o(t[s])
                  ? i(t[s], function(t) {
                      return a + encodeURIComponent(n(t));
                    }).join(e)
                  : a + encodeURIComponent(n(t[s]));
              }).join(e)
            : a
            ? encodeURIComponent(n(a)) + r + encodeURIComponent(n(t))
            : ""
        );
      };
      var o =
        Array.isArray ||
        function(t) {
          return "[object Array]" === Object.prototype.toString.call(t);
        };
      function i(t, e) {
        if (t.map) return t.map(e);
        for (var r = [], n = 0; n < t.length; n++) r.push(e(t[n], n));
        return r;
      }
      var s =
        Object.keys ||
        function(t) {
          var e = [];
          for (var r in t)
            Object.prototype.hasOwnProperty.call(t, r) && e.push(r);
          return e;
        };
    },
    function(t, e, r) {
      "use strict";
      function n(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e);
      }
      t.exports = function(t, e, r, i) {
        (e = e || "&"), (r = r || "=");
        var s = {};
        if ("string" != typeof t || 0 === t.length) return s;
        var a = /\+/g;
        t = t.split(e);
        var h = 1e3;
        i && "number" == typeof i.maxKeys && (h = i.maxKeys);
        var u = t.length;
        h > 0 && u > h && (u = h);
        for (var l = 0; l < u; ++l) {
          var f,
            c,
            p,
            g,
            y = t[l].replace(a, "%20"),
            m = y.indexOf(r);
          m >= 0
            ? ((f = y.substr(0, m)), (c = y.substr(m + 1)))
            : ((f = y), (c = "")),
            (p = decodeURIComponent(f)),
            (g = decodeURIComponent(c)),
            n(s, p)
              ? o(s[p])
                ? s[p].push(g)
                : (s[p] = [s[p], g])
              : (s[p] = g);
        }
        return s;
      };
      var o =
        Array.isArray ||
        function(t) {
          return "[object Array]" === Object.prototype.toString.call(t);
        };
    },
    function(t, e, r) {
      "use strict";
      (e.decode = e.parse = r(3)), (e.encode = e.stringify = r(2));
    },
    function(t, e, r) {
      "use strict";
      t.exports = {
        isString: function(t) {
          return "string" == typeof t;
        },
        isObject: function(t) {
          return "object" == typeof t && null !== t;
        },
        isNull: function(t) {
          return null === t;
        },
        isNullOrUndefined: function(t) {
          return null == t;
        }
      };
    },
    function(t, e) {
      var r;
      r = (function() {
        return this;
      })();
      try {
        r = r || Function("return this")() || (0, eval)("this");
      } catch (t) {
        "object" == typeof window && (r = window);
      }
      t.exports = r;
    },
    function(t, e) {
      t.exports = function(t) {
        return (
          t.webpackPolyfill ||
            ((t.deprecate = function() {}),
            (t.paths = []),
            t.children || (t.children = []),
            Object.defineProperty(t, "loaded", {
              enumerable: !0,
              get: function() {
                return t.l;
              }
            }),
            Object.defineProperty(t, "id", {
              enumerable: !0,
              get: function() {
                return t.i;
              }
            }),
            (t.webpackPolyfill = 1)),
          t
        );
      };
    },
    function(t, e, r) {
      (function(t, n) {
        var o;
        /*! https://mths.be/punycode v1.4.1 by @mathias */ !(function(i) {
          "object" == typeof e && e && e.nodeType,
            "object" == typeof t && t && t.nodeType;
          var s = "object" == typeof n && n;
          s.global !== s && s.window !== s && s.self;
          var a,
            h = 2147483647,
            u = 36,
            l = 1,
            f = 26,
            c = 38,
            p = 700,
            g = 72,
            y = 128,
            m = "-",
            v = /^xn--/,
            b = /[^\x20-\x7E]/,
            d = /[\x2E\u3002\uFF0E\uFF61]/g,
            x = {
              overflow: "Overflow: input needs wider integers to process",
              "not-basic": "Illegal input >= 0x80 (not a basic code point)",
              "invalid-input": "Invalid input"
            },
            j = u - l,
            w = Math.floor,
            O = String.fromCharCode;
          function A(t) {
            throw new RangeError(x[t]);
          }
          function k(t, e) {
            for (var r = t.length, n = []; r--; ) n[r] = e(t[r]);
            return n;
          }
          function E(t, e) {
            var r = t.split("@"),
              n = "";
            return (
              r.length > 1 && ((n = r[0] + "@"), (t = r[1])),
              n + k((t = t.replace(d, ".")).split("."), e).join(".")
            );
          }
          function C(t) {
            for (var e, r, n = [], o = 0, i = t.length; o < i; )
              (e = t.charCodeAt(o++)) >= 55296 && e <= 56319 && o < i
                ? 56320 == (64512 & (r = t.charCodeAt(o++)))
                  ? n.push(((1023 & e) << 10) + (1023 & r) + 65536)
                  : (n.push(e), o--)
                : n.push(e);
            return n;
          }
          function I(t) {
            return k(t, function(t) {
              var e = "";
              return (
                t > 65535 &&
                  ((e += O((((t -= 65536) >>> 10) & 1023) | 55296)),
                  (t = 56320 | (1023 & t))),
                (e += O(t))
              );
            }).join("");
          }
          function P(t) {
            return t - 48 < 10
              ? t - 22
              : t - 65 < 26
              ? t - 65
              : t - 97 < 26
              ? t - 97
              : u;
          }
          function S(t, e) {
            return t + 22 + 75 * (t < 26) - ((0 != e) << 5);
          }
          function T(t, e, r) {
            var n = 0;
            for (
              t = r ? w(t / p) : t >> 1, t += w(t / e);
              t > (j * f) >> 1;
              n += u
            )
              t = w(t / j);
            return w(n + ((j + 1) * t) / (t + c));
          }
          function L(t) {
            var e,
              r,
              n,
              o,
              i,
              s,
              a,
              c,
              p,
              v,
              b = [],
              d = t.length,
              x = 0,
              j = y,
              O = g;
            for ((r = t.lastIndexOf(m)) < 0 && (r = 0), n = 0; n < r; ++n)
              t.charCodeAt(n) >= 128 && A("not-basic"), b.push(t.charCodeAt(n));
            for (o = r > 0 ? r + 1 : 0; o < d; ) {
              for (
                i = x, s = 1, a = u;
                o >= d && A("invalid-input"),
                  ((c = P(t.charCodeAt(o++))) >= u || c > w((h - x) / s)) &&
                    A("overflow"),
                  (x += c * s),
                  !(c < (p = a <= O ? l : a >= O + f ? f : a - O));
                a += u
              )
                s > w(h / (v = u - p)) && A("overflow"), (s *= v);
              (O = T(x - i, (e = b.length + 1), 0 == i)),
                w(x / e) > h - j && A("overflow"),
                (j += w(x / e)),
                (x %= e),
                b.splice(x++, 0, j);
            }
            return I(b);
          }
          function U(t) {
            var e,
              r,
              n,
              o,
              i,
              s,
              a,
              c,
              p,
              v,
              b,
              d,
              x,
              j,
              k,
              E = [];
            for (d = (t = C(t)).length, e = y, r = 0, i = g, s = 0; s < d; ++s)
              (b = t[s]) < 128 && E.push(O(b));
            for (n = o = E.length, o && E.push(m); n < d; ) {
              for (a = h, s = 0; s < d; ++s)
                (b = t[s]) >= e && b < a && (a = b);
              for (
                a - e > w((h - r) / (x = n + 1)) && A("overflow"),
                  r += (a - e) * x,
                  e = a,
                  s = 0;
                s < d;
                ++s
              )
                if (((b = t[s]) < e && ++r > h && A("overflow"), b == e)) {
                  for (
                    c = r, p = u;
                    !(c < (v = p <= i ? l : p >= i + f ? f : p - i));
                    p += u
                  )
                    (k = c - v),
                      (j = u - v),
                      E.push(O(S(v + (k % j), 0))),
                      (c = w(k / j));
                  E.push(O(S(c, 0))), (i = T(r, x, n == o)), (r = 0), ++n;
                }
              ++r, ++e;
            }
            return E.join("");
          }
          (a = {
            version: "1.4.1",
            ucs2: { decode: C, encode: I },
            decode: L,
            encode: U,
            toASCII: function(t) {
              return E(t, function(t) {
                return b.test(t) ? "xn--" + U(t) : t;
              });
            },
            toUnicode: function(t) {
              return E(t, function(t) {
                return v.test(t) ? L(t.slice(4).toLowerCase()) : t;
              });
            }
          }),
            void 0 ===
              (o = function() {
                return a;
              }.call(e, r, e, t)) || (t.exports = o);
        })();
      }.call(this, r(7)(t), r(6)));
    },
    function(t, e, r) {
      "use strict";
      var n = r(8),
        o = r(5);
      function i() {
        (this.protocol = null),
          (this.slashes = null),
          (this.auth = null),
          (this.host = null),
          (this.port = null),
          (this.hostname = null),
          (this.hash = null),
          (this.search = null),
          (this.query = null),
          (this.pathname = null),
          (this.path = null),
          (this.href = null);
      }
      (e.parse = d),
        (e.resolve = function(t, e) {
          return d(t, !1, !0).resolve(e);
        }),
        (e.resolveObject = function(t, e) {
          return t ? d(t, !1, !0).resolveObject(e) : e;
        }),
        (e.format = function(t) {
          o.isString(t) && (t = d(t));
          return t instanceof i ? t.format() : i.prototype.format.call(t);
        }),
        (e.Url = i);
      var s = /^([a-z0-9.+-]+:)/i,
        a = /:[0-9]*$/,
        h = /^(\/\/?(?!\/)[^\?\s]*)(\?[^\s]*)?$/,
        u = ["{", "}", "|", "\\", "^", "`"].concat([
          "<",
          ">",
          '"',
          "`",
          " ",
          "\r",
          "\n",
          "\t"
        ]),
        l = ["'"].concat(u),
        f = ["%", "/", "?", ";", "#"].concat(l),
        c = ["/", "?", "#"],
        p = /^[+a-z0-9A-Z_-]{0,63}$/,
        g = /^([+a-z0-9A-Z_-]{0,63})(.*)$/,
        y = { javascript: !0, "javascript:": !0 },
        m = { javascript: !0, "javascript:": !0 },
        v = {
          http: !0,
          https: !0,
          ftp: !0,
          gopher: !0,
          file: !0,
          "http:": !0,
          "https:": !0,
          "ftp:": !0,
          "gopher:": !0,
          "file:": !0
        },
        b = r(4);
      function d(t, e, r) {
        if (t && o.isObject(t) && t instanceof i) return t;
        var n = new i();
        return n.parse(t, e, r), n;
      }
      (i.prototype.parse = function(t, e, r) {
        if (!o.isString(t))
          throw new TypeError(
            "Parameter 'url' must be a string, not " + typeof t
          );
        var i = t.indexOf("?"),
          a = -1 !== i && i < t.indexOf("#") ? "?" : "#",
          u = t.split(a);
        u[0] = u[0].replace(/\\/g, "/");
        var d = (t = u.join(a));
        if (((d = d.trim()), !r && 1 === t.split("#").length)) {
          var x = h.exec(d);
          if (x)
            return (
              (this.path = d),
              (this.href = d),
              (this.pathname = x[1]),
              x[2]
                ? ((this.search = x[2]),
                  (this.query = e
                    ? b.parse(this.search.substr(1))
                    : this.search.substr(1)))
                : e && ((this.search = ""), (this.query = {})),
              this
            );
        }
        var j = s.exec(d);
        if (j) {
          var w = (j = j[0]).toLowerCase();
          (this.protocol = w), (d = d.substr(j.length));
        }
        if (r || j || d.match(/^\/\/[^@\/]+@[^@\/]+/)) {
          var O = "//" === d.substr(0, 2);
          !O || (j && m[j]) || ((d = d.substr(2)), (this.slashes = !0));
        }
        if (!m[j] && (O || (j && !v[j]))) {
          for (var A, k, E = -1, C = 0; C < c.length; C++) {
            -1 !== (I = d.indexOf(c[C])) && (-1 === E || I < E) && (E = I);
          }
          -1 !== (k = -1 === E ? d.lastIndexOf("@") : d.lastIndexOf("@", E)) &&
            ((A = d.slice(0, k)),
            (d = d.slice(k + 1)),
            (this.auth = decodeURIComponent(A))),
            (E = -1);
          for (C = 0; C < f.length; C++) {
            var I;
            -1 !== (I = d.indexOf(f[C])) && (-1 === E || I < E) && (E = I);
          }
          -1 === E && (E = d.length),
            (this.host = d.slice(0, E)),
            (d = d.slice(E)),
            this.parseHost(),
            (this.hostname = this.hostname || "");
          var P =
            "[" === this.hostname[0] &&
            "]" === this.hostname[this.hostname.length - 1];
          if (!P)
            for (
              var S = this.hostname.split(/\./), T = ((C = 0), S.length);
              C < T;
              C++
            ) {
              var L = S[C];
              if (L && !L.match(p)) {
                for (var U = "", q = 0, R = L.length; q < R; q++)
                  L.charCodeAt(q) > 127 ? (U += "x") : (U += L[q]);
                if (!U.match(p)) {
                  var M = S.slice(0, C),
                    N = S.slice(C + 1),
                    z = L.match(g);
                  z && (M.push(z[1]), N.unshift(z[2])),
                    N.length && (d = "/" + N.join(".") + d),
                    (this.hostname = M.join("."));
                  break;
                }
              }
            }
          this.hostname.length > 255
            ? (this.hostname = "")
            : (this.hostname = this.hostname.toLowerCase()),
            P || (this.hostname = n.toASCII(this.hostname));
          var _ = this.port ? ":" + this.port : "",
            D = this.hostname || "";
          (this.host = D + _),
            (this.href += this.host),
            P &&
              ((this.hostname = this.hostname.substr(
                1,
                this.hostname.length - 2
              )),
              "/" !== d[0] && (d = "/" + d));
        }
        if (!y[w])
          for (C = 0, T = l.length; C < T; C++) {
            var F = l[C];
            if (-1 !== d.indexOf(F)) {
              var W = encodeURIComponent(F);
              W === F && (W = escape(F)), (d = d.split(F).join(W));
            }
          }
        var Q = d.indexOf("#");
        -1 !== Q && ((this.hash = d.substr(Q)), (d = d.slice(0, Q)));
        var $ = d.indexOf("?");
        if (
          (-1 !== $
            ? ((this.search = d.substr($)),
              (this.query = d.substr($ + 1)),
              e && (this.query = b.parse(this.query)),
              (d = d.slice(0, $)))
            : e && ((this.search = ""), (this.query = {})),
          d && (this.pathname = d),
          v[w] && this.hostname && !this.pathname && (this.pathname = "/"),
          this.pathname || this.search)
        ) {
          _ = this.pathname || "";
          var H = this.search || "";
          this.path = _ + H;
        }
        return (this.href = this.format()), this;
      }),
        (i.prototype.format = function() {
          var t = this.auth || "";
          t &&
            ((t = (t = encodeURIComponent(t)).replace(/%3A/i, ":")),
            (t += "@"));
          var e = this.protocol || "",
            r = this.pathname || "",
            n = this.hash || "",
            i = !1,
            s = "";
          this.host
            ? (i = t + this.host)
            : this.hostname &&
              ((i =
                t +
                (-1 === this.hostname.indexOf(":")
                  ? this.hostname
                  : "[" + this.hostname + "]")),
              this.port && (i += ":" + this.port)),
            this.query &&
              o.isObject(this.query) &&
              Object.keys(this.query).length &&
              (s = b.stringify(this.query));
          var a = this.search || (s && "?" + s) || "";
          return (
            e && ":" !== e.substr(-1) && (e += ":"),
            this.slashes || ((!e || v[e]) && !1 !== i)
              ? ((i = "//" + (i || "")),
                r && "/" !== r.charAt(0) && (r = "/" + r))
              : i || (i = ""),
            n && "#" !== n.charAt(0) && (n = "#" + n),
            a && "?" !== a.charAt(0) && (a = "?" + a),
            e +
              i +
              (r = r.replace(/[?#]/g, function(t) {
                return encodeURIComponent(t);
              })) +
              (a = a.replace("#", "%23")) +
              n
          );
        }),
        (i.prototype.resolve = function(t) {
          return this.resolveObject(d(t, !1, !0)).format();
        }),
        (i.prototype.resolveObject = function(t) {
          if (o.isString(t)) {
            var e = new i();
            e.parse(t, !1, !0), (t = e);
          }
          for (
            var r = new i(), n = Object.keys(this), s = 0;
            s < n.length;
            s++
          ) {
            var a = n[s];
            r[a] = this[a];
          }
          if (((r.hash = t.hash), "" === t.href))
            return (r.href = r.format()), r;
          if (t.slashes && !t.protocol) {
            for (var h = Object.keys(t), u = 0; u < h.length; u++) {
              var l = h[u];
              "protocol" !== l && (r[l] = t[l]);
            }
            return (
              v[r.protocol] &&
                r.hostname &&
                !r.pathname &&
                (r.path = r.pathname = "/"),
              (r.href = r.format()),
              r
            );
          }
          if (t.protocol && t.protocol !== r.protocol) {
            if (!v[t.protocol]) {
              for (var f = Object.keys(t), c = 0; c < f.length; c++) {
                var p = f[c];
                r[p] = t[p];
              }
              return (r.href = r.format()), r;
            }
            if (((r.protocol = t.protocol), t.host || m[t.protocol]))
              r.pathname = t.pathname;
            else {
              for (
                var g = (t.pathname || "").split("/");
                g.length && !(t.host = g.shift());

              );
              t.host || (t.host = ""),
                t.hostname || (t.hostname = ""),
                "" !== g[0] && g.unshift(""),
                g.length < 2 && g.unshift(""),
                (r.pathname = g.join("/"));
            }
            if (
              ((r.search = t.search),
              (r.query = t.query),
              (r.host = t.host || ""),
              (r.auth = t.auth),
              (r.hostname = t.hostname || t.host),
              (r.port = t.port),
              r.pathname || r.search)
            ) {
              var y = r.pathname || "",
                b = r.search || "";
              r.path = y + b;
            }
            return (
              (r.slashes = r.slashes || t.slashes), (r.href = r.format()), r
            );
          }
          var d = r.pathname && "/" === r.pathname.charAt(0),
            x = t.host || (t.pathname && "/" === t.pathname.charAt(0)),
            j = x || d || (r.host && t.pathname),
            w = j,
            O = (r.pathname && r.pathname.split("/")) || [],
            A =
              ((g = (t.pathname && t.pathname.split("/")) || []),
              r.protocol && !v[r.protocol]);
          if (
            (A &&
              ((r.hostname = ""),
              (r.port = null),
              r.host && ("" === O[0] ? (O[0] = r.host) : O.unshift(r.host)),
              (r.host = ""),
              t.protocol &&
                ((t.hostname = null),
                (t.port = null),
                t.host && ("" === g[0] ? (g[0] = t.host) : g.unshift(t.host)),
                (t.host = null)),
              (j = j && ("" === g[0] || "" === O[0]))),
            x)
          )
            (r.host = t.host || "" === t.host ? t.host : r.host),
              (r.hostname =
                t.hostname || "" === t.hostname ? t.hostname : r.hostname),
              (r.search = t.search),
              (r.query = t.query),
              (O = g);
          else if (g.length)
            O || (O = []),
              O.pop(),
              (O = O.concat(g)),
              (r.search = t.search),
              (r.query = t.query);
          else if (!o.isNullOrUndefined(t.search)) {
            if (A)
              (r.hostname = r.host = O.shift()),
                (P =
                  !!(r.host && r.host.indexOf("@") > 0) && r.host.split("@")) &&
                  ((r.auth = P.shift()), (r.host = r.hostname = P.shift()));
            return (
              (r.search = t.search),
              (r.query = t.query),
              (o.isNull(r.pathname) && o.isNull(r.search)) ||
                (r.path =
                  (r.pathname ? r.pathname : "") + (r.search ? r.search : "")),
              (r.href = r.format()),
              r
            );
          }
          if (!O.length)
            return (
              (r.pathname = null),
              r.search ? (r.path = "/" + r.search) : (r.path = null),
              (r.href = r.format()),
              r
            );
          for (
            var k = O.slice(-1)[0],
              E =
                ((r.host || t.host || O.length > 1) &&
                  ("." === k || ".." === k)) ||
                "" === k,
              C = 0,
              I = O.length;
            I >= 0;
            I--
          )
            "." === (k = O[I])
              ? O.splice(I, 1)
              : ".." === k
              ? (O.splice(I, 1), C++)
              : C && (O.splice(I, 1), C--);
          if (!j && !w) for (; C--; C) O.unshift("..");
          !j ||
            "" === O[0] ||
            (O[0] && "/" === O[0].charAt(0)) ||
            O.unshift(""),
            E && "/" !== O.join("/").substr(-1) && O.push("");
          var P,
            S = "" === O[0] || (O[0] && "/" === O[0].charAt(0));
          A &&
            ((r.hostname = r.host = S ? "" : O.length ? O.shift() : ""),
            (P = !!(r.host && r.host.indexOf("@") > 0) && r.host.split("@")) &&
              ((r.auth = P.shift()), (r.host = r.hostname = P.shift())));
          return (
            (j = j || (r.host && O.length)) && !S && O.unshift(""),
            O.length
              ? (r.pathname = O.join("/"))
              : ((r.pathname = null), (r.path = null)),
            (o.isNull(r.pathname) && o.isNull(r.search)) ||
              (r.path =
                (r.pathname ? r.pathname : "") + (r.search ? r.search : "")),
            (r.auth = t.auth || r.auth),
            (r.slashes = r.slashes || t.slashes),
            (r.href = r.format()),
            r
          );
        }),
        (i.prototype.parseHost = function() {
          var t = this.host,
            e = a.exec(t);
          e &&
            (":" !== (e = e[0]) && (this.port = e.substr(1)),
            (t = t.substr(0, t.length - e.length))),
            t && (this.hostname = t);
        });
    },
    function(t, e, r) {
      "use strict";
      const n = "undefined" == typeof URL ? r(9).URL : URL;
      function o(t, e) {
        return e.some(e => (e instanceof RegExp ? e.test(t) : e === t));
      }
      t.exports = (t, e) => {
        e = Object.assign(
          {
            normalizeProtocol: !0,
            normalizeHttps: !1,
            stripFragment: !0,
            stripWWW: !0,
            removeQueryParameters: [/^utm_\w+/i],
            removeTrailingSlash: !0,
            removeDirectoryIndex: !1,
            sortQueryParameters: !0
          },
          e
        );
        const r = (t = t.trim()).startsWith("//");
        (!r && /^\.*\//.test(t)) ||
          (t = t.replace(/^(?!(?:\w+:)?\/\/)|^\/\//, "http://"));
        const i = new n(t);
        if (
          (e.normalizeHttps &&
            "https:" === i.protocol &&
            (i.protocol = "http:"),
          e.stripFragment && (i.hash = ""),
          i.pathname && (i.pathname = i.pathname.replace(/\/{2,}/g, "/")),
          i.pathname && (i.pathname = decodeURI(i.pathname)),
          !0 === e.removeDirectoryIndex &&
            (e.removeDirectoryIndex = [/^index\.[a-z]+$/]),
          Array.isArray(e.removeDirectoryIndex) &&
            e.removeDirectoryIndex.length > 0)
        ) {
          let t = i.pathname.split("/");
          o(t[t.length - 1], e.removeDirectoryIndex) &&
            ((t = t.slice(0, t.length - 1)),
            (i.pathname = t.slice(1).join("/") + "/"));
        }
        if (
          (i.hostname &&
            ((i.hostname = i.hostname.replace(/\.$/, "")),
            e.stripWWW && (i.hostname = i.hostname.replace(/^www\./, ""))),
          Array.isArray(e.removeQueryParameters))
        )
          for (const t of [...i.searchParams.keys()])
            o(t, e.removeQueryParameters) && i.searchParams.delete(t);
        return (
          e.sortQueryParameters && i.searchParams.sort(),
          (t = i.toString()),
          (e.removeTrailingSlash || "/" === i.pathname) &&
            (t = t.replace(/\/$/, "")),
          r && !e.normalizeProtocol && (t = t.replace(/^http:\/\//, "//")),
          t
        );
      };
    },
    function(t, e, r) {
      var n = r(1),
        o = r(0),
        i = {
          attributes: {
            compose: function(t, e, r) {
              "object" != typeof t && (t = {}),
                "object" != typeof e && (e = {});
              var n = o(!0, {}, e);
              for (var i in (r ||
                (n = Object.keys(n).reduce(function(t, e) {
                  return null != n[e] && (t[e] = n[e]), t;
                }, {})),
              t))
                void 0 !== t[i] && void 0 === e[i] && (n[i] = t[i]);
              return Object.keys(n).length > 0 ? n : void 0;
            },
            diff: function(t, e) {
              "object" != typeof t && (t = {}),
                "object" != typeof e && (e = {});
              var r = Object.keys(t)
                .concat(Object.keys(e))
                .reduce(function(r, o) {
                  return (
                    n(t[o], e[o]) || (r[o] = void 0 === e[o] ? null : e[o]), r
                  );
                }, {});
              return Object.keys(r).length > 0 ? r : void 0;
            },
            transform: function(t, e, r) {
              if ("object" != typeof t) return e;
              if ("object" == typeof e) {
                if (!r) return e;
                var n = Object.keys(e).reduce(function(r, n) {
                  return void 0 === t[n] && (r[n] = e[n]), r;
                }, {});
                return Object.keys(n).length > 0 ? n : void 0;
              }
            }
          },
          iterator: function(t) {
            return new s(t);
          },
          length: function(t) {
            return "number" == typeof t.delete
              ? t.delete
              : "number" == typeof t.retain
              ? t.retain
              : "string" == typeof t.insert
              ? t.insert.length
              : 1;
          }
        };
      function s(t) {
        (this.ops = t), (this.index = 0), (this.offset = 0);
      }
      (s.prototype.hasNext = function() {
        return this.peekLength() < 1 / 0;
      }),
        (s.prototype.next = function(t) {
          t || (t = 1 / 0);
          var e = this.ops[this.index];
          if (e) {
            var r = this.offset,
              n = i.length(e);
            if (
              (t >= n - r
                ? ((t = n - r), (this.index += 1), (this.offset = 0))
                : (this.offset += t),
              "number" == typeof e.delete)
            )
              return { delete: t };
            var o = {};
            return (
              e.attributes && (o.attributes = e.attributes),
              "number" == typeof e.retain
                ? (o.retain = t)
                : "string" == typeof e.insert
                ? (o.insert = e.insert.substr(r, t))
                : (o.insert = e.insert),
              o
            );
          }
          return { retain: 1 / 0 };
        }),
        (s.prototype.peek = function() {
          return this.ops[this.index];
        }),
        (s.prototype.peekLength = function() {
          return this.ops[this.index]
            ? i.length(this.ops[this.index]) - this.offset
            : 1 / 0;
        }),
        (s.prototype.peekType = function() {
          return this.ops[this.index]
            ? "number" == typeof this.ops[this.index].delete
              ? "delete"
              : "number" == typeof this.ops[this.index].retain
              ? "retain"
              : "insert"
            : "retain";
        }),
        (t.exports = i);
    },
    function(t, e) {
      var r =
        "[object Arguments]" ==
        (function() {
          return Object.prototype.toString.call(arguments);
        })();
      function n(t) {
        return "[object Arguments]" == Object.prototype.toString.call(t);
      }
      function o(t) {
        return (
          (t &&
            "object" == typeof t &&
            "number" == typeof t.length &&
            Object.prototype.hasOwnProperty.call(t, "callee") &&
            !Object.prototype.propertyIsEnumerable.call(t, "callee")) ||
          !1
        );
      }
      ((e = t.exports = r ? n : o).supported = n), (e.unsupported = o);
    },
    function(t, e) {
      function r(t) {
        var e = [];
        for (var r in t) e.push(r);
        return e;
      }
      (t.exports = "function" == typeof Object.keys ? Object.keys : r).shim = r;
    },
    function(t, e) {
      var r = -1,
        n = 1,
        o = 0;
      function i(t, e, u) {
        if (t == e) return t ? [[o, t]] : [];
        (u < 0 || t.length < u) && (u = null);
        var f = a(t, e),
          c = t.substring(0, f);
        f = h((t = t.substring(f)), (e = e.substring(f)));
        var p = t.substring(t.length - f),
          g = (function(t, e) {
            var u;
            if (!t) return [[n, e]];
            if (!e) return [[r, t]];
            var l = t.length > e.length ? t : e,
              f = t.length > e.length ? e : t,
              c = l.indexOf(f);
            if (-1 != c)
              return (
                (u = [
                  [n, l.substring(0, c)],
                  [o, f],
                  [n, l.substring(c + f.length)]
                ]),
                t.length > e.length && (u[0][0] = u[2][0] = r),
                u
              );
            if (1 == f.length)
              return [
                [r, t],
                [n, e]
              ];
            var p = (function(t, e) {
              var r = t.length > e.length ? t : e,
                n = t.length > e.length ? e : t;
              if (r.length < 4 || 2 * n.length < r.length) return null;
              function o(t, e, r) {
                for (
                  var n,
                    o,
                    i,
                    s,
                    u = t.substring(r, r + Math.floor(t.length / 4)),
                    l = -1,
                    f = "";
                  -1 != (l = e.indexOf(u, l + 1));

                ) {
                  var c = a(t.substring(r), e.substring(l)),
                    p = h(t.substring(0, r), e.substring(0, l));
                  f.length < p + c &&
                    ((f = e.substring(l - p, l) + e.substring(l, l + c)),
                    (n = t.substring(0, r - p)),
                    (o = t.substring(r + c)),
                    (i = e.substring(0, l - p)),
                    (s = e.substring(l + c)));
                }
                return 2 * f.length >= t.length ? [n, o, i, s, f] : null;
              }
              var i,
                s,
                u,
                l,
                f,
                c = o(r, n, Math.ceil(r.length / 4)),
                p = o(r, n, Math.ceil(r.length / 2));
              if (!c && !p) return null;
              i = p ? (c && c[4].length > p[4].length ? c : p) : c;
              t.length > e.length
                ? ((s = i[0]), (u = i[1]), (l = i[2]), (f = i[3]))
                : ((l = i[0]), (f = i[1]), (s = i[2]), (u = i[3]));
              var g = i[4];
              return [s, u, l, f, g];
            })(t, e);
            if (p) {
              var g = p[0],
                y = p[1],
                m = p[2],
                v = p[3],
                b = p[4],
                d = i(g, m),
                x = i(y, v);
              return d.concat([[o, b]], x);
            }
            return (function(t, e) {
              for (
                var o = t.length,
                  i = e.length,
                  a = Math.ceil((o + i) / 2),
                  h = a,
                  u = 2 * a,
                  l = new Array(u),
                  f = new Array(u),
                  c = 0;
                c < u;
                c++
              )
                (l[c] = -1), (f[c] = -1);
              (l[h + 1] = 0), (f[h + 1] = 0);
              for (
                var p = o - i,
                  g = p % 2 != 0,
                  y = 0,
                  m = 0,
                  v = 0,
                  b = 0,
                  d = 0;
                d < a;
                d++
              ) {
                for (var x = -d + y; x <= d - m; x += 2) {
                  for (
                    var j = h + x,
                      w =
                        (C =
                          x == -d || (x != d && l[j - 1] < l[j + 1])
                            ? l[j + 1]
                            : l[j - 1] + 1) - x;
                    C < o && w < i && t.charAt(C) == e.charAt(w);

                  )
                    C++, w++;
                  if (((l[j] = C), C > o)) m += 2;
                  else if (w > i) y += 2;
                  else if (g) {
                    var O = h + p - x;
                    if (O >= 0 && O < u && -1 != f[O]) {
                      var A = o - f[O];
                      if (C >= A) return s(t, e, C, w);
                    }
                  }
                }
                for (var k = -d + v; k <= d - b; k += 2) {
                  for (
                    var O = h + k,
                      E =
                        (A =
                          k == -d || (k != d && f[O - 1] < f[O + 1])
                            ? f[O + 1]
                            : f[O - 1] + 1) - k;
                    A < o &&
                    E < i &&
                    t.charAt(o - A - 1) == e.charAt(i - E - 1);

                  )
                    A++, E++;
                  if (((f[O] = A), A > o)) b += 2;
                  else if (E > i) v += 2;
                  else if (!g) {
                    var j = h + p - k;
                    if (j >= 0 && j < u && -1 != l[j]) {
                      var C = l[j],
                        w = h + C - j;
                      if (C >= (A = o - A)) return s(t, e, C, w);
                    }
                  }
                }
              }
              return [
                [r, t],
                [n, e]
              ];
            })(t, e);
          })(
            (t = t.substring(0, t.length - f)),
            (e = e.substring(0, e.length - f))
          );
        return (
          c && g.unshift([o, c]),
          p && g.push([o, p]),
          (function t(e) {
            e.push([o, ""]);
            var i = 0;
            var s = 0;
            var u = 0;
            var l = "";
            var f = "";
            var c;
            for (; i < e.length; )
              switch (e[i][0]) {
                case n:
                  u++, (f += e[i][1]), i++;
                  break;
                case r:
                  s++, (l += e[i][1]), i++;
                  break;
                case o:
                  s + u > 1
                    ? (0 !== s &&
                        0 !== u &&
                        (0 !== (c = a(f, l)) &&
                          (i - s - u > 0 && e[i - s - u - 1][0] == o
                            ? (e[i - s - u - 1][1] += f.substring(0, c))
                            : (e.splice(0, 0, [o, f.substring(0, c)]), i++),
                          (f = f.substring(c)),
                          (l = l.substring(c))),
                        0 !== (c = h(f, l)) &&
                          ((e[i][1] = f.substring(f.length - c) + e[i][1]),
                          (f = f.substring(0, f.length - c)),
                          (l = l.substring(0, l.length - c)))),
                      0 === s
                        ? e.splice(i - u, s + u, [n, f])
                        : 0 === u
                        ? e.splice(i - s, s + u, [r, l])
                        : e.splice(i - s - u, s + u, [r, l], [n, f]),
                      (i = i - s - u + (s ? 1 : 0) + (u ? 1 : 0) + 1))
                    : 0 !== i && e[i - 1][0] == o
                    ? ((e[i - 1][1] += e[i][1]), e.splice(i, 1))
                    : i++,
                    (u = 0),
                    (s = 0),
                    (l = ""),
                    (f = "");
              }
            "" === e[e.length - 1][1] && e.pop();
            var p = !1;
            i = 1;
            for (; i < e.length - 1; )
              e[i - 1][0] == o &&
                e[i + 1][0] == o &&
                (e[i][1].substring(e[i][1].length - e[i - 1][1].length) ==
                e[i - 1][1]
                  ? ((e[i][1] =
                      e[i - 1][1] +
                      e[i][1].substring(
                        0,
                        e[i][1].length - e[i - 1][1].length
                      )),
                    (e[i + 1][1] = e[i - 1][1] + e[i + 1][1]),
                    e.splice(i - 1, 1),
                    (p = !0))
                  : e[i][1].substring(0, e[i + 1][1].length) == e[i + 1][1] &&
                    ((e[i - 1][1] += e[i + 1][1]),
                    (e[i][1] =
                      e[i][1].substring(e[i + 1][1].length) + e[i + 1][1]),
                    e.splice(i + 1, 1),
                    (p = !0))),
                i++;
            p && t(e);
          })(g),
          null != u &&
            (g = (function(t, e) {
              var n = (function(t, e) {
                  if (0 === e) return [o, t];
                  for (var n = 0, i = 0; i < t.length; i++) {
                    var s = t[i];
                    if (s[0] === r || s[0] === o) {
                      var a = n + s[1].length;
                      if (e === a) return [i + 1, t];
                      if (e < a) {
                        t = t.slice();
                        var h = e - n,
                          u = [s[0], s[1].slice(0, h)],
                          l = [s[0], s[1].slice(h)];
                        return t.splice(i, 1, u, l), [i + 1, t];
                      }
                      n = a;
                    }
                  }
                  throw new Error("cursor_pos is out of bounds!");
                })(t, e),
                i = n[1],
                s = n[0],
                a = i[s],
                h = i[s + 1];
              if (null == a) return t;
              if (a[0] !== o) return t;
              if (null != h && a[1] + h[1] === h[1] + a[1])
                return i.splice(s, 2, h, a), l(i, s, 2);
              if (null != h && 0 === h[1].indexOf(a[1])) {
                i.splice(s, 2, [h[0], a[1]], [0, a[1]]);
                var u = h[1].slice(a[1].length);
                return (
                  u.length > 0 && i.splice(s + 2, 0, [h[0], u]), l(i, s, 3)
                );
              }
              return t;
            })(g, u)),
          (g = (function(t) {
            for (
              var e = !1,
                i = function(t) {
                  return t.charCodeAt(0) >= 56320 && t.charCodeAt(0) <= 57343;
                },
                s = function(t) {
                  return (
                    t.charCodeAt(t.length - 1) >= 55296 &&
                    t.charCodeAt(t.length - 1) <= 56319
                  );
                },
                a = 2;
              a < t.length;
              a += 1
            )
              t[a - 2][0] === o &&
                s(t[a - 2][1]) &&
                t[a - 1][0] === r &&
                i(t[a - 1][1]) &&
                t[a][0] === n &&
                i(t[a][1]) &&
                ((e = !0),
                (t[a - 1][1] = t[a - 2][1].slice(-1) + t[a - 1][1]),
                (t[a][1] = t[a - 2][1].slice(-1) + t[a][1]),
                (t[a - 2][1] = t[a - 2][1].slice(0, -1)));
            if (!e) return t;
            for (var h = [], a = 0; a < t.length; a += 1)
              t[a][1].length > 0 && h.push(t[a]);
            return h;
          })(g))
        );
      }
      function s(t, e, r, n) {
        var o = t.substring(0, r),
          s = e.substring(0, n),
          a = t.substring(r),
          h = e.substring(n),
          u = i(o, s),
          l = i(a, h);
        return u.concat(l);
      }
      function a(t, e) {
        if (!t || !e || t.charAt(0) != e.charAt(0)) return 0;
        for (var r = 0, n = Math.min(t.length, e.length), o = n, i = 0; r < o; )
          t.substring(i, o) == e.substring(i, o) ? (i = r = o) : (n = o),
            (o = Math.floor((n - r) / 2 + r));
        return o;
      }
      function h(t, e) {
        if (!t || !e || t.charAt(t.length - 1) != e.charAt(e.length - 1))
          return 0;
        for (var r = 0, n = Math.min(t.length, e.length), o = n, i = 0; r < o; )
          t.substring(t.length - o, t.length - i) ==
          e.substring(e.length - o, e.length - i)
            ? (i = r = o)
            : (n = o),
            (o = Math.floor((n - r) / 2 + r));
        return o;
      }
      var u = i;
      function l(t, e, r) {
        for (var n = e + r - 1; n >= 0 && n >= e - 1; n--)
          if (n + 1 < t.length) {
            var o = t[n],
              i = t[n + 1];
            o[0] === i[1] && t.splice(n, 2, [o[0], o[1] + i[1]]);
          }
        return t;
      }
      (u.INSERT = n), (u.DELETE = r), (u.EQUAL = o), (t.exports = u);
    },
    function(t, e, r) {
      var n = r(14),
        o = r(1),
        i = r(0),
        s = r(11),
        a = String.fromCharCode(0),
        h = function(t) {
          Array.isArray(t)
            ? (this.ops = t)
            : null != t && Array.isArray(t.ops)
            ? (this.ops = t.ops)
            : (this.ops = []);
        };
      (h.prototype.insert = function(t, e) {
        var r = {};
        return 0 === t.length
          ? this
          : ((r.insert = t),
            null != e &&
              "object" == typeof e &&
              Object.keys(e).length > 0 &&
              (r.attributes = e),
            this.push(r));
      }),
        (h.prototype.delete = function(t) {
          return t <= 0 ? this : this.push({ delete: t });
        }),
        (h.prototype.retain = function(t, e) {
          if (t <= 0) return this;
          var r = { retain: t };
          return (
            null != e &&
              "object" == typeof e &&
              Object.keys(e).length > 0 &&
              (r.attributes = e),
            this.push(r)
          );
        }),
        (h.prototype.push = function(t) {
          var e = this.ops.length,
            r = this.ops[e - 1];
          if (((t = i(!0, {}, t)), "object" == typeof r)) {
            if ("number" == typeof t.delete && "number" == typeof r.delete)
              return (this.ops[e - 1] = { delete: r.delete + t.delete }), this;
            if (
              "number" == typeof r.delete &&
              null != t.insert &&
              ((e -= 1), "object" != typeof (r = this.ops[e - 1]))
            )
              return this.ops.unshift(t), this;
            if (o(t.attributes, r.attributes)) {
              if ("string" == typeof t.insert && "string" == typeof r.insert)
                return (
                  (this.ops[e - 1] = { insert: r.insert + t.insert }),
                  "object" == typeof t.attributes &&
                    (this.ops[e - 1].attributes = t.attributes),
                  this
                );
              if ("number" == typeof t.retain && "number" == typeof r.retain)
                return (
                  (this.ops[e - 1] = { retain: r.retain + t.retain }),
                  "object" == typeof t.attributes &&
                    (this.ops[e - 1].attributes = t.attributes),
                  this
                );
            }
          }
          return (
            e === this.ops.length ? this.ops.push(t) : this.ops.splice(e, 0, t),
            this
          );
        }),
        (h.prototype.chop = function() {
          var t = this.ops[this.ops.length - 1];
          return t && t.retain && !t.attributes && this.ops.pop(), this;
        }),
        (h.prototype.filter = function(t) {
          return this.ops.filter(t);
        }),
        (h.prototype.forEach = function(t) {
          this.ops.forEach(t);
        }),
        (h.prototype.map = function(t) {
          return this.ops.map(t);
        }),
        (h.prototype.partition = function(t) {
          var e = [],
            r = [];
          return (
            this.forEach(function(n) {
              (t(n) ? e : r).push(n);
            }),
            [e, r]
          );
        }),
        (h.prototype.reduce = function(t, e) {
          return this.ops.reduce(t, e);
        }),
        (h.prototype.changeLength = function() {
          return this.reduce(function(t, e) {
            return e.insert ? t + s.length(e) : e.delete ? t - e.delete : t;
          }, 0);
        }),
        (h.prototype.length = function() {
          return this.reduce(function(t, e) {
            return t + s.length(e);
          }, 0);
        }),
        (h.prototype.slice = function(t, e) {
          (t = t || 0), "number" != typeof e && (e = 1 / 0);
          for (
            var r = [], n = s.iterator(this.ops), o = 0;
            o < e && n.hasNext();

          ) {
            var i;
            o < t ? (i = n.next(t - o)) : ((i = n.next(e - o)), r.push(i)),
              (o += s.length(i));
          }
          return new h(r);
        }),
        (h.prototype.compose = function(t) {
          for (
            var e = s.iterator(this.ops), r = s.iterator(t.ops), n = new h();
            e.hasNext() || r.hasNext();

          )
            if ("insert" === r.peekType()) n.push(r.next());
            else if ("delete" === e.peekType()) n.push(e.next());
            else {
              var o = Math.min(e.peekLength(), r.peekLength()),
                i = e.next(o),
                a = r.next(o);
              if ("number" == typeof a.retain) {
                var u = {};
                "number" == typeof i.retain
                  ? (u.retain = o)
                  : (u.insert = i.insert);
                var l = s.attributes.compose(
                  i.attributes,
                  a.attributes,
                  "number" == typeof i.retain
                );
                l && (u.attributes = l), n.push(u);
              } else
                "number" == typeof a.delete &&
                  "number" == typeof i.retain &&
                  n.push(a);
            }
          return n.chop();
        }),
        (h.prototype.concat = function(t) {
          var e = new h(this.ops.slice());
          return (
            t.ops.length > 0 &&
              (e.push(t.ops[0]), (e.ops = e.ops.concat(t.ops.slice(1)))),
            e
          );
        }),
        (h.prototype.diff = function(t, e) {
          if (this.ops === t.ops) return new h();
          var r = [this, t].map(function(e) {
              return e
                .map(function(r) {
                  if (null != r.insert)
                    return "string" == typeof r.insert ? r.insert : a;
                  throw new Error(
                    "diff() called " +
                      (e === t ? "on" : "with") +
                      " non-document"
                  );
                })
                .join("");
            }),
            i = new h(),
            u = n(r[0], r[1], e),
            l = s.iterator(this.ops),
            f = s.iterator(t.ops);
          return (
            u.forEach(function(t) {
              for (var e = t[1].length; e > 0; ) {
                var r = 0;
                switch (t[0]) {
                  case n.INSERT:
                    (r = Math.min(f.peekLength(), e)), i.push(f.next(r));
                    break;
                  case n.DELETE:
                    (r = Math.min(e, l.peekLength())), l.next(r), i.delete(r);
                    break;
                  case n.EQUAL:
                    r = Math.min(l.peekLength(), f.peekLength(), e);
                    var a = l.next(r),
                      h = f.next(r);
                    o(a.insert, h.insert)
                      ? i.retain(
                          r,
                          s.attributes.diff(a.attributes, h.attributes)
                        )
                      : i.push(h).delete(r);
                }
                e -= r;
              }
            }),
            i.chop()
          );
        }),
        (h.prototype.eachLine = function(t, e) {
          e = e || "\n";
          for (
            var r = s.iterator(this.ops), n = new h(), o = 0;
            r.hasNext();

          ) {
            if ("insert" !== r.peekType()) return;
            var i = r.peek(),
              a = s.length(i) - r.peekLength(),
              u = "string" == typeof i.insert ? i.insert.indexOf(e, a) - a : -1;
            if (u < 0) n.push(r.next());
            else if (u > 0) n.push(r.next(u));
            else {
              if (!1 === t(n, r.next(1).attributes || {}, o)) return;
              (o += 1), (n = new h());
            }
          }
          n.length() > 0 && t(n, {}, o);
        }),
        (h.prototype.transform = function(t, e) {
          if (((e = !!e), "number" == typeof t))
            return this.transformPosition(t, e);
          for (
            var r = s.iterator(this.ops), n = s.iterator(t.ops), o = new h();
            r.hasNext() || n.hasNext();

          )
            if ("insert" !== r.peekType() || (!e && "insert" === n.peekType()))
              if ("insert" === n.peekType()) o.push(n.next());
              else {
                var i = Math.min(r.peekLength(), n.peekLength()),
                  a = r.next(i),
                  u = n.next(i);
                if (a.delete) continue;
                u.delete
                  ? o.push(u)
                  : o.retain(
                      i,
                      s.attributes.transform(a.attributes, u.attributes, e)
                    );
              }
            else o.retain(s.length(r.next()));
          return o.chop();
        }),
        (h.prototype.transformPosition = function(t, e) {
          e = !!e;
          for (var r = s.iterator(this.ops), n = 0; r.hasNext() && n <= t; ) {
            var o = r.peekLength(),
              i = r.peekType();
            r.next(),
              "delete" !== i
                ? ("insert" === i && (n < t || !e) && (t += o), (n += o))
                : (t -= Math.min(o, t - n));
          }
          return t;
        }),
        (t.exports = h);
    },
    function(t, e, r) {
      "use strict";
      Object.defineProperty(e, "__esModule", { value: !0 });
      var n = (function() {
          return function(t, e) {
            if (Array.isArray(t)) return t;
            if (Symbol.iterator in Object(t))
              return (function(t, e) {
                var r = [],
                  n = !0,
                  o = !1,
                  i = void 0;
                try {
                  for (
                    var s, a = t[Symbol.iterator]();
                    !(n = (s = a.next()).done) &&
                    (r.push(s.value), !e || r.length !== e);
                    n = !0
                  );
                } catch (t) {
                  (o = !0), (i = t);
                } finally {
                  try {
                    !n && a.return && a.return();
                  } finally {
                    if (o) throw i;
                  }
                }
                return r;
              })(t, e);
            throw new TypeError(
              "Invalid attempt to destructure non-iterable instance"
            );
          };
        })(),
        o =
          Object.assign ||
          function(t) {
            for (var e = 1; e < arguments.length; e++) {
              var r = arguments[e];
              for (var n in r)
                Object.prototype.hasOwnProperty.call(r, n) && (t[n] = r[n]);
            }
            return t;
          },
        i = (function() {
          function t(t, e) {
            for (var r = 0; r < e.length; r++) {
              var n = e[r];
              (n.enumerable = n.enumerable || !1),
                (n.configurable = !0),
                "value" in n && (n.writable = !0),
                Object.defineProperty(t, n.key, n);
            }
          }
          return function(e, r, n) {
            return r && t(e.prototype, r), n && t(e, n), e;
          };
        })(),
        s = h(r(15)),
        a = h(r(10));
      function h(t) {
        return t && t.__esModule ? t : { default: t };
      }
      var u = {
          globalRegularExpression: /(https?:\/\/|www\.)[\S]+/g,
          urlRegularExpression: /(https?:\/\/[\S]+)|(www.[\S]+)/,
          normalizeRegularExpression: /(https?:\/\/[\S]+)|(www.[\S]+)/,
          normalizeUrlOptions: { stripFragment: !1, stripWWW: !1 }
        },
        l = (function() {
          function t(e, r) {
            !(function(t, e) {
              if (!(t instanceof e))
                throw new TypeError("Cannot call a class as a function");
            })(this, t),
              (this.quill = e),
              (r = r || {}),
              (this.options = o({}, u, r)),
              this.registerTypeListener(),
              this.registerPasteListener();
          }
          return (
            i(t, [
              {
                key: "registerPasteListener",
                value: function() {
                  var t = this;
                  this.quill.clipboard.addMatcher(Node.TEXT_NODE, function(
                    e,
                    r
                  ) {
                    if ("string" == typeof e.data) {
                      var n = e.data.match(t.options.globalRegularExpression);
                      if (n && n.length > 0) {
                        var o = new s.default(),
                          i = e.data;
                        n.forEach(function(e) {
                          var r = i.split(e),
                            n = r.shift();
                          o.insert(n),
                            o.insert(e, { link: t.normalize(e) }),
                            (i = r.join(e));
                        }),
                          o.insert(i),
                          (r.ops = o.ops);
                      }
                      return r;
                    }
                  });
                }
              },
              {
                key: "registerTypeListener",
                value: function() {
                  var t = this;
                  this.quill.on("text-change", function(e) {
                    var r = e.ops;
                    if (!(!r || r.length < 1 || r.length > 2)) {
                      var n = r[r.length - 1];
                      n.insert &&
                        "string" == typeof n.insert &&
                        n.insert.match(/\s/) &&
                        t.checkTextForUrl();
                    }
                  });
                }
              },
              {
                key: "checkTextForUrl",
                value: function() {
                  var t = this.quill.getSelection();
                  if (t) {
                    var e = this.quill.getLeaf(t.index),
                      r = n(e, 1)[0];
                    if (r.text && "a" !== r.parent.domNode.localName) {
                      var o = r.text.match(this.options.urlRegularExpression);
                      if (o) {
                        var i = this.quill.getIndex(r) + o.index;
                        this.textToUrl(i, o[0]);
                      }
                    }
                  }
                }
              },
              {
                key: "textToUrl",
                value: function(t, e) {
                  var r = new s.default()
                    .retain(t)
                    .delete(e.length)
                    .insert(e, { link: this.normalize(e) });
                  this.quill.updateContents(r);
                }
              },
              {
                key: "normalize",
                value: function(t) {
                  return this.options.normalizeRegularExpression.test(t)
                    ? (0, a.default)(t, this.options.normalizeUrlOptions)
                    : t;
                }
              }
            ]),
            t
          );
        })();
      (e.default = l),
        window.Quill && window.Quill.register("modules/magicUrl", l);
    }
  ]);
});
