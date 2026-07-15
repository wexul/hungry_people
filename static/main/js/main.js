$(document).ready(function () {

    const $window = $(window);
    const $header = $('.header');
    const $specialtiesSlider = $('.specialties__slider');
    const $backToTop = $('.back-to-top');
    const $authModal = $('.auth-modal');
    const $authStatus = $('.auth-modal__status');


    function getCookie(name) {
        const cookie = document.cookie
            .split(';')
            .map(value => value.trim())
            .find(value => value.startsWith(`${name}=`));

        return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : '';
    }


    function csrfHeaders() {
        return {
            'X-CSRFToken': getCookie('csrftoken')
        };
    }


    function serializeForm($form) {
        const fields = $form.serializeArray().filter(function (field) {
            return field.name !== 'csrfmiddlewaretoken';
        });

        return $.param(fields);
    }


    function firstError(errors) {
        if (!errors) {
            return '';
        }

        const field = Object.keys(errors)[0];
        return field && errors[field] ? errors[field][0] : '';
    }


    function responseMessage(xhr, fallback) {
        const response = xhr.responseJSON || {};
        return firstError(response.errors) || response.message || fallback;
    }


    function setButtonLoading($button, isLoading, loadingText) {
        if (!$button.length) {
            return;
        }

        if (isLoading) {
            $button.data('original-text', $button.text()).prop('disabled', true).text(loadingText);
            return;
        }

        $button.prop('disabled', false).text($button.data('original-text') || $button.text());
    }


    /* =========================
       FIXED HEADER
    ========================= */

    function updateHeader() {
        const scrollTop = $window.scrollTop();

        $header.toggleClass('header_fixed', scrollTop > 80);
        $backToTop.toggleClass('is-visible', scrollTop > 600);
    }

    updateHeader();
    $window.on('scroll', updateHeader);


    /* =========================
       MOBILE NAVIGATION
    ========================= */

    $('.header__toggle').on('click', function () {
        const isOpen = $header.toggleClass('header_menu-open').hasClass('header_menu-open');

        $(this)
            .attr('aria-expanded', isOpen)
            .attr('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    });

    $('.header__link[href^="#"], .header__logo').on('click', function () {
        $header.removeClass('header_menu-open');
        $('.header__toggle')
            .attr('aria-expanded', 'false')
            .attr('aria-label', 'Open navigation');
    });

    $window.on('resize', function () {
        if ($window.width() > 1200) {
            $header.removeClass('header_menu-open');
            $('.header__toggle')
                .attr('aria-expanded', 'false')
                .attr('aria-label', 'Open navigation');
        }
    });


    /* =========================
       SPECIALITIES SLIDER
    ========================= */

    if ($specialtiesSlider.length) {
        if (typeof $.fn.slick !== 'function') {
            console.error('Slick Carousel is not loaded.');
        } else if (!$specialtiesSlider.hasClass('slick-initialized')) {
            $specialtiesSlider.slick({
                arrows: false,
                dots: true,
                infinite: true,
                speed: 500,
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: false
            });
        }
    }


    /* =========================
       MENU FILTER
    ========================= */

    $('.menu__filters').on('click', '.menu__filter', function () {
        const $selectedFilter = $(this);
        const selectedCategory = $selectedFilter.data('filter');
        const isAlreadyActive = $selectedFilter.hasClass('is-active');

        $('.menu__filter')
            .removeClass('is-active')
            .attr('aria-pressed', 'false');

        if (isAlreadyActive) {
            $('.menu__item').removeClass('is-hidden');
            return;
        }

        $selectedFilter
            .addClass('is-active')
            .attr('aria-pressed', 'true');

        $('.menu__item').each(function () {
            const itemCategory = $(this).data('category');
            $(this).toggleClass('is-hidden', itemCategory !== selectedCategory);
        });
    });


    /* =========================
       AUTHENTICATION
    ========================= */

    function showAuthStatus(message, type) {
        $authStatus
            .removeClass('is-success is-error')
            .addClass(type === 'success' ? 'is-success' : 'is-error')
            .text(message);
    }

    function openAuthModal() {
        $header.removeClass('header_menu-open');
        $('.header__toggle').attr('aria-expanded', 'false');

        $authModal.addClass('is-open').attr('aria-hidden', 'false');
        $('body').addClass('auth-modal-open');
        $authModal.find('input:visible').first().trigger('focus');
    }

    function closeAuthModal() {
        $authModal.removeClass('is-open').attr('aria-hidden', 'true');
        $('body').removeClass('auth-modal-open');
        $authStatus.removeClass('is-success is-error').text('');
    }

    function setAuthenticatedState(isAuthenticated) {
        const $button = $('[data-auth-button]');

        if (isAuthenticated) {
            $button.removeAttr('data-auth-open').attr('data-auth-logout', '').text('Logout');
        } else {
            $button.removeAttr('data-auth-logout').attr('data-auth-open', '').text('Login');
        }
    }

    $(document).on('click', '[data-auth-open]', openAuthModal);
    $('[data-auth-close]').on('click', closeAuthModal);

    $(document).on('click', '[data-auth-logout]', function () {
        const $button = $(this);

        $.ajax({
            url: $button.data('logout-url'),
            method: 'POST',
            dataType: 'json',
            headers: csrfHeaders()
        })
            .done(function () {
                setAuthenticatedState(false);
            })
            .fail(function (xhr) {
                alert(responseMessage(xhr, 'Could not sign out.'));
            });
    });

    $(document).on('keydown', function (event) {
        if (event.key === 'Escape' && $authModal.hasClass('is-open')) {
            closeAuthModal();
        }
    });

    $('[data-auth-tab]').on('click', function () {
        const selectedPanel = $(this).data('auth-tab');
        const selectedTitle = $(this).data('auth-title');

        $('[data-auth-tab]').removeClass('is-active').attr('aria-selected', 'false');
        $(this).addClass('is-active').attr('aria-selected', 'true');

        $('[data-auth-panel]').attr('hidden', true);
        $(`[data-auth-panel="${selectedPanel}"]`).removeAttr('hidden');
        $('#auth-modal-title').text(selectedTitle);
        $authStatus.removeClass('is-success is-error').text('');
        $(`[data-auth-panel="${selectedPanel}"] input`).first().trigger('focus');
    });

    $('.auth-modal__form').on('submit', function (event) {
        event.preventDefault();

        const formElement = this;
        const $form = $(formElement);
        const $button = $form.find('.auth-modal__submit');

        if (!formElement.checkValidity()) {
            formElement.reportValidity();
            return;
        }

        setButtonLoading($button, true, 'Sending...');
        $authStatus.removeClass('is-success is-error').text('');

        $.ajax({
            url: formElement.action,
            method: 'POST',
            data: serializeForm($form),
            dataType: 'json',
            headers: csrfHeaders()
        })
            .done(function (response) {
                showAuthStatus(response.message, 'success');
                setAuthenticatedState(true);
                formElement.reset();
                window.setTimeout(closeAuthModal, 700);
            })
            .fail(function (xhr) {
                showAuthStatus(responseMessage(xhr, 'The request failed.'), 'error');
            })
            .always(function () {
                setButtonLoading($button, false);
            });
    });

    $('.auth-modal__forgot').on('click', function () {
        const email = $('[data-auth-panel="login"] [name="email"]').val().trim();
        if (!email) {
            showAuthStatus('Enter your email first.', 'error');
            return;
        }

        $.ajax({
            url: $(this).data('reset-url'),
            method: 'POST',
            dataType: 'json',
            headers: csrfHeaders(),
            data: {email: email}
        })
            .done(function (response) {
                showAuthStatus(response.message, 'success');
            })
            .fail(function (xhr) {
                showAuthStatus(responseMessage(xhr, 'Could not send the reset link.'), 'error');
            });
    });


    /* =========================
       BACK TO TOP
    ========================= */

    $backToTop.on('click', function () {
        $('html, body').animate({scrollTop: 0}, 500);
    });


    /* =========================
       PUBLIC FORMS
    ========================= */

    function showFormStatus($form, message, type) {
        $form.find('.form-status')
            .removeClass('is-success is-error')
            .addClass(type === 'success' ? 'is-success' : 'is-error')
            .text(message);
    }

    function submitPublicForm(formElement, loadingText) {
        const $form = $(formElement);
        const $button = $form.find('button[type="submit"]');

        if (!formElement.checkValidity()) {
            formElement.reportValidity();
            return;
        }

        setButtonLoading($button, true, loadingText);

        $.ajax({
            url: formElement.action,
            method: 'POST',
            data: serializeForm($form),
            dataType: 'json',
            headers: csrfHeaders()
        })
            .done(function (response) {
                showFormStatus($form, response.message, 'success');
                formElement.reset();
            })
            .fail(function (xhr) {
                showFormStatus($form, responseMessage(xhr, 'The request failed.'), 'error');
            })
            .always(function () {
                setButtonLoading($button, false);
            });
    }

    $('.booking__form').on('submit', function (event) {
        event.preventDefault();
        submitPublicForm(this, 'Booking...');
    });

    $('.contact__form').on('submit', function (event) {
        event.preventDefault();
        submitPublicForm(this, 'Sending...');
    });

    $('.booking__form, .contact__form').on('input change', function () {
        $(this).find('.form-status').removeClass('is-success is-error').text('');
    });

});
