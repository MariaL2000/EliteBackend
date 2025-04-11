const d = document;

d.addEventListener("DOMContentLoaded", function () {
  d.querySelectorAll(".carousel-wrapper").forEach(initializeCarousel);
});

function toggleCard() {
  const overlay = d.querySelector(".overlay");
  overlay.style.display =
    overlay.style.display === "none" || overlay.style.display === ""
      ? "flex"
      : "none";
}

function initializeCarousel(carouselWrapper) {
  const container = carouselWrapper.querySelector(".products-container");
  const wrapper = carouselWrapper.querySelector(".products-wrapper");
  const leftBtn = carouselWrapper.querySelector(".arrow-left");
  const rightBtn = carouselWrapper.querySelector(".arrow-right");
  const cardWidth = 300; // Width of each card plus gap
  const scrollAmount = cardWidth + 24; // Card width plus gap

  // Function to scroll left
  function scrollLeft() {
    const currentScroll = container.scrollLeft;
    container.scrollTo({
      left: currentScroll - scrollAmount,
      behavior: "smooth",
    });
    updateButtonStates();
  }

  // Function to scroll right
  function scrollRight() {
    const currentScroll = container.scrollLeft;
    container.scrollTo({
      left: currentScroll + scrollAmount,
      behavior: "smooth",
    });
    updateButtonStates();
  }

  // Update button states based on scroll position
  function updateButtonStates() {
    const currentScroll = container.scrollLeft;
    const maxScroll = container.scrollWidth - container.clientWidth;

    leftBtn.style.opacity = currentScroll <= 0 ? "0.5" : "1";
    leftBtn.style.cursor = currentScroll <= 0 ? "default" : "pointer";

    rightBtn.style.opacity = currentScroll >= maxScroll ? "0.5" : "1";
    rightBtn.style.cursor = currentScroll >= maxScroll ? "default" : "pointer";
  }

  leftBtn.addEventListener("click", scrollLeft);
  rightBtn.addEventListener("click", scrollRight);

  container.addEventListener("scroll", updateButtonStates);

  updateButtonStates();

  let isDown = false;
  let startX;
  let initialScrollPos;

  container.addEventListener("mousedown", (e) => {
    isDown = true;
    container.style.cursor = "grabbing";
    startX = e.pageX - container.offsetLeft;
    initialScrollPos = container.scrollLeft;
  });

  container.addEventListener("mouseleave", () => {
    isDown = false;
    container.style.cursor = "grab";
  });

  container.addEventListener("mouseup", () => {
    isDown = false;
    container.style.cursor = "grab";
  });

  container.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - container.offsetLeft;
    const walk = (x - startX) * 2;
    container.scrollLeft = initialScrollPos - walk;
    updateButtonStates();
  });
}

d.addEventListener("DOMContentLoaded", function () {
  const animatedElements = d.querySelectorAll(".animated");

  function checkVisibility() {
    const windowHeight = window.innerHeight;

    animatedElements.forEach((element) => {
      const elementTop = element.getBoundingClientRect().top;

      if (elementTop < windowHeight * 0.8) {
        // 80% del viewport
        element.classList.add("visible");
      } else {
        element.classList.remove("visible");
      }
    });
  }

  window.addEventListener("scroll", checkVisibility);
  checkVisibility(); // Ejecutar al cargar la página
});

function moveSlide(direction, carouselId) {
  const carousel = d.getElementById(carouselId);
  const slides = carousel.children.length;
  let index = parseInt(carousel.dataset.index || 0);
  index = (index + direction + slides) % slides;
  carousel.dataset.index = index;
  carousel.style.transform = `translateX(${-index * 100}%)`;
}

const options = {
  threshold: 0, // 0 significa que se dispara cuando el elemento sale/entra completamente
};

const callback = (entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) {
      console.log("¡Elemento fuera del viewport!");
      d.querySelector(".navbar-new").style.display = "block";
    } else {
      // El elemento está visible
      console.log("¡Elemento dentro del viewport!");
      d.querySelector(".navbar-new").style.display = "none";
    }
  });
};

const observer = new IntersectionObserver(callback, options);

// Selecciona el elemento que quieres observar
const elemento = d.querySelectorAll(".quote-button")[1];

// Comienza a observar
observer.observe(elemento);

