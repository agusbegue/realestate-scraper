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

//guardo el url con el *_id
$('.btn-del').click(function(e){
    console.log('entro');
    var url = $(e.target).attr('data-url');
    $('.btn-ok').data('url', url);
    var index = e.target.parentNode.parentNode.rowIndex;
    $('.btn-ok').data('index', index);
});
$('.btn-info').click(function(e) {
    console.log('hola');
});
//mando la request para borrar
$('.btn-ok').click(function(e) {
    console.log('clickie');
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : $(e.target).data('url'),
        type : "POST",
        data : {csrfmiddlewaretoken: csrftoken},
        success : function(json) {
            $('#modal-confirm-delete').modal('hide');
            document.getElementById("dataTable").deleteRow($(e.target).data('index'));
        },
        error : function() {
            console.log("error");
        }
    });
    return false;
});