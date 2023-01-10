(function($) {
    /**
     *
     * @param el
     * @returns {boolean}
     * @link https://stackoverflow.com/questions/123999/how-can-i-tell-if-a-dom-element-is-visible-in-the-current-viewport
     */
    function isInView(el) {
        const box = el.getBoundingClientRect();
        return box.top < window.innerHeight && box.bottom >= 0;
    }

    let scrollData = {
        break: false,
        in_progress: false
    };

    function lazyLoaderScroll() {
        if (scrollData.in_progress) {
            scrollData.break = true;
        }

        let $lazyElements = $('.lazy-spotify-loader');
        $lazyElements.each(function(index, element) {
            if (scrollData.break) {
                scrollData.break = false;
                scrollData.in_progress = false;
                return;
            }

            scrollData.in_progress = true;

            let $element = $(element);
            if (isInView(element.parentElement)) {
                if ($element.attr('data-spotify-embed') != null) {
                    let embed = $element.attr('data-spotify-embed');
                    embed = atob(embed);
                    $element.html(embed);
                    $element.removeAttr('data-spotify-embed');
                }

                $element.show();
            }
            else {
                $element.hide();
            }
        });

        scrollData.in_progress = false
    }

    $(window).scroll(lazyLoaderScroll);
    $(lazyLoaderScroll);

})(jQuery);