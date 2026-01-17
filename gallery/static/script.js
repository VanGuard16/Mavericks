const lightbox = GLightbox({
    selector: '.glightbox',
    touchNavigation: true,
    loop: true
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const img = entry.target;
      img.src = img.dataset.src;
      img.onload = () => {img.classList.add("loaded")}
      observer.unobserve(img)
    });
  }, {rootMargin: '300px'})

  document.querySelectorAll('.gallery-img').forEach(img => observer.observe(img))