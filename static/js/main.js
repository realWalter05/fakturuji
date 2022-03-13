$("#dodavatel_get_data").click(function(){
    var text = $("#dodavatel").val();

    $.ajax({
      url: '/get_ico_data',
      type: "get",
      data: {jsdata: text},
      datatype: "json",
      contentType : 'application/json',
      success: function(response) {
        fill_ico_data("dodavatel", JSON.parse(response));
      },
      error: function(xhr) {
        console.log(xhr);
      }
    });
});

$("#odberatel_get_data").click(function(){
    var text = $("#odberatel").val();

    $.ajax({
      url: '/get_ico_data',
      type: "get",
      data: {jsdata: text},
      datatype: "json",
      contentType : 'application/json',
      success: function(response) {
        fill_ico_data("odberatel", JSON.parse(response));
      },
      error: function(xhr) {
        console.log(xhr);
      }
    });
});

function fill_ico_data(title, data) {
  console.log("#"+title+"_rejstrik");
  document.querySelector("#"+title+"_street").value = data[1];
  document.querySelector("#"+title+"_city").value = data[2];
  document.querySelector("#"+title+"_country").value = data[3];
  document.querySelector("#"+title+"_ico").value = data[4];
  document.querySelector("#"+title+"_dic").value = data[5];
  document.querySelector("#"+title+"_rejstrik").value = data[6];
}