document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card__carousel");
  const dotsContainer = document.querySelector(".dots");
  const playPauseBtn = document.getElementById("playPauseBtn");
  const carousel = document.querySelector(".carousel__scroll");
  let currentIndex = 0;
  let slideInterval = null;
  let fillAnimationInterval = null;
  let isScrolling = false;
  let scrollTimeout;

  // Create dots
  cards.forEach((_, index) => {
    const dot = document.createElement("div");
    dot.classList.add("dot");
    if (index === 0) dot.classList.add("active");
    dot.addEventListener("click", () => goToSlide(index));
    dotsContainer.appendChild(dot);
  });

  // Add scroll event listener
  carousel.addEventListener("scroll", () => {
    if (!isScrolling) {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const scrollPosition = carousel.scrollLeft;
        const cardWidth =
          cards[0].offsetWidth + parseInt(getComputedStyle(carousel).gap);
        const newIndex = Math.round(scrollPosition / cardWidth);

        if (newIndex !== currentIndex) {
          goToSlide(newIndex);
        }
      }, 50);
    }
  });

  function updateActiveDotGradient(notContinue = true) {
    const dots = document.querySelectorAll(".dot");
    dots.forEach((dot) => {
      if (!dot.classList.contains("active")) {
        dot.style.background = "#ccc";
      }
    });

    const activeDot = document.querySelector(".dot.active");
    if (!notContinue) {
      clearInterval(fillAnimationInterval);
      activeDot.style.background = "#ccc";
      return;
    }

    let progress = 0;

    clearInterval(fillAnimationInterval);
    fillAnimationInterval = setInterval(() => {
      progress = (progress + 1) % 100;
      activeDot.style.background = `linear-gradient(to right, #000000 ${progress}%, #ccc ${progress}%)`;

      if (!activeDot.classList.contains("active")) {
        clearInterval(fillAnimationInterval);
      }
    }, 50);
  }

  function goToSlide(index) {
    isScrolling = true;
    const cardWidth =
      cards[0].offsetWidth + parseInt(getComputedStyle(carousel).gap);

    // Ocultar el título del nuevo slide antes de la transición
    const nextTitle = cards[index].querySelector("h1");
    nextTitle.style.opacity = "0";

    carousel.scrollTo({
      left: cardWidth * index,
      behavior: "smooth",
    });

    cards[currentIndex].classList.remove("active");
    const dots = document.querySelectorAll(".dot");
    dots.forEach((dot) => dot.classList.remove("active"));

    currentIndex = index;

    setTimeout(() => {
      cards[currentIndex].classList.remove("active");
      void cards[currentIndex].offsetWidth;
      cards[currentIndex].classList.add("active");

      const currentTitle = cards[currentIndex].querySelector("h1");
      currentTitle.style.opacity = "1";
      currentTitle.classList.remove(
        "animate__animated",
        "animate__fadeInRight"
      );
      void currentTitle.offsetWidth;
      currentTitle.classList.add("animate__animated", "animate__fadeInRight");
    }, 500);

    dots[currentIndex].classList.add("active");

    const isPlaying = playPauseBtn
      .querySelector("svg")
      .parentElement.classList.contains("playing");
    updateActiveDotGradient(isPlaying);

    setTimeout(() => {
      isScrolling = false;
    }, 500);
  }

  function nextSlide() {
    let nextIndex = currentIndex + 1;
    if (nextIndex >= cards.length) nextIndex = 0;
    goToSlide(nextIndex);
  }

  function toggleSlideshow() {
    const svg = playPauseBtn.querySelector("svg");
    svg.parentElement.classList.toggle("playing");

    if (svg.parentElement.classList.contains("playing")) {
      updateActiveDotGradient(true);
      slideInterval = setInterval(nextSlide, 5000);
    } else {
      clearInterval(slideInterval);
      updateActiveDotGradient(false);
    }
  }

  playPauseBtn.addEventListener("click", toggleSlideshow);

  const element = d.querySelector(".container-play");

  window.addEventListener("scroll", () => {
    const rect = element.getBoundingClientRect();
    const windowHeight = window.innerHeight;

    if (rect.top <= windowHeight) {
      // Multiplying by a higher number (40 instead of 20) makes it reach 0 faster
      const translation = -10 + ((windowHeight - rect.top) / windowHeight) * 40;
      // Clamp the value to prevent going past 0
      const finalTranslation = Math.min(translation, 0);
      element.style.transform = `translateY(${finalTranslation}rem)`;
    }
  });

  const options = {
    threshold: 0, // 0 significa que se dispara cuando el elemento sale/entra completamente
    rootMargin: "30px",
  };

  const callback = (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        console.log("¡Elemento fuera del viewport!");
        element.style.opacity = "0";
      } else {
        console.log("¡Elemento dentro del viewport!");
        element.style.opacity = "1";
      }
    });
  };

  const observer = new IntersectionObserver(callback, options);

  observer.observe(element);
});

