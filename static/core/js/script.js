// صبر می‌کنیم تا تمام محتوای HTML صفحه به طور کامل بارگذاری و آماده شود
document.addEventListener('DOMContentLoaded', function () {

    // =================================================================
    // 1. مدیریت منوی ناوبری (Navigation Menu)
    // =================================================================
    const menu = document.querySelector('#menu-bar');
    const navbar = document.querySelector('.navbar');

    if (menu && navbar) {
        menu.onclick = () => {
            menu.classList.toggle('fa-times');
            navbar.classList.toggle('active');
        }
        window.onscroll = () => {
            menu.classList.remove('fa-times');
            navbar.classList.remove('active');
        }
    }

    // =================================================================
    // 2. مدیریت اسلایدر صفحه اصلی (Home Page Slider)
    // =================================================================
    const slides = document.querySelectorAll('.home .slide-container');

if (slides.length > 0) {
    let slideIndex = 0;

    function showNextSlide() {
        slides[slideIndex].classList.remove('active');
        slideIndex = (slideIndex + 1) % slides.length;
        slides[slideIndex].classList.add('active');
    }

    function showPrevSlide() {
        slides[slideIndex].classList.remove('active');
        slideIndex = (slideIndex - 1 + slides.length) % slides.length;
        slides[slideIndex].classList.add('active');
    }

    // **** این بخش را اضافه یا اصلاح کنید ****
    // پیدا کردن دکمه‌ها بر اساس ID
    const nextBtn = document.querySelector('#next-btn');
    const prevBtn = document.querySelector('#prev-btn');

    // اضافه کردن شنونده رویداد کلیک
    if (nextBtn && prevBtn) {
        nextBtn.addEventListener('click', showNextSlide);
        prevBtn.addEventListener('click', showPrevSlide);
    }
}
    // =================================================================
    // 3. مدیریت گالری تصاویر محصولات (Product Image Gallery)
    // =================================================================
    const smallImages = document.querySelectorAll('.small-image .small-thumb');
    if (smallImages.length > 0) {
        smallImages.forEach(smallImage => {
            smallImage.addEventListener('click', () => {
                const src = smallImage.getAttribute('src');
                const productRow = smallImage.closest('.row');
                if (productRow) {
                    const bigImage = productRow.querySelector('.big-image .big-image-content');
                    if (bigImage) {
                        bigImage.src = src;
                    }
                }
            });
        });
    }

    // =================================================================
    // 4. مدیریت دکمه افزودن/حذف از لیست علاقه‌مندی‌ها (Wishlist Toggle)
    // =================================================================
    
    // این خط در کد شما جا افتاده بود و اکنون اضافه شده است
    const wishlistButtons = document.querySelectorAll('.wishlist-toggle-btn');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const link = this;
            const url = link.href;
            const productId = link.dataset.productId;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    showToast(data.message);

                    if (productId) { // اگر در صفحه علاقه‌مندی‌ها هستیم
                        const cardToRemove = document.getElementById(`product-card-${productId}`);
                        if (cardToRemove) {
                            cardToRemove.style.transition = 'opacity 0.5s, transform 0.5s';
                            cardToRemove.style.opacity = '0';
                            cardToRemove.style.transform = 'scale(0.9)';
                            setTimeout(() => {
                                cardToRemove.remove();
                                const container = document.querySelector('.wishlist-page #wishlist-container');
                                if (container && container.children.length === 0) {
                                    const productListUrl = container.dataset.productListUrl;
                                    container.innerHTML = `
                                        <div class="empty-wishlist" id="empty-wishlist-message">
                                            <p>لیست علاقه‌مندی‌های شما خالی است.</p>
                                            <a href="${productListUrl}" class="btn btn-primary">مشاهده همه محصولات</a>
                                        </div>`;
                                }
                            }, 500);
                        }
                    } else { // اگر در صفحات دیگر هستیم
                        if (data.action === 'added') {
                            link.classList.add('text-danger');
                            const icon = link.querySelector('i, .fa-heart');
                            if (icon) {
                                icon.classList.add('fas');
                                icon.classList.remove('far');
                            }
                        } else {
                            link.classList.remove('text-danger');
                            const icon = link.querySelector('i, .fa-heart');
                            if (icon) {
                                icon.classList.remove('fas');
                                icon.classList.add('far');
                            }
                        }
                    }
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Wishlist toggle error:', error);
                showToast('خطایی در ارتباط با سرور رخ داد.', 'error');
            });
        });
    });
});

// =================================================================
// توابع کمکی (Helper Functions)
// =================================================================

function showToast(message, type = 'success') {
    const toastContainer = document.createElement('div');
    toastContainer.className = `toast-message ${type}`;
    toastContainer.textContent = message;
    document.body.appendChild(toastContainer);

    Object.assign(toastContainer.style, {
        position: 'fixed', bottom: '20px', left: '50%', transform: 'translateX(-50%)',
        padding: '12px 25px', borderRadius: '8px',
        backgroundColor: type === 'success' ? '#28a745' : '#dc3545',
        color: 'white', zIndex: 1050, opacity: 0,
        transition: 'opacity 0.5s, transform 0.5s',
        boxShadow: '0 4px 15px rgba(0,0,0,0.2)'
    });

    setTimeout(() => {
        toastContainer.style.opacity = 1;
        toastContainer.style.transform = 'translateX(-50%) translateY(-10px)';
    }, 100);

    setTimeout(() => {
        toastContainer.style.opacity = 0;
        toastContainer.addEventListener('transitionend', () => {
            if (document.body.contains(toastContainer)) {
                document.body.removeChild(toastContainer);
            }
        });
    }, 3000);
}

function getCsrfToken() {
    const tokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (tokenElement) {
        return tokenElement.value;
    }
    let csrfToken = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                csrfToken = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                break;
            }
        }
    }
    return csrfToken;
}


