(this["webpackJsonpcallosum-webapp"]=this["webpackJsonpcallosum-webapp"]||[]).push([[0],{58:function(e,n,t){},86:function(e,n,t){"use strict";t.r(n);var r=t(0),a=t.n(r),c=t(42),s=t.n(c),o=(t(58),t(52)),i=t(24),u=t(16),l=t(15),f=t.n(l),m=t(53),d=t(21),p=t(43),b=t.n(p),h=t(51),j=new URLSearchParams(window.location.search),v="".concat(j.get("host")||"localhost",":").concat(j.get("port")||5e3),O=Object(h.a)(v);function g(e){return x.apply(this,arguments)}function x(){return(x=Object(d.a)(f.a.mark((function e(n){return f.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:O.emit("msg",n);case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}var y=t(47),w=b.a.get("//".concat(v,"/static/features.csv")).then(function(){var e=Object(d.a)(f.a.mark((function e(n){var t;return f.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,new Promise((function(e,t){Object(y.parse)(n.data,{dynamicTyping:!0,skipEmptyLines:!0,header:!0,complete:e,error:t})}));case 2:return t=e.sent,e.abrupt("return",t.data.filter((function(e){return"default"!==e.name})).map((function(e){return Object(m.a)({},e)})));case 4:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}()).catch((function(e){return console.error(e),[{id:0,name:"Test 123",song:"Test 123",artist:"Test Artist",danceability:0,energy:0,liveness:0,valence:0},{id:0,name:"Test 456",song:"Test 456",artist:"Another Artist",danceability:0,energy:0,liveness:0,valence:0}]}));function F(){return(F=Object(d.a)(f.a.mark((function e(){return f.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",w);case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function k(){return(k=Object(d.a)(f.a.mark((function e(n){return f.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,g({type:"select",name:n});case 2:case"end":return e.stop()}}),e)})))).apply(this,arguments)}var C,S,E,N,T,L,M=t(17),P=a.a.createContext(null),A=t(28),J=t.n(A),B=t(3),I=M.a.div(C||(C=Object(u.a)(["\n    font-family: Lato, sans-serif;\n    font-weight: 400;\n    font-style: normal;\n    border-radius: 2px;\n    background: #FFF2;\n    cursor: pointer;\n    user-select: none;\n\n    //&:hover {\n    //    background: #FFF5;\n    //}\n\n    //&:active {\n    //    color: #555;\n    //    background: #FFF;\n    //}\n\n    &.selected {\n        color: #000;\n        background: #EEE;\n        cursor: default;\n    }\n"])));function z(e){var n=e.music,t=Object(r.useContext)(P),a=t.selected,c=t.setSelected,s=n.name===a;return Object(B.jsxs)(I,{className:J()("d-flex px-3 py-2 my-2 align-items-center",s&&"selected"),onClick:function(){c(n.name),function(e){return k.apply(this,arguments)}(n.name).catch((function(e){console.error(e)}))},children:[Object(B.jsx)("div",{className:"h4 mb-0 flex-grow-1",children:n.artist}),Object(B.jsx)("div",{className:"h6 mb-0 text-end text-muted",children:n.song})]})}function D(e){for(var n=e.length;0!==n;){var t=Math.floor(Math.random()*n);n--;var r=[e[t],e[n]];e[n]=r[0],e[t]=r[1]}return e}var R=Object(M.b)(S||(S=Object(u.a)(["\n    0% {\n        opacity: 0;\n    }\n"]))),U=Object(M.b)(E||(E=Object(u.a)(["\n    0% {\n        opacity: .5;\n        transform: scale(1);\n    }\n    10% {\n        transform: scale(.99);\n    }\n"]))),q=M.a.h1(N||(N=Object(u.a)(["\n    font-family: Futura, Jost, sans-serif;\n    color: #EEE;\n    text-align: center;\n    font-size: 8rem;\n    font-weight: 100;\n    text-transform: uppercase;\n    letter-spacing: 0;\n    user-select: none;\n    cursor: pointer;\n    animation: "," 1s forwards ease-out;\n\n    &.shuffle {\n        animation: "," 1s forwards ease-out;\n    }\n"])),R,U),G=M.a.div(T||(T=Object(u.a)(["\n    margin: auto;\n    max-width: 60rem;\n"]))),H=M.a.div(L||(L=Object(u.a)(["\n    max-height: 20rem;\n    overflow-y: auto;\n"])));function K(){var e=Object(r.useState)(""),n=Object(i.a)(e,2),t=n[0],a=n[1],c=Object(r.useState)([]),s=Object(i.a)(c,2),u=s[0],l=s[1],f=Object(r.useState)(null),m=Object(i.a)(f,2),d=m[0],p=m[1],b=Object(r.useState)(0),h=Object(i.a)(b,2),j=h[0],v=h[1];Object(r.useEffect)((function(){(function(){return F.apply(this,arguments)})().then((function(e){return l(D(Object(o.a)(e)))})).catch((function(e){return console.error(e)}))}),[]);return Object(B.jsx)(P.Provider,{value:{selected:d,setSelected:function(e){p(e),v(Math.random())}},children:Object(B.jsxs)("div",{className:"mx-2 mt-3 mt-md-4",children:[Object(B.jsx)(q,{className:J()("mb-3 text-center",j&&"shuffle"),onClick:function(){return l(D(u)),v(Math.random()),void a("")},children:"Callosum"},j),Object(B.jsxs)(G,{children:[Object(B.jsx)("div",{className:"py-2",children:Object(B.jsx)("input",{type:"text",className:"form-control form-control-lg rounded-0",placeholder:"search for music...",value:t,onFocus:function(e){return e.target.select()},onChange:function(e){return a(e.target.value)}})}),Object(B.jsx)(H,{className:"pe-2",children:u.filter((function(e){if(!t)return!0;var n=t.toLowerCase().trim();return[e.genre,e.artist,e.song].some((function(e){return String(null!==e&&void 0!==e?e:"").toLowerCase().includes(n)}))})).map((function(e){return Object(B.jsx)(z,{music:e},e.name)}))})]})]})})}var Q=function(e){e&&e instanceof Function&&t.e(3).then(t.bind(null,87)).then((function(n){var t=n.getCLS,r=n.getFID,a=n.getFCP,c=n.getLCP,s=n.getTTFB;t(e),r(e),a(e),c(e),s(e)}))};s.a.render(Object(B.jsx)(a.a.StrictMode,{children:Object(B.jsx)(K,{})}),document.getElementById("root")),Q()}},[[86,1,2]]]);
//# sourceMappingURL=main.af8c39e1.chunk.js.map