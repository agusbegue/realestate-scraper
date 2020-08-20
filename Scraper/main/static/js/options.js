function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var del_url;
var del_row;

//guardo el url y row a borrar en la window
$('#dataTable').on('click', '.btn-del', function () {
    console.log('entro');
    window.del_url = $(this).attr('data-url');
    window.del_row = $(this).parents('tr');
});

//confirmo y mando la request para borrar
$('.btn-ok').click(function(e) {
    console.log('clickie');
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : window.del_url,
        type : "POST",
        data : {csrfmiddlewaretoken: csrftoken},
        success : function(json) {
            $('#modal-confirm-delete').modal('hide');
            $('#dataTable').DataTable().row($(window.del_row)).remove().draw();
            console.log('borrado');
        },
        error : function() {
            console.log("error");
        }
    });
    return false;
});