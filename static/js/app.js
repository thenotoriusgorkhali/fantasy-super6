// Global JS utilities for Fantasy Super 6

// Animated counter
function animateCounter(el, target, duration = 1500) {
  const start = 0;
  const increment = target / (duration / 16);
  let current = start;
  const update = () => {
    current = Math.min(current + increment, target);
    el.textContent = Math.floor(current).toLocaleString();
    if (current < target) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// Intersection observer for counters
document.addEventListener('DOMContentLoaded', () => {
  const counters = document.querySelectorAll('[data-counter]');
  if (counters.length === 0) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.dataset.counter);
        animateCounter(entry.target, target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => observer.observe(c));

  // Auto-dismiss messages
  const messages = document.querySelectorAll('.auto-dismiss');
  messages.forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'all 0.5s ease';
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(100%)';
      setTimeout(() => msg.remove(), 500);
    }, 4000);
  });
});
