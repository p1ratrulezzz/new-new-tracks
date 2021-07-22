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

    function lazyLoaderScroll() {
        let $lazyElements = $('.lazy-spotify-loader');
        $lazyElements.each(function(index, element) {
            if (isInView(element)) {
                let $element = $(element);
                $element.removeClass('lazy-spotify-loader');
                let embed = $element.attr('data-spotify-embed');
                embed = atob(embed);
                $element.html(embed);
                $element.removeAttr('data-spotify-embed');
            }
            else {
                return;
            }
        });
    }

    $(window).scroll(lazyLoaderScroll);
    $(lazyLoaderScroll);

})(jQuery);