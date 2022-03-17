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
  let container = document.getElementById("first_col_inputs");
  
  let row = document.createElement("div");
  row.classList.add("row");
  row.appendChild(CreateItemCol("number", "form-control", "count", "Počet"));
  row.appendChild(CreateItemCol("number", "form-control", "price", "Cena"));

  let rowSecond = document.createElement("div");
  rowSecond.classList.add("row");
  rowSecond.appendChild(CreateItemCol("text", "form-control", "polozka", "Položka"));
  rowSecond.appendChild(CreateItemCol("number", "form-control", "dph", "DPH"));

  // Append children
  container.appendChild(rowSecond);
  container.appendChild(row);
}
