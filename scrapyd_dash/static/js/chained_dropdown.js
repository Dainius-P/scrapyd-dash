/* CHAINED DROPDOWNS FOR ADDING TASKS */

$('#versionSelect').change(function (){
    var selectedProject = $('#projectSelect').val(); 
    var selectedVersion = $('#versionSelect').val(); 
    var selectedServer = $('#serverSelect').val(); 

    $('#spiderSelect').empty();

    $.ajax({
      url: "/api/v3/get_spiders/",
      dataType: "json",
      data: {
        'project': selectedProject,
        'server': selectedServer,
        'version': selectedVersion
      },
      success : function (resp){
        $("#spiderSelect").append('<option value="" disabled selected>Select Spider</option>');

        $.each(resp, function( index, value ) {
          var o = new Option(value, value);
          $(o).html(value);
          $("#spiderSelect").append(o);
        });
      }
    });
});

$('#projectSelect').change(function (){
    var selectedProject = $('#projectSelect').val(); 

    $('#versionSelect').empty();
    $('#spiderSelect').empty();

    $.ajax({
      url: "/api/v3/get_versions/",
      dataType: "json",
      data: {
        'project': selectedProject
      },
      success : function (resp){
        $("#versionSelect").append('<option value="" disabled selected>Select Version</option>');
        $("#versionSelect").append('<option value="" name="version">Latest</option>');
        $.each(resp, function( index, value ) {
          var o = new Option(value['name'], value['name']);
          $(o).html(value['name']);
          $("#versionSelect").append(o);
        });
      }
    });
});


$('#serverSelect').change(function (){
    var selectedServer = $('#serverSelect').val(); 

    $('#projectSelect').empty();
    $('#versionSelect').empty();
    $('#spiderSelect').empty();

    $.ajax({
      url: "/api/v3/get_projects/",
      dataType: "json",
      data: {
        'server': selectedServer
      },
      success : function (resp) {
        $("#projectSelect").append('<option value="" disabled selected>Select Project</option>');
        $.each(resp, function( index, value ) {
          var o = new Option(value['pk'], value['pk']);

          $(o).html(value['name']);
          $("#projectSelect").append(o);
        });
      }
    });
});