// Dark mode script
document.addEventListener('DOMContentLoaded', function () {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    const htmlElement = document.documentElement;

    // On page load or when changing themes, best to add inline in `head` to avoid FOUC
    function initializeTheme() {
        // 1. Check for user preference in localStorage
        const userTheme = localStorage.getItem('color-theme');
        if (userTheme) {
            htmlElement.classList.add(userTheme);
            if (userTheme === 'dark') {
                themeToggleLightIcon.classList.remove('hidden');
                themeToggleDarkIcon.classList.add('hidden');
            } else {
                themeToggleDarkIcon.classList.remove('hidden');
                themeToggleLightIcon.classList.add('hidden');
            }
        } else {
            // 2. Check for system preference
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                htmlElement.classList.add('dark');
                themeToggleLightIcon.classList.remove('hidden');
                themeToggleDarkIcon.classList.add('hidden');
            } else {
                htmlElement.classList.add('light'); // Default to light if no preference
                themeToggleDarkIcon.classList.remove('hidden');
                themeToggleLightIcon.classList.add('hidden');
            }
        }
    }

    initializeTheme();

    themeToggleBtn.addEventListener('click', function () {
        // toggle icons
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');

        // if set via local storage previously
        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                htmlElement.classList.add('dark');
                htmlElement.classList.remove('light');
                localStorage.setItem('color-theme', 'dark');
            } else {
                htmlElement.classList.remove('dark');
                htmlElement.classList.add('light');
                localStorage.setItem('color-theme', 'light');
            }

        } else {
            // if NOT set via local storage previously
            if (htmlElement.classList.contains('dark')) {
                htmlElement.classList.remove('dark');
                htmlElement.classList.add('light');
                localStorage.setItem('color-theme', 'light');
            } else {
                htmlElement.classList.add('dark');
                htmlElement.classList.remove('light');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    });

    // Listen for changes in system preference
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        // Only update if no explicit user preference is set
        if (!localStorage.getItem('color-theme')) {
            if (event.matches) {
                htmlElement.classList.add('dark');
                htmlElement.classList.remove('light');
                themeToggleLightIcon.classList.remove('hidden');
                themeToggleDarkIcon.classList.add('hidden');
            } else {
                htmlElement.classList.remove('dark');
                htmlElement.classList.add('light');
                themeToggleDarkIcon.classList.remove('hidden');
                themeToggleLightIcon.classList.add('hidden');
            }
        }
    });
});