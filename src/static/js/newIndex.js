const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      desktopToggle = body.querySelector(".sidebar .toggle"), // Desktop toggle
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

// Get ALL mobile toggles (header and footer)
let mobileToggles = [];

// Mobile close button reference
let mobileCloseBtn = null;

// Check if we're on mobile 
function isMobile() {
    return window.innerWidth <= 768;
}

// Function to get current mobile toggle elements
function getMobileToggles() {
    const headerToggle = document.querySelector('.header-top-flex .head-link.toggle');
    const footerToggle = document.querySelector('.float-link.toggle');
    
    mobileToggles = [];
    if (headerToggle) mobileToggles.push(headerToggle);
    if (footerToggle) mobileToggles.push(footerToggle);
    
    return mobileToggles;
}

// Function to optimize layout on mobile
function optimizeMobileLayout() {
    if (!isMobile()) return;
    
    // Add a class to body when on very small screens
    if (window.innerWidth <= 320) {
        document.body.classList.add('very-small-screen');
    } else {
        document.body.classList.remove('very-small-screen');
    }
    
    // Recalculate heights
    setVhProperty();
    setMobileSidebarHeight();
}

function manageScrollAnimations() {
    const cards = document.querySelectorAll('.card');

    if (isMobile()) {
        // Adding mobile scroll animation class
        cards.forEach(card => {
            if (!card.classList.contains('mobile-scroll-blur-subtle')) {
                card.classList.add('mobile-scroll-blur');
            }
        });
    }else{
        // Removing mobile scroll animation if on desktop
        cards.forEach(card => {
            card.classList.remove('mobile-scroll-blur-subtle');
        });
    }
}

// Call this function on resize and initialization
window.addEventListener('resize', optimizeMobileLayout);

