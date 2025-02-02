if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

// This script toggles the active class and aria-current attribute on the nav links
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const startTimeInput = document.getElementById("start_time");
  const endTimeInput = document.getElementById("end_time");

  form.addEventListener("submit", function (event) {
    const startTime = new Date(startTimeInput.value);
    const endTime = new Date(endTimeInput.value);
    const currentTime = new Date();

    if (startTime > currentTime || endTime > currentTime) {
      alert("Start and end times must be before the current datetime.");
      event.preventDefault();
      return;
    }

    if (endTime < startTime) {
      alert("End time cannot be before start time.");
      event.preventDefault();
      return;
    }
  });
});

function confirmAction(message, formId) {
  if (confirm(message)) {
    document.getElementById(formId).submit();
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const logoutButton = document.getElementById("logoutButton");
  const deleteAccountButton = document.getElementById("deleteAccountButton");
  const successMessage = document.getElementById("successMessage");

  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      confirmAction("Are you sure you want to logout?", "logoutForm");
    });
  }

  if (deleteAccountButton) {
    deleteAccountButton.addEventListener("click", function () {
      confirmAction(
        "Are you sure you want to delete your account, and all your entries? This action cannot be undone.",
        "deleteAccountForm"
      );
    });
  }
});
