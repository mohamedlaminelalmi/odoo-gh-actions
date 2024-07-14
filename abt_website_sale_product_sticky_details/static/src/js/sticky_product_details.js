/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { cloneContentEls } from "@website/js/utils";

const AbtStickyProductDetails = publicWidget.Widget.extend({
    selector: ".sticky-product-details",
    events: {
        'click #sticky_add_to_cart': '_onClickAddCart',
        'click #sticky_buy_now': '_onClickAddCartByNow',
    },

    /**
     * @override
     */
    async start() {
        $('#wrapwrap').scroll(this._onPageScroll.bind(this));
        return this._super(...arguments);
    },

    _onPageScroll() {
        const stickyProductDetails = $(".sticky-product-details-content");
        const productDetailsOffset = $("#product_details").offset().top * 1.2;
        const footerOffset = $('footer').offset().top;
        const scrollTop = $(window).scrollTop();
        const windowHeight = $(window).height();

        if (scrollTop > productDetailsOffset) {
            stickyProductDetails.fadeIn(500, function() {
                if (footerOffset < windowHeight) {
                    stickyProductDetails.removeClass("fixed");
                    stickyProductDetails.addClass("sticky");
                } else {
                    stickyProductDetails.removeClass("sticky");
                    stickyProductDetails.addClass("fixed");
                }
            });
        } else {
            stickyProductDetails.fadeOut(300, function() {
                stickyProductDetails.removeClass("fixed");
                stickyProductDetails.removeClass("sticky");
            });
        }
    },

    _onClickAddCart(ev) {
        if($('body').hasClass('editor_enable')){
            e.stopPropagation();
        } else{
            $("div#product_details .js_product.js_main_product #add_to_cart").trigger("click");
            return false;
        }
    },

    _onClickAddCartByNow(ev) {
        if($('body').hasClass('editor_enable')){
            e.stopPropagation();
        } else{
            $("div#product_details .js_product.js_main_product .o_we_buy_now").trigger("click");
            return false;
        }
    }

});

publicWidget.registry.AbtStickyProductDetails = AbtStickyProductDetails;

export default AbtStickyProductDetails;
