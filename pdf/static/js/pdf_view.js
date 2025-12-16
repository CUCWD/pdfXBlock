/* Javascript for pdfXBlock. */
function pdfXBlockInitView(runtime, element, initArgs) {
    /* Weird behaviour :
     * In the LMS, element is the DOM container.
     * In the CMS, element is the jQuery object associated*
     * So here I make sure element is the jQuery object */
    if (element.innerHTML) {
        element = $(element);
    }

    // Defaults (grab from initArgs if provided)
    // completionCondition: "viewing_delay" | "scroll_bottom" | "last_page"
    // completionDelayMs: number (milliseconds)
    const completionCondition =
        (initArgs && initArgs.completionCondition) || "viewing_delay";
    const completionDelayMs =
        (initArgs && initArgs.completionDelayMs) || 5000;

    let hasMarked = false;
    let viewingTimerId = null;

    function handlerUrl(name) {
        return runtime.handlerUrl(element, name);
    }

    function markCompleted() {
        if (hasMarked) return;
        hasMarked = true;

        $.ajax({
            type: "POST",
            url: handlerUrl("mark_completed"),
            data: JSON.stringify({}),
            contentType: "application/json",
        }).fail(function () {
            // Best effort; optionally allow retry
            hasMarked = false;
        });
    }

    function clearViewingTimer() {
        if (viewingTimerId) {
        window.clearTimeout(viewingTimerId);
        viewingTimerId = null;
        }
    }

    // ---- Visibility gate (matches "completion by viewing" semantics) ----
    // Calls callbackOnVisible when element is at least 50% visible in viewport
    // Calls callbackOnNotVisible when element is less than 50% visible in viewport (if provided)
    // Uses IntersectionObserver if available, otherwise treats as always visible
    // Cleans up on unload
    // Based on https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
    // and https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API/Using_the_Intersection_Observer_API
    // and https://stackoverflow.com/questions/51188531/check-if-element-is-visible-in-viewport-with-intersectionobserver
    function whenVisible(callbackOnVisible, callbackOnNotVisible) {
        const target = element[0];
        if (!target) {
            // If we can't observe, treat as visible
            callbackOnVisible();
            return;
        }

        if (!("IntersectionObserver" in window)) {
            // Fallback: treat as visible
            callbackOnVisible();
            return;
        }

        const observer = new IntersectionObserver(
            function (entries) {
                const entry = entries[0];
                const visible = entry.isIntersecting && entry.intersectionRatio >= 0.5; // >=50% visible

                if (visible) {
                callbackOnVisible();
                } else if (callbackOnNotVisible) {
                callbackOnNotVisible();
                }
            },
            { threshold: [0.5] }
        );

        observer.observe(target);

        // Clean up
        $(window).on("unload", function () {
            clearViewingTimer();
            observer.disconnect();
        });
    }


    // ---- Condition: last_page ----
    function initLastPageCompletion() {
        // This works only if you're using PDF.js
        // Not implemented yet
    }

    // ---- Condition: scroll_bottom ----
    function initScrollBottomCompletion() {
        // This works only if you're using PDF.js
        // Not implemented yet
    }

    // ---- Condition: viewing_delay ----
    function initViewingDelayCompletion() {
        function startTimer() {
        if (hasMarked) return;
        if (viewingTimerId) return;

        viewingTimerId = window.setTimeout(function () {
            viewingTimerId = null;
            markCompleted();
        }, completionDelayMs);
        }

        whenVisible(startTimer, clearViewingTimer);
    }

    $(function () {
        element.find('.pdf-download-button').on('click', function () {
            $.post(handlerUrl("on_download"), '{}');
        });

        // Completion behavior
        switch (completionCondition) {
            case "viewing_delay":
                initViewingDelayCompletion();
                break;
            // case "scroll_bottom":
                // Need PDF.js integration to view scroll position
                // Not reliably implementable with pdf_view.js <object> unless you render the PDF in a scrollable container you control (typically https://github.com/mozilla/pdf.js)
                // initScrollBottomCompletion();
                // break;
            // case "last_page":
                // Need PDF.js integration to view current page
                // Essentially requires https://github.com/mozilla/pdf.js (or another JS PDF renderer that exposes page events)
                // initLastPageCompletion();
                // break;
            default:
                // Unknown value -> safest default
                initViewingDelayCompletion();
        }
    });
}
