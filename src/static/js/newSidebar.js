const body = document.querySelector("body"),
        sidebar = body.querySelector(".sidebar"),
        toggle = body.querySelector(".toggle"),
        modeSwitch = body.querySelector(".toggle-switch"),
        modeText = body.querySelector(".mode-text");


        // Sidebar (close) event handler
        toggle.addEventListener("click", () => {
                sidebar.classList.toggle("close");
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