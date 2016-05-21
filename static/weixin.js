var app = function() {
  var e, t = navigator.userAgent, n = !1, o = !1, i = !1, a = "";
  return (e = t.match(/MicroMessenger\/((\d+)\.(\d+))/i)) ? (n = !0,
  a = e[1]) : (e = t.match(/ QQ[\s\/]([\d\.]*)/i)) ? (o = !0,
  a = e[1]) : (e = t.match(/ Qzone[\s\/]([\d\.]*)/i)) && (i = !0,
  a = e[1]),
  {
      weixin: n,
      mqq: o,
      qzone: i,
      version: a
  }
}();
var JsLoader={
  load:function(sUrl,fCallback){
    var _script = document.createElement("script");
    _script.setAttribute("type","text/javascript");
    _script.setAttribute("src",sUrl);
    document.getElementsByTagName("head")[0].appendChild(_script);

    if(/msie/.test(window.navigator.userAgent.toLowerCase())){
      _script.onreadystatechange=function(){
        if(this.readyState=="loaded"||this.readyState=="complete"){
          fCallback();
        }
      };
    }else if(/gecko/.test(window.navigator.userAgent.toLowerCase())){
      _script.onload=function(){
        fCallback();
      };
    }else{
      fCallback();
    }
  }
};
if(app.weixin){
  JsLoader.load('https://res.wx.qq.com/open/js/jweixin-1.0.0.js',function(){
    console.log(_G);
    wx.onMenuShareTimeline(_G);
    wx.onMenuShareAppMessage(_G);
  });
};
