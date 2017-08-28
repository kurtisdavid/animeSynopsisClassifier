
function fixHeight() {
    var winHeight = $(window).height();
    var titleH = $('#title').eq(0).outerHeight();
    var predH = $('#predictions').eq(0).outerHeight();
    var infoH = $('#info').eq(0).outerHeight();
    var formH = $('#form').eq(0).outerHeight();
    var headHeight = titleH + predH + infoH + formH + 10;

    if (winHeight<=headHeight) {
        $('#head').css('paddingTop', (headHeight-winHeight + 225) + 'px');
    }
    else if (winHeight-headHeight<200){
        console.log(winHeight);
        console.log(headHeight);

        $('#head').css('paddingTop', 225 + 'px');
    }
}

$(document).ready(function () {
    console.log('ready!');
    fixHeight();
});