document.addEventListener("DOMContentLoaded", function () {
  // Seleccionamos todas las imágenes circulares
  const circleImages = document.querySelectorAll(".circle-image");

  circleImages.forEach((image) => {
    image.addEventListener("click", function (event) {
      // Encontrar la tarjeta contenedora de la imagen clickeada
      const productCard = event.target.closest(".product-card");

      if (productCard) {
        // Buscar el contenido de la tarjeta
        const cardContent = productCard.querySelector(".card-content");

        if (cardContent) {
          // Alternar la clase 'visible' para mostrar/ocultar la tarjeta
          cardContent.classList.toggle("visible");
        }
      }
    });
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".video-slide");
  const nextBtn = document.querySelector(".video-nav.next");
  const prevBtn = document.querySelector(".video-nav.prev");
  let currentSlide = 0;

  // Función para pausar todos los videos
  function pauseAllVideos() {
    slides.forEach((slide) => {
      const video = slide.querySelector("video");
      if (video.currentTime > 0) {
        video.pause();
        video.currentTime = 0;
      }
    });
  }
// Función para mostrar el slide actual
  function showSlide(index) {
    pauseAllVideos();
    slides.forEach((slide) => slide.classList.remove("active"));
    slides[index].classList.add("active");
  }
// Botón siguiente
  nextBtn.addEventListener("click", () => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  });
 // Botón anterior
  prevBtn.addEventListener("click", () => {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
  });

  
  document.querySelector(".video-carousel").addEventListener("click", (e) => {
    if (e.target.closest(".play-button")) {
      const activeSlide = slides[currentSlide];
      const video = activeSlide.querySelector("video");
      if (video) {
        if (video.paused) {
          video.play();
        } else {
          video.pause();
          video.currentTime = 0; // Reinicia el video
        }
      }
    }
  });

  const html = document.documentElement;
  const canvas = document.getElementById("hero-lightpass");
  const context = canvas.getContext("2d");
  const canvasContainer = document.querySelector(".canvas-container");
  const container = document.querySelector(".container");
  let stop = false;
  let canvasInView = false; // Flag to track if canvas is in viewport
  let lastScrollTop = 0; // To track scroll direction

  const frameCount = 148;
  const currentFrame = (index) =>
    `https://www.apple.com/105/media/us/airpods-pro/2019/1299e2f5_9206_4470_b28e_08307a42f19b/anim/sequence/large/01-hero-lightpass/${index
      .toString()
      .padStart(4, "0")}.jpg`;

  const preloadImages = () => {
    for (let i = 1; i < frameCount; i++) {
      const img = new Image();
      img.src = currentFrame(i);
      if (i == 147) {
        stop = true;
        return;
      }
    }
  };

  if (stop) console.log({stop});

  const img = new Image();
  img.src = currentFrame(1);

  canvas.width = 1158;
  canvas.height = 770;

  img.onload = function () {
    context.drawImage(img, 0, 0);
  };

  const updateImage = (index) => {
    // Ensure index is within valid range (1 to frameCount)
    const validIndex = Math.max(1, Math.min(frameCount, Math.round(index)));
    img.src = currentFrame(validIndex);
    context.drawImage(img, 0, 0);
  };

  // Set up Intersection Observer to detect when canvas enters viewport
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        canvasInView = entry.isIntersecting;

        // If canvas just entered view, update the image to current scroll position
        if (canvasInView) {
          updateAnimationFrame();
        }
      });
    },
    {
      threshold: 0.1, // Trigger when at least 10% of the canvas is visible
    }
  );

  // Start observing the canvas
  observer.observe(canvas);

  // Function to calculate and update the current animation frame
  function updateAnimationFrame() {
    const scrollTop = html.scrollTop;
    const containerRect = container.getBoundingClientRect();
    const containerTop = containerRect.top + window.scrollY;
    const containerHeight = container.offsetHeight;

    // Calculate animation progress based on scroll position within container
    const scrollProgress =
      (scrollTop - containerTop) / (containerHeight - window.innerHeight);
    const animationProgress = Math.max(0, Math.min(1, scrollProgress));

    const frameIndex = Math.round(animationProgress * (frameCount - 1)) + 1;

    requestAnimationFrame(() => updateImage(frameIndex));
  }

  // Initialize the animation range once the page loads
  window.addEventListener("load", () => {
    // Initial setup
    updateAnimationFrame();
  });

  window.addEventListener("scroll", () => {
    const scrollTop = html.scrollTop;
    const maxScrollTop = html.scrollHeight - window.innerHeight;
    const scrollFraction = scrollTop / maxScrollTop;

    // Determine scroll direction
    const scrollingDown = scrollTop > lastScrollTop;
    lastScrollTop = scrollTop;

    // Get container position information
    const containerRect = container.getBoundingClientRect();
    const containerTop = containerRect.top + window.scrollY;
    const containerBottom = containerTop + container.offsetHeight;

    // Check if we should fix or unfix the canvas container
    if (
      scrollTop >= containerTop &&
      scrollTop < containerBottom - canvasContainer.offsetHeight
    ) {
      // Fix the canvas container when scroll is within the container
      canvasContainer.classList.add("fixed");
      canvasContainer.style.top = "0";
    } else {
      // Unfix when outside the container
      canvasContainer.classList.remove("fixed");

      // If we've scrolled past the container, position at the bottom
      if (scrollTop >= containerBottom - canvasContainer.offsetHeight) {
        canvasContainer.style.top =
          container.offsetHeight - canvasContainer.offsetHeight + "px";
      } else {
        // Reset top position when above the container
        canvasContainer.style.top = "";
      }
    }

    // Mostrar un elemento cuando el scroll llega al 50%
    if (scrollFraction >= 0.5) {
      document.getElementById("c").style.display = "none";
    } else {
      document.getElementById("c").style.display = "block";
    }

    // Only update animation when canvas is in view
    if (canvasInView) {
      updateAnimationFrame();
    }
  });

  // Handle window resize to recalculate positions
  window.addEventListener("resize", () => {
    if (canvasInView) {
      updateAnimationFrame();
    }
  });

  preloadImages();
});
