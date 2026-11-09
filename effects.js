// Progressive enhancement only: content remains visible if JavaScript is disabled.
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  }, {threshold: .08, rootMargin: '0px 0px 30px 0px'});
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}
