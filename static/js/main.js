
function GetFirmaData(parent) {
  console.log(parent);
  let text = parent.querySelector(".form-nazev").value;

  $.ajax({
    url: '/get_ico_data',
    type: "get",
    data: {jsdata: text},
    datatype: "json",
    contentType : 'application/json',
    success: function(response) {
      fill_data(JSON.parse(response), parent);
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });   
}

function GetDataFromId(id, parent, je_dodavatel) {
  $.ajax({
    url: '/get_data_from_id',
    type: "get",
    data: {id: id},
    datatype: "json",
    contentType : 'application/json',
    success: function(response) {
      console.log(je_dodavatel);
      if (je_dodavatel)
        document.getElementById("dodavatel_id").value = id;
      else 
        document.getElementById("odberatel_id").value = id;
      
      fill_data(JSON.parse(response), parent, je_dodavatel);
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });
}

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


function GetHintFirmy(text, parent, je_dodavatel, je_odberatel) {
  $.ajax({
    url: '/get_user_firmy_names',
    type: "get",
    data: {search_text: text, je_dodavatel: je_dodavatel, je_odberatel: je_odberatel},
    datatype: "json",
    contentType : 'application/json',
    success: function(response) {
      HintFirma(JSON.parse(response), parent, je_dodavatel);
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });
}


function HintFirma(firmy, parent, je_dodavatel) {
  let hints = parent.querySelectorAll(".hint-element");
  if (hints) {
    hints.forEach(function DeleteIt(hint) {
      hint.remove();
    });
  }

  let hintMenu = parent.querySelector("#hint-menu");
  firmy.forEach(function AddToHintTable(value) {
    let a = document.createElement("a");
    a.classList.add("dropdown-item");
    a.classList.add("hint-element");
    a.setAttribute("onclick", 'GetDataFromId('+value["id"]+', this.parentElement.parentElement.parentElement, '+je_dodavatel+');'); 
    a.textContent = value["nazev"];
    hintMenu.appendChild(a);
  });
}

function fill_data(data, parent, je_dodavatel) {
  if (parent.querySelector("#warning")) {
    // Deleting error message if there
    parent.querySelector("#warning").remove()
  }  
  console.log(data);
  if (!data) {
    let status = document.createElement("div");
    status.classList.add("text-danger");
    status.setAttribute("id", "warning");
    status.innerText = "Data nebyla nalezena."

    parent.appendChild(status);
  } else {  
    parent.querySelector(".form-nazev").value = data[0];
    parent.querySelector(".form-ico").value = data[1];
    parent.querySelector(".form-dic").value = data[2];    
    parent.querySelector(".form-street").value = data[3];
    parent.querySelector(".form-cislo-popisne").value = data[4];
    parent.querySelector(".form-psc").value = data[5];
    parent.querySelector(".form-city").value = data[6];
    parent.querySelector(".form-country").value = data[7];
    parent.querySelector(".form-rejstrik").value = data[8];
    parent.querySelector(".form-vlozka").value = data[9];
    parent.querySelector(".form-telefon").value = data[10];
    parent.querySelector(".form-email").value = data[11];
    parent.querySelector(".form-web").value = data[12];

    // Fill out bank data if its dodavatel
    if (je_dodavatel) {
      document.querySelector("input[name='account_number']").value = data[13];
      document.querySelector("input[name='bank_number']").value = data[14];
      document.querySelector("input[name='iban']").value = data[15];
      document.querySelector("input[name='swift']").value = data[16];
      document.querySelector("input[name='konst_cislo']").value = data[17];
      document.querySelector("input[name='var_cislo']").value = data[18];     
    }
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
  row.appendChild(CreateItemCol("text", "form-control", "currency", "Měna"));

  let polozka_item = document.createElement("div");
  
  // Append children
  polozka_item.appendChild(row);

  container.appendChild(polozka_item)
}

function SetDropdownAresTest(output_id, input_data) {
  document.getElementById(output_id).innerText = "Dovyplnit \"" + input_data.value + "\"";
}
