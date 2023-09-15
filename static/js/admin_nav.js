
function getCookie(cname) {
      var cookies = ` ${document.cookie}`.split(";");
      var val = "";
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].split("=");
        if (cookie[0] == ` ${cname}`) {
          return cookie[1];
        }
      }
      return "";
   }

const showNavbar = (toggleId, navId, bodyId, navtoggle, navicon, mainD, pageTitle) => {
          const nvtoggle = document.getElementById(navtoggle);
          const toggle = document.getElementById(toggleId),
            main = document.getElementById(mainD),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            nav_icon = document.getElementById(navicon),
            p_title = document.getElementById(pageTitle)


            let nav_expanders = [toggle, nvtoggle];

          // Validate that all variables exist
          if (toggle && nav && bodypd && nvtoggle) {
            if(getCookie("side_expanded")==="true" && window.innerWidth >= 768){
                  nav.classList.add("show");
                  toggle.classList.add("bx-x");
                  nav_icon.classList.add("bx-x");
                  bodypd.classList.add("body-pd");
                  p_title.classList.add("title-pd");
            }


            nav_expanders.forEach(btn=>{
                  btn.addEventListener("click", () => {
                  nav.classList.toggle("show");
                  toggle.classList.toggle("bx-x");
                  nav_icon.classList.toggle("bx-x");
                  bodypd.classList.toggle("body-pd");
                  p_title.classList.toggle("title-pd");

                  if(nav.classList.contains("show") && window.innerWidth >= 768){
                      document.cookie = "side_expanded=true";
                  }
                  else{
                      document.cookie = "side_expanded=false"
                  }
                })
            ;})

            if(main){
             main.addEventListener("click", () => {
                 let win_width = window.innerWidth;
                 if (win_width < 768) {
                     nav.classList.remove("show");
                     toggle.classList.remove("bx-x");
                     nav_icon.classList.remove("bx-x");
                     bodypd.classList.remove("body-pd");
                     p_title.classList.remove("title-pd");
                     document.cookie = "side_expanded=false";
                 }
             })
            }
          }
        };

function color_link(link_id){
    let colored = document.getElementById(link_id);
    colored.classList.add("active")
}
