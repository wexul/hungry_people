$(document).ready(function () {

    const $window = $(window);
    const $header = $('.header');
    const $specialtiesSlider = $('.specialties__slider');


    /* =========================
       FIXED HEADER
    ========================= */

    function updateHeader() {
        const isScrolled = $window.scrollTop() > 80;

        $header.toggleClass('header_fixed', isScrolled);
    }

    updateHeader();

    $window.on('scroll', updateHeader);


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

        const selectedCategory = $(this).data('filter');

        $('.menu__filter').removeClass('is-active');
        $(this).addClass('is-active');

        $('.menu__item').each(function () {

            const itemCategory = $(this).data('category');

            const shouldShow =
                selectedCategory === 'all' ||
                selectedCategory === itemCategory;

            $(this).toggleClass('is-hidden', !shouldShow);

        });

    });


    /* =========================
       FORM STATUS
    ========================= */

    function showFormStatus($form, message, type) {

        const $status = $form.find('.form-status');

        if (!$status.length) {
            return;
        }

        $status
            .removeClass('is-success is-error')
            .addClass(
                type === 'success'
                    ? 'is-success'
                    : 'is-error'
            )
            .text(message);

    }


    function clearFormStatus($form) {

        $form
            .find('.form-status')
            .removeClass('is-success is-error')
            .text('');

    }


    function validateForm(formElement, $form, errorMessage) {

        if (formElement.checkValidity()) {
            return true;
        }

        formElement.reportValidity();

        showFormStatus(
            $form,
            errorMessage,
            'error'
        );

        return false;

    }


    /* =========================
       BOOKING FORM
    ========================= */

    $('.booking__form').on('submit', function (event) {

        event.preventDefault();

        const formElement = this;
        const $form = $(formElement);

        const isValid = validateForm(
            formElement,
            $form,
            'Please fill in all booking fields.'
        );

        if (!isValid) {
            return;
        }

        const bookingData = {
            name: $form.find('[name="name"]').val().trim(),
            email: $form.find('[name="email"]').val().trim(),
            phone: $form.find('[name="phone"]').val().trim(),
            people: $form.find('[name="people"]').val(),
            date: $form.find('[name="date"]').val(),
            time: $form.find('[name="time"]').val()
        };

        console.log('Booking data:', bookingData);

        showFormStatus(
            $form,
            'Your table request has been received.',
            'success'
        );

        formElement.reset();

    });


    /* =========================
       CONTACT FORM
    ========================= */

    $('.contact__form').on('submit', function (event) {

        event.preventDefault();

        const formElement = this;
        const $form = $(formElement);

        const isValid = validateForm(
            formElement,
            $form,
            'Please fill in your name, email and message.'
        );

        if (!isValid) {
            return;
        }

        const contactData = {
            name: $form.find('[name="name"]').val().trim(),
            email: $form.find('[name="email"]').val().trim(),
            phone: $form.find('[name="phone"]').val().trim(),
            message: $form.find('[name="message"]').val().trim()
        };

        console.log('Contact data:', contactData);

        showFormStatus(
            $form,
            'Thank you. Your message has been sent.',
            'success'
        );

        formElement.reset();

    });


    /* =========================
       CLEAR FORM MESSAGES
    ========================= */

    $('.booking__form, .contact__form').on(
        'input change',
        function () {
            clearFormStatus($(this));
        }
    );

});