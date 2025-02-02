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

    // Check if start and end times are before the current datetime
    if (startTime > currentTime || endTime > currentTime) {
      alert("Start and end times must be before the current datetime.");
      event.preventDefault();
      return;
    }

    // Check if end time is before start time
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

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#entryForm");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.time_worked = parseFloat(data.time_worked); // Ensure time_worked is a float
    fetch(form.action, {
      method: form.method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});

document
  .getElementById("searchForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const params = new URLSearchParams(formData).toString();
    fetch(`/search?${params}`)
      .then((response) => response.json())
      .then((data) => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        data.forEach((entry) => {
          const entryDiv = document.createElement("div");
          entryDiv.classList.add("card", "mb-3");
          entryDiv.innerHTML = `
                            <div class="card-header">${entry.devtag}</div>
                            <div class="card-body">
                                <h5 class="card-title">${entry.project}</h5>
                                <p class="card-text"><strong>Start Time:</strong> ${entry.start_time}</p>
                                <p class="card-text"><strong>End Time:</strong> ${entry.end_time}</p>
                                <p class="card-text"><strong>Diary Entry:</strong> ${entry.diary_entry}</p>
                                <p class="card-text"><strong>Time Worked (Hours):</strong> ${entry.time_worked}</p>
                                <p class="card-text"><strong>Repository:</strong> <a href="${entry.repo}" target="_blank">${entry.repo}</a></p>
                                <p class="card-text">${entry.developer_notes}</p>
                                <p class="card-text">${entry.code_additions}</p>
                            </div>
                        `;
          resultsDiv.appendChild(entryDiv);
        });
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

    // Check if start and end times are before the current datetime
    if (startTime > currentTime || endTime > currentTime) {
      alert("Start and end times must be before the current datetime.");
      event.preventDefault();
      return;
    }

    // Check if end time is before start time
    if (endTime < startTime) {
      alert("End time cannot be before start time.");
      event.preventDefault();
      return;
    }
  });
});
