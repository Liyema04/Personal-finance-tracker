const body = document.querySelector("body"),
        sidebar = body.querySelector(".sidebar"),
        toggle = body.querySelector(".toggle"),
        modeSwitch = body.querySelector(".toggle-switch"),
        modeText = body.querySelector(".mode-text");


        // Sidebar (close) event handler
        toggle.addEventListener("click", () => {
                sidebar.classList.toggle("close");
                body.classList.toggle("sidebar-open"); // add/remove helper class
        });

        // Close sidebar when clicking on the overlay
        document.addEventListener("click", (e) => {
                if (body.classList.contains("sidebar-open")) {
                        const clickedInsideSidebar = sidebar.contains(e.target) || toggle.contains(e.target);
                        if (!clickedInsideSidebar) {
                                sidebar.classList.add("close");
                                body.classList.remove("sidebar-open");
                        }
                }
        });
        
        // Dark-Mode event handler
        modeSwitch.addEventListener("click", () => {
                body.classList.toggle("dark");

                if(body.classList.contains("dark")) {
                        modeText.innerText = "Light Mode"
                }else{
                        modeText.innerText = "Dark Mode"
                }
        });