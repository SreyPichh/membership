$(function () {

  /* Functions */

  var loadForm = function (e) {
    console.log("load form");
    e.preventDefault();
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        console.log("HEYYYYY beforeSend")
        $("#modal-acc").modal("show");
      },
      success: function (data) {
        $("#modal-acc .modal-content").html(data.html_form);
      },
      error: function(error){
        console.log("ERRORRR");
        console.log(error);
      }
    });
  };

  var saveForm = function (e) {
    e.preventDefault();
    var self = $(this);
    var form = $(self).get(0);
    var fromData = new FormData(form);
    var csrfmiddlewaretoken = $("meta[name='csrfmiddlewaretoken']").attr("content");
    fromData.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
    console.log(fromData.get("image"));
    var record_dom_id = $(self).attr('data-record-id');
    console.log($(self).attr("action"), $(self).attr("method"), record_dom_id, csrfmiddlewaretoken)
    $.ajax({
      url: $(self).attr("action"),
      data: fromData,
      type: $(self).attr("method"),
      dataType: 'json',
      processData: false,
      contentType: false,
      enctype: 'multipart/form-data',
      success: function (data) {
        var result = JSON.parse(JSON.stringify(data))
        if (result.form_is_valid) {
          // Remove deleted record from DOM
          if(result.action == 'delete'){
            $("#" + record_dom_id).remove();
          } else if(result.action == 'create') {

            $('#accommodation-tboby').append(result.saved_record);
          } else if(result.action == 'update') {
            $('#' + record_dom_id).replaceWith(result.updated_record);
          }

          $("#modal-acc").modal("hide");
        }
        // else {
        //   $("#modal-acc .modal-content").html(result.html_form);
        // }
      }
    });
    return false;
  };

  /* Binding */

  // Create accommodation
  $(".js-create-acc").click(loadForm);
  $("#modal-acc").on("submit", ".js-acc-create-form", saveForm);

  // Update accommodation
  $("#acc-table").on("click", ".js-update-acc", loadForm);
  $("#modal-acc").on("submit", ".js-accommodation-update-form", saveForm);

  // Delete accommodation
  $("#acc-table").on("click", ".js-delete-accommodation", loadForm);
  $("#modal-acc").on("submit", ".js-accommodation-delete-form", saveForm);

  // Pagination Clicks
  
});


