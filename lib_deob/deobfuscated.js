"use strict";
(self.webpackChunkgame_core = self.webpackChunkgame_core || []).push([[647], {
  1609: function (P, D, S) {
    var j = this && this.__assign || function () {
      j = Object.assign || function (R) {
        var V;
        for (var g = 1, B = arguments.length; g < B; g++) {
          for (var N in V = arguments[g]) {
            if (Object.prototype.hasOwnProperty.call(V, N)) {
              R[N] = V[N];
            }
          }
        }
        return R;
      };
      return j.apply(this, arguments);
    };
    var y = this && this.__awaiter || function (R, V, g, B) {
      return new (g ||= Promise)(function (N, b) {
        function F(Y) {
          try {
            M(B.next(Y));
          } catch (E) {
            b(E);
          }
        }
        function C(Y) {
          try {
            M(B.throw(Y));
          } catch (E) {
            b(E);
          }
        }
        function M(Y) {
          var E;
          if (Y.done) {
            N(Y.value);
          } else {
            (E = Y.value, E instanceof g ? E : new g(function (L) {
              L(E);
            })).then(F, C);
          }
        }
        M((B = B.apply(R, V || [])).next());
      });
    };
    var A = this && this.__generator || function (R, V) {
      var g;
      var B;
      var N;
      var b;
      var F = {
        label: 0,
        sent: function () {
          if (N[0] & 1) {
            throw N[1];
          }
          return N[1];
        },
        trys: [],
        ops: []
      };
      b = {
        next: C(0),
        throw: C(1),
        return: C(2)
      };
      if (typeof Symbol == "function") {
        b[Symbol.iterator] = function () {
          return this;
        };
      }
      return b;
      function C(M) {
        return function (Y) {
          return function (E) {
            if (g) {
              throw new TypeError("Generator is already executing.");
            }
            while (b && (b = 0, E[0] && (F = 0)), F) {
              try {
                g = 1;
                if (B && (N = E[0] & 2 ? B.return : E[0] ? B.throw || ((N = B.return) && N.call(B), 0) : B.next) && !(N = N.call(B, E[1])).done) {
                  return N;
                }
                B = 0;
                if (N) {
                  E = [E[0] & 2, N.value];
                }
                switch (E[0]) {
                  case 0:
                  case 1:
                    N = E;
                    break;
                  case 4:
                    F.label++;
                    return {
                      value: E[1],
                      done: false
                    };
                  case 5:
                    F.label++;
                    B = E[1];
                    E = [0];
                    continue;
                  case 7:
                    E = F.ops.pop();
                    F.trys.pop();
                    continue;
                  default:
                    if (!(N = F.trys, (N = N.length > 0 && N[N.length - 1]) || E[0] !== 6 && E[0] !== 2)) {
                      F = 0;
                      continue;
                    }
                    if (E[0] === 3 && (!N || E[1] > N[0] && E[1] < N[3])) {
                      F.label = E[1];
                      break;
                    }
                    if (E[0] === 6 && F.label < N[1]) {
                      F.label = N[1];
                      N = E;
                      break;
                    }
                    if (N && F.label < N[2]) {
                      F.label = N[2];
                      F.ops.push(E);
                      break;
                    }
                    if (N[2]) {
                      F.ops.pop();
                    }
                    F.trys.pop();
                    continue;
                }
                E = V.call(R, F);
              } catch (L) {
                E = [6, L];
                B = 0;
              } finally {
                g = N = 0;
              }
            }
            if (E[0] & 5) {
              throw E[1];
            }
            return {
              value: E[0] ? E[1] : undefined,
              done: true
            };
          }([M, Y]);
        };
      }
    };
    var z = this && this.__importDefault || function (R) {
      if (R && R.__esModule) {
        return R;
      } else {
        return {
          default: R
        };
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.ECApi = undefined;
    S(8423);
    var I = S(8139);
    var U = z(S(754));
    var x = S(2891);
    var q = S(9354);
    var X = S(2273);
    var w = S(4003);
    var v = S(1047);
    var T = function () {
      function R(V, g) {
        if (V) {
          this.origin = V;
        }
        if (g) {
          this.protocol = g;
        }
        this.headers = {};
      }
      R.prototype.setHeaderData = function (V) {
        this.headers = V;
      };
      R.prototype.setUserIP = function (V) {
        this.userIP = V;
      };
      R.prototype.setOrigin = function (V) {
        this.origin = V;
      };
      R.prototype.setProtocol = function (V) {
        this.protocol = V;
      };
      R.prototype.setMock = function (V) {
        this.mock = V;
      };
      R.prototype.setSecretTransportedHeader = function (V, g) {
        this.secretTransportedHeader ||= {};
        this.secretTransportedHeader[V] = g;
      };
      R.prototype.deleteSecretTransportedHeader = function (V) {
        if (this.secretTransportedHeader && this.secretTransportedHeader[V]) {
          delete this.secretTransportedHeader[V];
        }
      };
      R.prototype.createNewSession = function (V) {
        return y(this, undefined, undefined, function () {
          var B;
          var N;
          var F;
          var C;
          var M;
          var Y;
          var E;
          var L;
          var k;
          var H;
          var G;
          var Z;
          var W;
          var O;
          var J;
          var K;
          return A(this, function (Q) {
            switch (Q.label) {
              case 0:
                B = V.publicKey;
                N = V.userPreferredLang;
                F = V.userPreferredSupportedLang;
                C = V.renderType;
                M = V.apiType;
                Y = V.fallbackType;
                E = Y === undefined ? 0 : Y;
                L = V.isBootstrapMode;
                k = V.simulateRateLimit;
                H = V.originalSessionToken;
                G = {
                  public_key: B,
                  userip: this.userIP,
                  userbrowser: this.headers["user-agent"],
                  lang: N,
                  language: F,
                  api_type: M,
                  render_type: C,
                  original_session_token: H,
                  fallback_type: E
                };
                if (k) {
                  G.simulate_rate_limit = 1;
                }
                Z = `${q.ENDPOINT.SETUP_SESSION}/nojs/${L ? "bootstrapped/" : ""}${B}`;
                if ((0, X.isServer)()) {
                  W = {
                    return_security_info: 1
                  };
                  if (E !== null) {
                    W.nojs_fb_type = E;
                  }
                }
                return [4, this.callECApi(Z, {
                  data: G,
                  secretTransportedHeader: W
                })];
              case 1:
                O = Q.sent();
                J = (O == null ? undefined : O.data) ?? {};
                K = j({}, J);
                if (J == null ? undefined : J.token) {
                  K.token = this.convertTokenToObject(J.token);
                  K.verificationToken = J.token;
                }
                return [2, K];
            }
          });
        });
      };
      R.prototype.createNewGame = function (V) {
        return y(this, undefined, undefined, function () {
          var B;
          var N;
          var F;
          var C;
          var M;
          var Y;
          var E;
          var L;
          var k;
          var H;
          var G;
          var Z;
          var W;
          var O;
          var J;
          var K;
          return A(this, function (Q) {
            switch (Q.label) {
              case 0:
                B = V.sessionToken;
                N = V.region;
                F = V.userPreferredSupportedLang;
                C = V.renderType;
                M = V.disableCookies;
                Y = V.fallbackType;
                E = V.analyticsTier;
                L = V.data;
                k = V.repeatGame;
                H = V.passGet;
                G = V.isAudioGame;
                Z = V.apiBreakerVersion;
                W = V.isCompatibilityMode;
                O = {
                  token: B,
                  sid: N,
                  render_type: C,
                  lang: F,
                  isAudioGame: G ?? this.isAudioGame,
                  nojs_users_ip: this.userIP,
                  analytics_tier: E,
                  is_compatibility_mode: W,
                  data: L,
                  apiBreakerVersion: Z
                };
                if (k) {
                  O.repeat = k;
                }
                if (H) {
                  O.data = {
                    ps: H
                  };
                }
                if ((0, X.isServer)()) {
                  J = {
                    return_security_info: 1
                  };
                  if (Y) {
                    J.nojs_fb_type = Y;
                  }
                }
                return [4, this.callECApi(q.ENDPOINT.GET_GAME, {
                  sessionToken: B,
                  data: O,
                  secretTransportedHeader: J,
                  disableCookies: M
                })];
              case 1:
                if ((K = Q.sent()).data.error) {
                  throw new Error(K.data.error);
                }
                return [2, K.data ?? {}];
            }
          });
        });
      };
      R.prototype.checkAnswer = function (V) {
        return y(this, undefined, undefined, function () {
          var B;
          var N;
          var F;
          var C;
          var M;
          var Y;
          var E;
          var L;
          var k;
          var H;
          var G;
          var Z;
          var W;
          var O;
          var J;
          var K;
          var Q;
          return A(this, function (P0) {
            switch (P0.label) {
              case 0:
                B = V.sessionToken;
                N = V.gameToken;
                F = V.renderType;
                C = V.region;
                M = V.guesses;
                Y = V.tguesses;
                E = V.fallbackType;
                L = V.analyticsTier;
                k = V.bio;
                H = V.disableCookies;
                G = V.isCompatibilityMode;
                Z = V.ecdata;
                W = V.gp;
                O = (0, x.encryptECData)(JSON.stringify(M), B);
                J = {
                  session_token: B,
                  game_token: N,
                  sid: C,
                  guess: O,
                  render_type: F,
                  analytics_tier: L ?? 0,
                  bio: k,
                  is_compatibility_mode: G,
                  ecdata: Z
                };
                if (W) {
                  J.gp = JSON.stringify(W);
                }
                if (Y) {
                  J.tguess = (0, x.encryptECData)(JSON.stringify(Y), B);
                }
                if ((0, X.isServer)()) {
                  K = {};
                  if (E) {
                    K.nojs_fb_type = E;
                  }
                }
                return [4, this.callECApi(q.ENDPOINT.CHECK_ANSWER, {
                  sessionToken: B,
                  data: J,
                  secretTransportedHeader: K,
                  disableCookies: H
                })];
              case 1:
                if ((Q = P0.sent()).data.error) {
                  throw new Error(Q.data.error);
                }
                return [2, Q.data];
            }
          });
        });
      };
      R.prototype.logData = function (V) {
        return y(this, undefined, undefined, function () {
          return A(this, function (g) {
            switch (g.label) {
              case 0:
                return [4, this.callECApi(q.ENDPOINT.ANALYTICS, {
                  sessionToken: V.session_token,
                  disableCookies: V.disableCookies,
                  data: V
                })];
              case 1:
                return [2, g.sent().data];
            }
          });
        });
      };
      R.prototype.getEncryptionKey = function (V) {
        return y(this, undefined, undefined, function () {
          var g;
          var B;
          var N;
          var b;
          var F;
          var C;
          var M;
          var Y;
          return A(this, function (E) {
            switch (E.label) {
              case 0:
                g = V.sessionToken;
                B = V.gameToken;
                N = V.region;
                b = V.fallbackType;
                F = V.disableCookies;
                C = {
                  session_token: g,
                  game_token: B,
                  sid: N
                };
                if ((0, X.isServer)()) {
                  M = {};
                  if (b) {
                    M.nojs_fb_type = b;
                  }
                }
                return [4, this.callECApi(q.ENDPOINT.GET_ENCRYPTION_KEY, {
                  sessionToken: g,
                  data: C,
                  secretTransportedHeader: M,
                  disableCookies: F
                })];
              case 1:
                if ((Y = E.sent()).data.error) {
                  throw new Error(Y.data.error);
                }
                return [2, Y.data];
            }
          });
        });
      };
      R.prototype.getECURL = function () {
        if (!(0, X.isServer)()) {
          return "";
        }
        this.origin;
        var V = process.env.FORCE_PROTOCOL;
        if (V && ["http", "https"].includes(V)) {
          return `${V}://${this.origin}`;
        } else if (this.protocol === "https") {
          return `https://${this.origin}`;
        } else {
          return `http://${this.origin}`;
        }
      };
      R.prototype.callECApi = function (V, g) {
        if (this.mock) {
          return (0, w.mockRequest)(V);
        }
        var B = g.sessionToken;
        var N = g.data;
        var b = g.secretTransportedHeader;
        if (this.secretTransportedHeader) {
          b = j(j({}, this.secretTransportedHeader), b);
        }
        var F = (0, v.getTimestamp)();
        if (!g.disableCookies) {
          document.cookie = `timestamp=${F};path=/;secure;samesite=none`;
        }
        var C = {
          Accept: "*/*",
          "Cache-Control": "no-cache",
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
          "X-Requested-With": "XMLHttpRequest",
          "X-NewRelic-Timestamp": F
        };
        if (b && Object.keys(b).length > 0 && B) {
          C["X-Requested-ID"] = (0, x.encryptECData)(JSON.stringify(b), `REQUESTED${B}ID`);
        }
        if ((0, X.isServer)()) {
          if (C["X-Requested-ID"]) {
            C.immediate_reload = "true";
          }
          C = j(j({}, C), this.headers);
        }
        var M = this.getECURL();
        var Y = `${M}/fc/${V}`;
        var E = {
          url: Y,
          method: "post",
          headers: C,
          body: (0, I.stringify)(N)
        };
        return (0, U.default)(Y, E);
      };
      R.prototype.convertTokenToObject = function (V) {
        return V.split("|").reduce(function (g, B) {
          var N;
          var b = B.split("=");
          if (b.length === 1) {
            var F = b[0];
            g.sessionToken = F;
            return g;
          }
          var C = b[0];
          var M = b[1];
          return j(((N = {})[C] = M, N), g);
        }, {});
      };
      return R;
    }();
    D.ECApi = T;
  },
  9354: function (P, D) {
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.ENDPOINT = undefined;
    (function (S) {
      S.SETUP_SESSION = "gt";
      S.GET_GAME = "gfct/";
      S.CHECK_ANSWER = "ca/";
      S.GET_ENCRYPTION_KEY = "ekey/";
      S.ANALYTICS = "a/";
    })(D.ENDPOINT ||= {});
  },
  754: function (P, D, S) {
    var j = this && this.__awaiter || function (q, X, d, w) {
      return new (d ||= Promise)(function (v, T) {
        function R(B) {
          try {
            g(w.next(B));
          } catch (N) {
            T(N);
          }
        }
        function V(B) {
          try {
            g(w.throw(B));
          } catch (N) {
            T(N);
          }
        }
        function g(B) {
          var N;
          if (B.done) {
            v(B.value);
          } else {
            (N = B.value, N instanceof d ? N : new d(function (b) {
              b(N);
            })).then(R, V);
          }
        }
        g((w = w.apply(q, X || [])).next());
      });
    };
    var y = this && this.__generator || function (q, X) {
      var d;
      var w;
      var v;
      var T;
      var R = {
        label: 0,
        sent: function () {
          if (v[0] & 1) {
            throw v[1];
          }
          return v[1];
        },
        trys: [],
        ops: []
      };
      T = {
        next: V(0),
        throw: V(1),
        return: V(2)
      };
      if (typeof Symbol == "function") {
        T[Symbol.iterator] = function () {
          return this;
        };
      }
      return T;
      function V(g) {
        return function (B) {
          return function (N) {
            if (d) {
              throw new TypeError("Generator is already executing.");
            }
            while (T && (T = 0, N[0] && (R = 0)), R) {
              try {
                d = 1;
                if (w && (v = N[0] & 2 ? w.return : N[0] ? w.throw || ((v = w.return) && v.call(w), 0) : w.next) && !(v = v.call(w, N[1])).done) {
                  return v;
                }
                w = 0;
                if (v) {
                  N = [N[0] & 2, v.value];
                }
                switch (N[0]) {
                  case 0:
                  case 1:
                    v = N;
                    break;
                  case 4:
                    R.label++;
                    return {
                      value: N[1],
                      done: false
                    };
                  case 5:
                    R.label++;
                    w = N[1];
                    N = [0];
                    continue;
                  case 7:
                    N = R.ops.pop();
                    R.trys.pop();
                    continue;
                  default:
                    if (!(v = R.trys, (v = v.length > 0 && v[v.length - 1]) || N[0] !== 6 && N[0] !== 2)) {
                      R = 0;
                      continue;
                    }
                    if (N[0] === 3 && (!v || N[1] > v[0] && N[1] < v[3])) {
                      R.label = N[1];
                      break;
                    }
                    if (N[0] === 6 && R.label < v[1]) {
                      R.label = v[1];
                      v = N;
                      break;
                    }
                    if (v && R.label < v[2]) {
                      R.label = v[2];
                      R.ops.push(N);
                      break;
                    }
                    if (v[2]) {
                      R.ops.pop();
                    }
                    R.trys.pop();
                    continue;
                }
                N = X.call(q, R);
              } catch (b) {
                N = [6, b];
                w = 0;
              } finally {
                d = v = 0;
              }
            }
            if (N[0] & 5) {
              throw N[1];
            }
            return {
              value: N[0] ? N[1] : undefined,
              done: true
            };
          }([g, B]);
        };
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    S(8423);
    var A = S(7969);
    var z = S(383);
    var I = S(2273);
    var U = new z.Logger("[🛸 EC API Error]");
    var x = (0, I.isServer)();
    D.default = function (q, X) {
      return j(undefined, undefined, undefined, function () {
        var d;
        var w;
        var v;
        return y(this, function (T) {
          d = 0;
          v = function () {
            return j(undefined, undefined, undefined, function () {
              var R;
              var V;
              var g;
              var B;
              var N;
              return y(this, function (b) {
                switch (b.label) {
                  case 0:
                    R = function () {
                      return ++d < 3;
                    };
                    b.label = 1;
                  case 1:
                    b.trys.push([1, 7,, 10]);
                    return [4, fetch(q, X)];
                  case 2:
                    g = b.sent();
                    return [4, (0, A.convertFetchResponseToAxios)(g, X.method, X)];
                  case 3:
                    if ((V = b.sent()).data.error) {
                      if (R() && V.data.error === "DENIED ACCESS") {
                        return [4, v()];
                      } else {
                        return [3, 5];
                      }
                    } else {
                      return [3, 6];
                    }
                  case 4:
                    return [2, b.sent()];
                  case 5:
                    (B = new Error(`${V.data.error} - ${V.data.reason}`)).response = V;
                    throw B;
                  case 6:
                    return [3, 10];
                  case 7:
                    N = b.sent();
                    if (!(V = N.response)) {
                      throw N;
                    }
                    if (x && JSON.stringify(V.data) !== w) {
                      U.e(function (F) {
                        return JSON.stringify({
                          request: {
                            url: F.config.url,
                            method: F.config.method,
                            data: F.config.data
                          },
                          response: F.data,
                          responseStatus: F.status,
                          responseStatusText: F.statusText,
                          responseHeaders: F.headers
                        });
                      }(V));
                    }
                    w = JSON.stringify(V.data);
                    if (V.status >= 500 && R()) {
                      return [4, v()];
                    } else {
                      return [3, 9];
                    }
                  case 8:
                    return [2, b.sent()];
                  case 9:
                    return [3, 10];
                  case 10:
                    return [2, V];
                }
              });
            });
          };
          return [2, v()];
        });
      });
    };
  },
  1792: function (P, D, S) {
    var j = this && this.__createBinding || (Object.create ? function (A, z, I, U = I) {
      var x = Object.getOwnPropertyDescriptor(z, I);
      if (!x || !!("get" in x ? !z.__esModule : x.writable || x.configurable)) {
        x = {
          enumerable: true,
          get: function () {
            return z[I];
          }
        };
      }
      Object.defineProperty(A, U, x);
    } : function (A, z, I, U = I) {
      A[U] = z[I];
    });
    var y = this && this.__exportStar || function (A, z) {
      for (var I in A) {
        if (I !== "default" && !Object.prototype.hasOwnProperty.call(z, I)) {
          j(z, A, I);
        }
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    y(S(1609), D);
  },
  4003: function (P, D, S) {
    var j = this && this.__awaiter || function (I, U, x, q) {
      return new (x ||= Promise)(function (X, d) {
        function w(R) {
          try {
            T(q.next(R));
          } catch (V) {
            d(V);
          }
        }
        function v(R) {
          try {
            T(q.throw(R));
          } catch (V) {
            d(V);
          }
        }
        function T(R) {
          var V;
          if (R.done) {
            X(R.value);
          } else {
            (V = R.value, V instanceof x ? V : new x(function (g) {
              g(V);
            })).then(w, v);
          }
        }
        T((q = q.apply(I, U || [])).next());
      });
    };
    var y = this && this.__generator || function (I, U) {
      var x;
      var q;
      var X;
      var d;
      var w = {
        label: 0,
        sent: function () {
          if (X[0] & 1) {
            throw X[1];
          }
          return X[1];
        },
        trys: [],
        ops: []
      };
      d = {
        next: v(0),
        throw: v(1),
        return: v(2)
      };
      if (typeof Symbol == "function") {
        d[Symbol.iterator] = function () {
          return this;
        };
      }
      return d;
      function v(T) {
        return function (R) {
          return function (V) {
            if (x) {
              throw new TypeError("Generator is already executing.");
            }
            while (d && (d = 0, V[0] && (w = 0)), w) {
              try {
                x = 1;
                if (q && (X = V[0] & 2 ? q.return : V[0] ? q.throw || ((X = q.return) && X.call(q), 0) : q.next) && !(X = X.call(q, V[1])).done) {
                  return X;
                }
                q = 0;
                if (X) {
                  V = [V[0] & 2, X.value];
                }
                switch (V[0]) {
                  case 0:
                  case 1:
                    X = V;
                    break;
                  case 4:
                    w.label++;
                    return {
                      value: V[1],
                      done: false
                    };
                  case 5:
                    w.label++;
                    q = V[1];
                    V = [0];
                    continue;
                  case 7:
                    V = w.ops.pop();
                    w.trys.pop();
                    continue;
                  default:
                    if (!(X = w.trys, (X = X.length > 0 && X[X.length - 1]) || V[0] !== 6 && V[0] !== 2)) {
                      w = 0;
                      continue;
                    }
                    if (V[0] === 3 && (!X || V[1] > X[0] && V[1] < X[3])) {
                      w.label = V[1];
                      break;
                    }
                    if (V[0] === 6 && w.label < X[1]) {
                      w.label = X[1];
                      X = V;
                      break;
                    }
                    if (X && w.label < X[2]) {
                      w.label = X[2];
                      w.ops.push(V);
                      break;
                    }
                    if (X[2]) {
                      w.ops.pop();
                    }
                    w.trys.pop();
                    continue;
                }
                V = U.call(I, w);
              } catch (g) {
                V = [6, g];
                q = 0;
              } finally {
                x = X = 0;
              }
            }
            if (V[0] & 5) {
              throw V[1];
            }
            return {
              value: V[0] ? V[1] : undefined,
              done: true
            };
          }([T, R]);
        };
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.mockRequest = undefined;
    var A = S(9354);
    var z = S(4188);
    D.mockRequest = function (I) {
      return j(undefined, undefined, undefined, function () {
        var U;
        var x;
        var q;
        var X;
        var d;
        var w;
        var v;
        return y(this, function (T) {
          U = "ap-southeast-2";
          "animalsound";
          "en";
          q = `${x = "581615298b37991e8.7524233303"}|r=${U}|metabgclr=%23ffffff|guitextcolor=%23000000|metaiconclr=%23757575|meta=3|lang=en|pk=880B2DF4-49A5-48BA-BEDB-62FA6A739D2B|at=40|ag=101|cdn_url=abc|lurl=abc|surl=abc`;
          "657615298c6d55535.6026172003";
          X = "localhost:8082/challengeUrl";
          d = ["http://localhost", "http://localhost"];
          w = {
            "audio_game.title": "Audio Challenge"
          };
          v = function () {
            switch (I) {
              case `${A.ENDPOINT.SETUP_SESSION}/nojs/`:
                return {
                  challenge_url: X,
                  challenge_url_cdn: null,
                  noscript: "",
                  token: q,
                  mbio: true,
                  tbio: true,
                  kbio: true
                };
              case A.ENDPOINT.GET_GAME:
                return {
                  audio_challenge_urls: d,
                  audio_game_rate_limited: false,
                  challengeID: "657615298c6d55535.6026172003",
                  font_size_adjustments: 2,
                  game_data: {
                    game_variant: "animalsound",
                    input_format: z.InputFormat.Integer,
                    gameType: z.GameType.AudioGame,
                    customGUI: {
                      audio_download_disabled: 1,
                      encrypted_mode: 0
                    }
                  },
                  game_sid: U,
                  sid: U,
                  lang: "en",
                  sec: 10,
                  session_token: x,
                  string_table: w,
                  string_table_prefixes: [],
                  style_theme: null,
                  challengeURL: X,
                  earlyVictoryMessage: false
                };
              default:
                return {};
            }
          };
          return [2, new Promise(function (R) {
            var V = Math.floor(Math.random() * 500 + 500);
            setTimeout(function () {
              R({
                data: v()
              });
            }, V);
          })];
        });
      });
    };
  },
  930: function (P, D, S) {
    var j = this && this.__importDefault || function (x) {
      if (x && x.__esModule) {
        return x;
      } else {
        return {
          default: x
        };
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.decryptECData = D.encryptECData = D.decrypt = D.encrypt = undefined;
    var y = S(8112);
    var A = j(S(8885));
    var z = j(S(9488));
    var I = j(S(6725));
    var U = {
      stringify: function (x) {
        var q = {
          ct: x.ciphertext.toString(A.default)
        };
        if (x.iv) {
          q.iv = x.iv.toString();
        }
        if (x.salt) {
          q.s = x.salt.toString();
        }
        return JSON.stringify(q);
      },
      parse: function (x) {
        var q = JSON.parse(x);
        var X = y.lib.CipherParams.create({
          ciphertext: A.default.parse(q.ct)
        });
        if (q.iv) {
          X.iv = z.default.parse(q.iv);
        }
        if (q.s) {
          X.salt = z.default.parse(q.s);
        }
        return X;
      }
    };
    D.encrypt = function (x, q) {
      return I.default.encrypt(x.toString(), q, {
        format: U
      }).toString();
    };
    D.decrypt = function (x, q) {
      var X = x;
      if (x && typeof x == "object") {
        X = JSON.stringify(X);
      }
      var d = I.default.decrypt(X, q, {
        format: U
      }).toString(A.default);
      if (typeof window != "undefined") {
        return window.atob(d);
      } else {
        return Buffer.from(d, "base64").toString();
      }
    };
    D.encryptECData = function (x, q) {
      return (0, D.encrypt)(x, q);
    };
    D.decryptECData = function (x, q) {
      return (0, D.decrypt)(x, q);
    };
  },
  2891: function (P, D, S) {
    var j = this && this.__createBinding || (Object.create ? function (A, z, I, U = I) {
      var x = Object.getOwnPropertyDescriptor(z, I);
      if (!x || !!("get" in x ? !z.__esModule : x.writable || x.configurable)) {
        x = {
          enumerable: true,
          get: function () {
            return z[I];
          }
        };
      }
      Object.defineProperty(A, U, x);
    } : function (A, z, I, U = I) {
      A[U] = z[I];
    });
    var y = this && this.__exportStar || function (A, z) {
      for (var I in A) {
        if (I !== "default" && !Object.prototype.hasOwnProperty.call(z, I)) {
          j(z, A, I);
        }
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    y(S(930), D);
  },
  4188: function (P, D) {
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.RenderType = D.InputFormat = D.PageType = D.GameType = D.CAResponseType = D.CAAudioModeResponseType = undefined;
    (function (S) {
      S.Answered = "correct";
      S.NotAnswered = "incorrect";
    })(D.CAAudioModeResponseType ||= {});
    (function (S) {
      S.Answered = "answered";
      S.NotAnswered = "not answered";
    })(D.CAResponseType ||= {});
    (function (S) {
      S[S.Type101 = 101] = "Type101";
      S[S.AudioGame = 101] = "AudioGame";
      S[S.AudioMode = 2] = "AudioMode";
      S[S.TileGame = 3] = "TileGame";
      S[S.MatchGame = 4] = "MatchGame";
    })(D.GameType ||= {});
    (function (S) {
      S.Verify = "VERIFY";
      S.Game = "GAME";
      S.Checking = "CHECKING";
      S.Loading = "LOADING";
      S.Victory = "VICTORY";
      S.Error = "ERROR";
      S.AttemptLimit = "ATTEMPT_LIMIT";
    })(D.PageType ||= {});
    (function (S) {
      S.Integer = "integer";
    })(D.InputFormat ||= {});
    (function (S) {
      S.NoJS = "noJS";
      S.LiteJS = "liteJS";
      S.Canvas = "canvas";
    })(D.RenderType ||= {});
  },
  2084: function (P, D, S) {
    var j = this && this.__assign || function () {
      j = Object.assign || function (X) {
        var d;
        for (var w = 1, v = arguments.length; w < v; w++) {
          for (var T in d = arguments[w]) {
            if (Object.prototype.hasOwnProperty.call(d, T)) {
              X[T] = d[T];
            }
          }
        }
        return X;
      };
      return j.apply(this, arguments);
    };
    var y = this && this.__createBinding || (Object.create ? function (X, d, w, v = w) {
      var T = Object.getOwnPropertyDescriptor(d, w);
      if (!T || !!("get" in T ? !d.__esModule : T.writable || T.configurable)) {
        T = {
          enumerable: true,
          get: function () {
            return d[w];
          }
        };
      }
      Object.defineProperty(X, v, T);
    } : function (X, d, w, v = w) {
      X[v] = d[w];
    });
    var A = this && this.__setModuleDefault || (Object.create ? function (X, d) {
      Object.defineProperty(X, "default", {
        enumerable: true,
        value: d
      });
    } : function (X, d) {
      X.default = d;
    });
    var z = this && this.__importStar || function (X) {
      if (X && X.__esModule) {
        return X;
      }
      var d = {};
      if (X != null) {
        for (var w in X) {
          if (w !== "default" && Object.prototype.hasOwnProperty.call(X, w)) {
            y(d, X, w);
          }
        }
      }
      A(d, X);
      return d;
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.RTL_LANGUAGES = D.transformStringTablePrefixes = D.useTranslation = D.useI18N = D.I18NProvider = undefined;
    var I = z(S(698));
    var U = I.default.createContext({});
    D.I18NProvider = function (X) {
      var d = X.children;
      var w = X.translations;
      var v = w === undefined ? {} : w;
      var T = X.prefixes;
      var R = X.transformMiddlewares;
      var V = (0, I.useMemo)(function () {
        return q(v, T, R);
      }, [v, T, R]);
      return I.default.createElement(U.Provider, {
        value: V
      }, d);
    };
    D.useI18N = function () {
      return (0, I.useContext)(U);
    };
    D.useTranslation = function () {
      var X = (0, I.useContext)(U);
      return (0, I.useCallback)(function (d, w) {
        var v = X[d];
        if (v === undefined || typeof v != "string") {
          return d;
        } else {
          if (w) {
            v = v.replace(/{{.*?}}/g, function (T) {
              return `${w[T.replace(/[{}\s]/g, "")]}`;
            });
          }
          return v;
        }
      }, [X]);
    };
    function x(X, d) {
      if (d && d.length !== 0) {
        return d.reduce(function (w, v) {
          var T = Object.keys(w).filter(function (R) {
            return R.startsWith(`${v}-`);
          }).reduce(function (R, V) {
            R[V.split("-")[1]] = w[V];
            return R;
          }, {});
          return j(j({}, w), T);
        }, X);
      } else {
        return X;
      }
    }
    D.transformStringTablePrefixes = x;
    function q(X, d, w) {
      var v = X;
      v = x(X, d);
      if (w == null ? undefined : w.length) {
        return v = w.reduce(function (T, R) {
          return R(T);
        }, v);
      } else {
        return v;
      }
    }
    D.RTL_LANGUAGES = ["ar", "shu", "sqr", "ssh", "xaa", "yhd", "yud", "aao", "abh", "abv", "acm", "acq", "acw", "acx", "acy", "adf", "ads", "aeb", "aec", "afb", "ajp", "apc", "apd", "arb", "arq", "ars", "ary", "arz", "auz", "avl", "ayh", "ayl", "ayn", "ayp", "bbz", "pga", "he", "iw", "ps", "pbt", "pbu", "pst", "prp", "prd", "ur", "ydd", "yds", "yih", "ji", "yi", "hbo", "men", "xmn", "fa", "jpr", "peo", "pes", "prs", "dv", "sam"];
  },
  9939: function (P, D, S) {
    var j = this && this.__createBinding || (Object.create ? function (A, z, I, U = I) {
      var x = Object.getOwnPropertyDescriptor(z, I);
      if (!x || !!("get" in x ? !z.__esModule : x.writable || x.configurable)) {
        x = {
          enumerable: true,
          get: function () {
            return z[I];
          }
        };
      }
      Object.defineProperty(A, U, x);
    } : function (A, z, I, U = I) {
      A[U] = z[I];
    });
    var y = this && this.__exportStar || function (A, z) {
      for (var I in A) {
        if (I !== "default" && !Object.prototype.hasOwnProperty.call(z, I)) {
          j(z, A, I);
        }
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    y(S(2084), D);
  },
  4516: function (P, D, S) {
    var j = this && this.__createBinding || (Object.create ? function (A, z, I, U = I) {
      var x = Object.getOwnPropertyDescriptor(z, I);
      if (!x || !!("get" in x ? !z.__esModule : x.writable || x.configurable)) {
        x = {
          enumerable: true,
          get: function () {
            return z[I];
          }
        };
      }
      Object.defineProperty(A, U, x);
    } : function (A, z, I, U = I) {
      A[U] = z[I];
    });
    var y = this && this.__exportStar || function (A, z) {
      for (var I in A) {
        if (I !== "default" && !Object.prototype.hasOwnProperty.call(z, I)) {
          j(z, A, I);
        }
      }
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    y(S(1792), D);
    y(S(4188), D);
  },
  2273: function (P, D) {
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.isServer = undefined;
    D.isServer = function () {
      return typeof window == "undefined";
    };
  },
  7969: function (P, D) {
    var S = this && this.__awaiter || function (A, z, I, U) {
      return new (I ||= Promise)(function (x, q) {
        function X(v) {
          try {
            w(U.next(v));
          } catch (T) {
            q(T);
          }
        }
        function d(v) {
          try {
            w(U.throw(v));
          } catch (T) {
            q(T);
          }
        }
        function w(v) {
          var T;
          if (v.done) {
            x(v.value);
          } else {
            (T = v.value, T instanceof I ? T : new I(function (R) {
              R(T);
            })).then(X, d);
          }
        }
        w((U = U.apply(A, z || [])).next());
      });
    };
    var j = this && this.__generator || function (A, z) {
      var I;
      var U;
      var x;
      var q;
      var X = {
        label: 0,
        sent: function () {
          if (x[0] & 1) {
            throw x[1];
          }
          return x[1];
        },
        trys: [],
        ops: []
      };
      q = {
        next: d(0),
        throw: d(1),
        return: d(2)
      };
      if (typeof Symbol == "function") {
        q[Symbol.iterator] = function () {
          return this;
        };
      }
      return q;
      function d(w) {
        return function (v) {
          return function (T) {
            if (I) {
              throw new TypeError("Generator is already executing.");
            }
            while (q && (q = 0, T[0] && (X = 0)), X) {
              try {
                I = 1;
                if (U && (x = T[0] & 2 ? U.return : T[0] ? U.throw || ((x = U.return) && x.call(U), 0) : U.next) && !(x = x.call(U, T[1])).done) {
                  return x;
                }
                U = 0;
                if (x) {
                  T = [T[0] & 2, x.value];
                }
                switch (T[0]) {
                  case 0:
                  case 1:
                    x = T;
                    break;
                  case 4:
                    X.label++;
                    return {
                      value: T[1],
                      done: false
                    };
                  case 5:
                    X.label++;
                    U = T[1];
                    T = [0];
                    continue;
                  case 7:
                    T = X.ops.pop();
                    X.trys.pop();
                    continue;
                  default:
                    if (!(x = X.trys, (x = x.length > 0 && x[x.length - 1]) || T[0] !== 6 && T[0] !== 2)) {
                      X = 0;
                      continue;
                    }
                    if (T[0] === 3 && (!x || T[1] > x[0] && T[1] < x[3])) {
                      X.label = T[1];
                      break;
                    }
                    if (T[0] === 6 && X.label < x[1]) {
                      X.label = x[1];
                      x = T;
                      break;
                    }
                    if (x && X.label < x[2]) {
                      X.label = x[2];
                      X.ops.push(T);
                      break;
                    }
                    if (x[2]) {
                      X.ops.pop();
                    }
                    X.trys.pop();
                    continue;
                }
                T = z.call(A, X);
              } catch (R) {
                T = [6, R];
                U = 0;
              } finally {
                I = x = 0;
              }
            }
            if (T[0] & 5) {
              throw T[1];
            }
            return {
              value: T[0] ? T[1] : undefined,
              done: true
            };
          }([w, v]);
        };
      }
    };
    var y = this && this.__spreadArray || function (A, z, I) {
      if (I || arguments.length === 2) {
        var U;
        for (var x = 0, q = z.length; x < q; x++) {
          if (!!U || !(x in z)) {
            U ||= Array.prototype.slice.call(z, 0, x);
            U[x] = z[x];
          }
        }
      }
      return A.concat(U || Array.prototype.slice.call(z));
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.convertFetchResponseToAxios = undefined;
    D.convertFetchResponseToAxios = function (A, z, I) {
      return S(undefined, undefined, undefined, function () {
        var U;
        var x;
        return j(this, function (q) {
          switch (q.label) {
            case 0:
              U = [];
              if (A.headers) {
                if (A.headers.forEach) {
                  A.headers.forEach(function (X, d) {
                    U.push([d, X]);
                  });
                } else if (A.headers.hasOwnProperty("entries")) {
                  U = A.headers.entries();
                }
              }
              x = y([], U, true).reduce(function (X, d) {
                var w = d[0];
                var v = d[1];
                X[w] = v;
                return X;
              }, {});
              return [4, A.json()];
            case 1:
              return [2, {
                data: q.sent(),
                status: A.status,
                headers: x,
                config: {
                  url: A.url,
                  method: z,
                  data: I.data
                },
                request: I,
                statusText: A.statusText
              }];
          }
        });
      });
    };
  },
  383: function (P, D) {
    var S = this && this.__spreadArray || function (y, A, z) {
      if (z || arguments.length === 2) {
        var I;
        for (var U = 0, x = A.length; U < x; U++) {
          if (!!I || !(U in A)) {
            I ||= Array.prototype.slice.call(A, 0, U);
            I[U] = A[U];
          }
        }
      }
      return y.concat(I || Array.prototype.slice.call(A));
    };
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.Logger = undefined;
    var j = function () {
      function y(A) {
        this.context = A;
      }
      y.prototype.d = function () {
        var A = [];
        for (var z = 0; z < arguments.length; z++) {
          A[z] = arguments[z];
        }
        console.debug.apply(console, S([this.context], A, false));
      };
      y.prototype.i = function () {
        var A = [];
        for (var z = 0; z < arguments.length; z++) {
          A[z] = arguments[z];
        }
        console.info.apply(console, S([this.context], A, false));
      };
      y.prototype.w = function () {
        var A = [];
        for (var z = 0; z < arguments.length; z++) {
          A[z] = arguments[z];
        }
        console.warn.apply(console, S([this.context], A, false));
      };
      y.prototype.e = function () {
        var A = [];
        for (var z = 0; z < arguments.length; z++) {
          A[z] = arguments[z];
        }
        console.error.apply(console, S([this.context], A, false));
      };
      return y;
    }();
    D.Logger = j;
  },
  1047: function (P, D) {
    Object.defineProperty(D, "__esModule", {
      value: true
    });
    D.getTimestamp = undefined;
    D.getTimestamp = function () {
      var S = Date.now().toString(10).substring(0, 7);
      var j = Date.now().toString(10).substring(7, 13);
      return `${S}00${j}`;
    };
  }
}]);
