$('#carouselExample').carousel({
    interval: 2000
});


$(document).ready(function() {
    /* show lightbox when clicking a thumbnail */
    $('a.thumb').click(function(event) {
        event.preventDefault();
        var content = $('.modal-body');
        content.empty();
        var title = $(this).attr("title");
        $('.modal-title').html(title);
        content.html($(this).html());
        $(".modal-profile").modal({ show: true });
    });

});