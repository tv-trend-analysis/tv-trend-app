// Add easy pre-loader to your website
// http://www.owlreporter.com/?p=1534
var cssIdowl = 'myCss';
if (!document.getElementById(cssIdowl))
{
    var head  = document.getElementsByTagName('head')[0];
    var link  = document.createElement('link');
    link.id   = cssIdowl;
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = 'http://cdn.rawgit.com/OwlReporter/Preloader/master/preloader.css';
    link.media = 'all';
    head.appendChild(link);
}
var p = document.createElement("div");
p.innerHTML = "<div style='z-index:100000' id='owlreporter-preloader'><div id='loader'></div><div class='loader-section section-left'></div><div class='loader-section section-right'></div></div>";
document.body.insertBefore(p, document.body.firstChild);
function pageload(){var e=(new Date).getTime(),t=(e-before)/1e3,n=document.getElementById("loadingtime");n.innerHTML="Page load: "+t+" seconds."}window.onload=function(){pageload()},setTimeout(function(){document.body.className+=" loaded"},6000),document.addEventListener?document.addEventListener("DOMContentLoaded",function(){document.removeEventListener("DOMContentLoaded",arguments.callee,!1),domReady()},!1):document.attachEvent&&document.attachEvent("onreadystatechange",function(){"complete"===document.readyState&&(document.detachEvent("onreadystatechange",arguments.callee),domReady())});