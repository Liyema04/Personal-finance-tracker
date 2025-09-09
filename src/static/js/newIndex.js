const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      desktopToggle = body.querySelector(".sidebar .toggle"), // Desktop toggle
      mobileToggle = document.querySelector('.header-top-flex .head-link.toggle'), // Mobile toggle
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

// Check if we're on mobile 
function isMobile() {
    return window.innerWidth <= 768;
}

// Fuction to set proper height on mobile 
function setMobileSidebarHeight() {
    if (!isMobile()) return;

    if (sidebar.classList.contains("mobile-open")) {
        // Sets height to full viewport when open
        sidebar.style.height = '100vh';
        sidebar.style.height = 'calc(var(--vh, 1vh) * 100)'; // For mobile browsers

        // Ensure men bar fills available space
        const menuBar = sidebar.querySelector('.menu-bar');
        if (menuBar) {
            menuBar.style.height = '100%';
        }

    }else{
        // Reset height when closed
        sidebar.style.height = '';
        const menuBar = sidebar.querySelector('.menu-bar');
        if (menuBar) {
            menuBar.style.height = '';
        }
    }
}

// Function to calculate and set --vh property for mobile height
function setVhProperty() {
    if (!isMobile()) return;

    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

// Unified toggle handler
function handleToggle() {
    if (isMobile()) {
        // On mobile, toggle the mobile-open class
        sidebar.classList.toggle("mobile-open");
        body.classList.toggle("sidebar-open");
        updateMobileIcon(sidebar.classList.contains("mobile-open"));
        // Set proper height after toggle
        setTimeout(setMobileSidebarHeight, 10);
    } else {
        // Desktop behavior - use close class
        sidebar.classList.toggle("close");
    }
}

// Update mobile toggle icon
function updateMobileIcon(isOpen) {
    if (!mobileToggle) return;
    
    const icon = mobileToggle.querySelector('i[data-lucide]');
    if (!icon) return;
    
    // Change icon based on sidebar state
    if (isOpen) {
        icon.setAttribute('data-lucide', 'panel-right-open');
    } else {
        icon.setAttribute('data-lucide', 'panel-right-close');
    }
    
    // Re-initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Set up toggle event listeners
function setupToggles() {
    // Desktop toggle
    if (desktopToggle) {
        desktopToggle.addEventListener("click", handleToggle);
    }
    
    // Mobile toggle
    if (mobileToggle) {
        mobileToggle.addEventListener("click", (e) => {
            e.preventDefault();
            handleToggle();
        });
    }
}

// Close sidebar when clicking on the overlay
document.addEventListener("click", (e) => {
    if (body.classList.contains("sidebar-open")) {
        const clickedInsideSidebar = sidebar.contains(e.target);
        const clickedDesktopToggle = desktopToggle?.contains(e.target);
        const clickedMobileToggle = mobileToggle?.contains(e.target);
        
        if (!clickedInsideSidebar && !clickedDesktopToggle && !clickedMobileToggle) {
            if (isMobile()) {
                sidebar.classList.remove("mobile-open");
                updateMobileIcon(false);
                setMobileSidebarHeight() // Reset height
            } else {
                sidebar.classList.add("close");
            }
            body.classList.remove("sidebar-open");
        }
    }
});

// Dark-Mode event handler
if (modeSwitch) {
    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");
        if (body.classList.contains("dark")) {
            modeText.innerText = "Light Mode";
        } else {
            modeText.innerText = "Dark Mode";
        }
    });
}

// Handling window resize events 
window.addEventListener("resize", () => {
    if (isMobile()) {
        // Update vh property on resize 
        setVhProperty();

        // Reset to default state on mobile
        sidebar.classList.remove("mobile-open");
        body.classList.remove("sidebar-open");
        updateMobileIcon(false);
        setMobileSidebarHeight(); // Reset height
    } else {
        // Ensure sidebar is visible on desktop
        sidebar.classList.remove("mobile-open");
        body.classList.remove("sidebar-open");
        sidebar.style.transform = '';
        sidebar.style.height = ''; // Reset height
    }
});

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Set up toggle functionality
    setupToggles();
    
    // Set vh property for mobile
    setVhProperty();
    
    // Initialize icon state
    updateMobileIcon(false);
    
    // Set initial sidebar height
    setMobileSidebarHeight();
    
    console.log("Sidebar initialized with mobile height fix");
});

// Listen for orientation changes on mobile
window.addEventListener('orientationchange', function() {
    if (isMobile()) {
        // Recalculate height after orientation change
        setTimeout(setVhProperty, 100);
        setTimeout(setMobileSidebarHeight, 150);
    }
});