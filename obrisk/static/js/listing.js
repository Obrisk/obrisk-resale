(function () {
    var sidebar = document.getElementById('sidebar');
    var sidebarOverlay = document.getElementsByClassName('sidebar-overlay')[0];
    var container = document.getElementsByClassName('container')[0];
    var sidebarBtnOpen = document.getElementById('sidebarBtnOpen');

    var openSidebar = function () {
      sidebarOverlay.style.left = '0';
      sidebar.style.left = '0';
      sidebarOverlay.style.top = '0';
      sidebar.style.display = 'block';
      $(".classifieds").toggleClass("open-sidebar");
    }

    var closeSidebar = function (e) {
      e.cancelBubble = true;
      sidebarOverlay.style.left = '-100%';
      sidebar.style.left = '-100%';
      $(".classifieds").toggleClass("open-sidebar");

    }

    //sidebarOverlay.addEventListener('click', closeSidebar);
    //sidebarBtnOpen.addEventListener('click', openSidebar);
  })()