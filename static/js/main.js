$("#dodavatel_get_data").click(function(){
    var text = $("#dodavatel_").val();

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
    var text = $("#odberatel_").val();

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

function set_date(id, plus_days) {
  var now = new Date();
  var day = ("0" + now.getDate()).slice(-2);
  var month = ("0" + (now.getMonth() + 1)).slice(-2);
  var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
  
  $('#'+id).val(today);
}

set_date("splatnost_date")
set_date("zdanpl_date")
set_date("vystaveni_date")

function fill_ico_data(title, data) {
  if (document.querySelector("#warning_"+title)) {
    // Deleting error message if there
    document.querySelector("#warning_"+title).remove()
  }  
  if (!data) {
    let status = document.createElement("div");
    status.classList.add("text-danger");
    status.setAttribute("id", "warning_"+title);
    status.innerText = "Data nebyla nalezena."

    document.querySelector("#"+title+"_col").appendChild(status);
  } else {  
    document.querySelector("#"+title+"_street").value = data[1];
    document.querySelector("#"+title+"_city").value = data[2];
    document.querySelector("#"+title+"_country").value = data[3];
    document.querySelector("#"+title+"_ico").value = data[4];
    document.querySelector("#"+title+"_dic").value = data[5];
    document.querySelector("#"+title+"_rejstrik").value = data[6];
  }
}

function CreateItemCol(type, class_text, name, placeholder) {
  let input = document.createElement("input");
  input.classList.add(class_text);
  input.type = type;
  input.name = name;
  input.placeholder = placeholder;

  let col = document.createElement("div");
  col.classList.add("col");
  col.appendChild(input);

  return col    
}

function CreateItem() {
  let container = document.getElementById("polozky");
  
  let row = document.createElement("div");
  row.classList.add("row");
  row.appendChild(CreateItemCol("text", "form-control", "polozka", "Dodávka"));
  row.appendChild(CreateItemCol("number", "form-control", "dph", "DPH"));
  row.appendChild(CreateItemCol("number", "form-control", "count", "Počet"));
  row.appendChild(CreateItemCol("number", "form-control", "price", "Cena"));

  let polozka_item = document.createElement("div");
  
  // Append children
  polozka_item.appendChild(row);

  container.appendChild(polozka_item)
}

function SetDropdownAresTest(output_id, input_data) {
  document.getElementById(output_id).innerText = "Dovyplnit \"" + input_data.value + "\"";

}

var http = require('http');

function startKeepAlive() {
    setInterval(function() {
        var options = {
            host: 'fakturujto.herokuapp.com',
            port: 80,
            path: '/'
        };
        http.get(options, function(res) {
            res.on('data', function(chunk) {
                try {
                    // optional logging... disable after it's working
                    console.log("HEROKU RESPONSE: " + chunk);
                } catch (err) {
                    console.log(err.message);
                }
            });
        }).on('error', function(err) {
            console.log("Error: " + err.message);
        });
    }, 20 * 60 * 1000); // load every 20 minutes
}

startKeepAlive();
