console.log("✅ script.js loaded!");

document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href^="#"]');
  if (!link) return;
  const id = link.getAttribute('href');
  if (id.length <= 1) return;
  const el = document.querySelector(id);
  if (!el) return;
  e.preventDefault();
  window.scrollTo({ top: el.offsetTop - 70, behavior: 'smooth' });
});

const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');
if (menuToggle && navLinks) {
  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('is-open');
  });
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => navLinks.classList.remove('is-open'));
  });
}

const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('show');
  });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal').forEach(el => io.observe(el));

function animateCounter(el, target, duration = 1400) {
  const start = 0;
  const startTime = performance.now();
  function tick(now) {
    const p = Math.min(1, (now - startTime) / duration);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.floor(start + (target - start) * eased).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const counters = document.querySelectorAll('.counter__num');
const counterIO = new IntersectionObserver((entries, obs) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseInt(el.getAttribute('data-target'), 10) || 0;
    animateCounter(el, target);
    obs.unobserve(el);
  });
}, { threshold: 0.6 });
counters.forEach(el => counterIO.observe(el));

document.getElementById('year').textContent = new Date().getFullYear();

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document.querySelectorAll('.contact-form').forEach(form => {
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const status = document.createElement('p');
    status.style.marginTop = '10px';
    status.style.fontWeight = '500';
    form.appendChild(status);

    const data = new FormData(form);
    try {
      const response = await fetch(form.action, {
        method: form.method,
        body: data,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
        },
      });

      if (response.ok) {
        const result = await response.json();
        if (result.status === "success") {
          status.textContent = "✅ Thank you! Your response has been recorded.";
          status.style.color = "var(--green-deep)";
          form.reset();
        } else {
          status.textContent = "⚠️ Please fill out all required fields.";
          status.style.color = "#d76b3b";
        }
      } else {
        status.textContent = "❌ Server error. Please try again later.";
        status.style.color = "#d76b3b";
      }
    } catch (err) {
      console.error("Form submission failed:", err);
      status.textContent = "❌ Could not send request.";
      status.style.color = "#d76b3b";
    }

    setTimeout(() => status.remove(), 4000);
  });
});

async function loadDonations() {
  try {
    console.log("Fetching donations...");
    const res = await fetch("http://127.0.0.1:8000/donations/list/");
    console.log("Response status:", res.status);

    if (!res.ok) throw new Error("Failed to load donations");

    const text = await res.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch (err) {
      console.error("❌ Could not parse JSON:", err);
      return;
    }

    const container = document.getElementById("donationList");
    if (!container) {
      console.error("❌ donationList div not found!");
      return;
    }

    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = `<p class="center muted">No recent donations yet — be the first to give 💚</p>`;
      return;
    }

    container.innerHTML = data.map((d, i) => `
      <div class="card donation-card reveal slide-up delay-${i % 3}">
        <h3>${d.restaurant_name}</h3>
        <p><strong>${d.food_type}</strong></p>
        <p>Quantity: ${d.quantity}</p>
        <p><em>${d.city}</em> • ${d.date}</p>
      </div>
    `).join("");

    document.querySelectorAll("#donationList .card").forEach(el => {
      el.classList.add("visible-now");
    });

    console.log("🎉 Donation cards rendered successfully!");
  } catch (err) {
    console.error("❌ Donation load failed:", err);
  }
}

document.addEventListener("DOMContentLoaded", loadDonations);
