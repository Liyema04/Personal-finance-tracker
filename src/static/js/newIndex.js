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

// Unified toggle handler
function handleToggle() {
    if (isMobile()) {
        // On mobile, toggle the mobile-open class
        sidebar.classList.toggle("mobile-open");
        body.classList.toggle("sidebar-open");
        updateMobileIcon(sidebar.classList.contains("mobile-open"));
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
        // Reset to default state on mobile
        sidebar.classList.remove("mobile-open");
        body.classList.remove("sidebar-open");
        updateMobileIcon(false);
    } else {
        // Ensure sidebar is visible on desktop
        sidebar.classList.remove("mobile-open");
        body.classList.remove("sidebar-open");
        sidebar.style.transform = '';
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
    
    // Initialize icon state
    updateMobileIcon(false);
    
    console.log("Sidebar initialized");
});