// Function to set proper height on mobile 
function setMobileSidebarHeight() {
    if (!isMobile()) return;

    if (sidebar.classList.contains("mobile-open")) {
        // Sets height to full viewport when open
        sidebar.style.height = '100vh';
        sidebar.style.height = 'calc(var(--vh, 1vh) * 100)'; // For mobile browsers

        // Ensure menu bar fills available space
        const menuBar = sidebar.querySelector('.menu-bar');
        if (menuBar) {
            menuBar.style.height = '100%';
        }
    } else {
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
function handleToggle(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    console.log('Toggle triggered, isMobile:', isMobile()); // Debug log
    
    if (isMobile()) {
        // On mobile, toggle the mobile-open class
        const isCurrentlyOpen = sidebar.classList.contains("mobile-open");
        
        if (isCurrentlyOpen) {
            sidebar.classList.remove("mobile-open");
            body.classList.remove("sidebar-open");
        } else {
            sidebar.classList.add("mobile-open");
            body.classList.add("sidebar-open");
        }
        
        updateMobileIcon(!isCurrentlyOpen);
        // Set proper height after toggle
        setTimeout(setMobileSidebarHeight, 10);
        
        console.log('Sidebar mobile-open:', !isCurrentlyOpen); // Debug log
    } else {
        // Desktop behavior - use close class
        sidebar.classList.toggle("close");
    }
}

// Update mobile toggle icon for ALL mobile toggles
function updateMobileIcon(isOpen) {
    getMobileToggles().forEach(toggle => {
        if (!toggle) return;
        
        const icon = toggle.querySelector('i[data-lucide]');
        if (icon) {
            // Change icon based on sidebar state
            if (isOpen) {
                icon.setAttribute('data-lucide', 'panel-right-open');
            } else {
                icon.setAttribute('data-lucide', 'panel-right-close');
            }
        }
    });
    
    // Re-initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Function to get mobile close button 
function getMobileCloseButton() {
    mobileCloseBtn = document.querySelector('.sidebar .mobile-close-btn');
    return mobileCloseBtn;
}

// Set up toggle event listeners
function setupToggles() {
    // Desktop toggle
    if (desktopToggle) {
        desktopToggle.removeEventListener("click", handleToggle); // Remove existing
        desktopToggle.addEventListener("click", handleToggle);
        console.log('Desktop toggle setup'); // Debug log
    }
    
    // Mobile toggles - get fresh references and set up listeners
    getMobileToggles().forEach((toggle, index) => {
        if (toggle) {
            // Remove existing listeners to prevent duplicates
            toggle.removeEventListener("click", handleToggle);
            toggle.removeEventListener("touchstart", handleToggle);
            
            // Add new listeners
            toggle.addEventListener("click", handleToggle);
            toggle.addEventListener("touchstart", handleToggle, { passive: false });
            
            console.log(`Mobile toggle ${index + 1} setup:`, toggle); // Debug log
        }
    });

    // Mobile close button in sidebar header 
    const closeBtn = getMobileCloseButton();
    if (closeBtn) {
        closeBtn.removeEventListener("click", handleToggle);
        closeBtn.removeEventListener("touchstart", handleToggle);

        closeBtn.addEventListener("click", handleToggle);
        closeBtn.addEventListener("touchstart", handleToggle, { passive: false });

        console.log('Mobile close button setup:', closeBtn);
    }
}

// Close sidebar when clicking on the overlay
document.addEventListener("click", (e) => {
    if (body.classList.contains("sidebar-open")) {
        const clickedInsideSidebar = sidebar.contains(e.target);
        const clickedDesktopToggle = desktopToggle?.contains(e.target);
        const clickedMobileCloseBtn = mobileCloseBtn?.contains(e.target);
        
        // Check if clicked on any mobile toggle
        const clickedMobileToggle = getMobileToggles().some(toggle => 
            toggle?.contains(e.target)
        );
        
        if (!clickedInsideSidebar && !clickedDesktopToggle && !clickedMobileToggle && !clickedMobileCloseBtn) {
            if (isMobile()) {
                sidebar.classList.remove("mobile-open");
                updateMobileIcon(false);
                setMobileSidebarHeight(); // Reset height
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

        manageScrollAnimations(); // scroll animations
        
        // Re-setup toggles after resize
        setTimeout(setupToggles, 100);
    } else {
        // Ensure sidebar is visible on desktop
        sidebar.classList.remove("mobile-open");
        body.classList.remove("sidebar-open");
        sidebar.style.transform = '';
        sidebar.style.height = ''; // Reset height

        manageScrollAnimations(); // remove scroll animations

        // On desktop, ensure sidebar is open by default
        if (sidebar.classList.contains("close")) {
            sidebar.classList.remove("close");
        }
    }
});

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    console.log('DOM loaded, initializing...'); // Debug log
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Set vh property for mobile
    setVhProperty();
    
    // Initialize icon state
    updateMobileIcon(false);
    
    // Set initial sidebar height
    setMobileSidebarHeight();

    // Initializing scroll animations
    manageScrollAnimations();
    
    // On desktop, ensure sidebar is open by default 
    if (!isMobile() && sidebar.classList.contains("close")) {
        sidebar.classList.remove("close");
    }

    // Call optimize layout
    optimizeMobileLayout();
    
    // Set up toggle functionality - delay to ensure DOM is fully ready
    setTimeout(() => {
        setupToggles();
        console.log('Toggle setup complete'); // Debug log
    }, 100);

    console.log("Sidebar initialized with mobile height fix");
});

// Listen for orientation changes on mobile
window.addEventListener('orientationchange', function() {
    if (isMobile()) {
        // Recalculate height after orientation change
        setTimeout(setVhProperty, 100);
        setTimeout(setMobileSidebarHeight, 150);
        setTimeout(optimizeMobileLayout, 200);
        setTimeout(setupToggles, 300); // Re-setup toggles
    }
});

// Additional safety check - re-setup toggles when content changes
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            // Check if footer navigation was added/changed
            const footerAdded = Array.from(mutation.addedNodes).some(node => 
                node.nodeType === 1 && (node.tagName === 'FOOTER' || node.querySelector && node.querySelector('.float-link.toggle'))
            );

            const closeBtnAdded = Array.from(mutation.addedNodes).some(node =>
                node.nodeType === 1 && (node.classList && node.classList.contains('mobile-close-btn'))
            );
            
            if (footerAdded) {
                setTimeout(setupToggles, 50);
                console.log('Footer navigation detected, re-setup toggles'); // Debug log
            }
        }
    });
});

// Start observing
observer.observe(document.body, {
    childList: true,
    subtree: true
});