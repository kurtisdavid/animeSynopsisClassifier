function gen_() {
  $.ajax({
   type: "POST",
   url: "/generate",
   async: true,
   success: fill
  });
}

function fill(link) {

  document.getElementById("anime").value = link;
  console.log(document.getElementById("anime"));
  document.getElementById("form").submit();

}

$(document).ajaxStart(function ()
{
    $('body').addClass('wait');

}).ajaxComplete(function () {

    $('body').removeClass('wait');

});