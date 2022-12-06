

function ShowFakturaPreview(faktura_id, element) {
	document.querySelector("#upravit-fakturu-btn").setAttribute("href", "upravit_fakturu?id="+faktura_id);
	if (document.querySelector("#sablona-fakturu-btn")) {
		document.querySelector("#sablona-fakturu-btn").setAttribute("href", "z_faktury_sablonu?id="+faktura_id);
	}

	previous = document.querySelector(".bg-light");
	if (previous) {
		previous.classList.remove("bg-light");
	}
	element.classList.add("bg-light");
	$.ajax({
		url: '/get_faktura_html',
		type: "get",
		data: {id: faktura_id},
		datatype: "text",
		contentType : 'application/json',
		success: function(content) {
			document.getElementById("faktura_preview").innerHTML= content;
		},
		error: function(xhr) {
			console.log(xhr);
		}});
}

function ModifySablonaButton(faktura_id) {
	document.querySelector("#fakturuj-sablonu-btn").setAttribute("href", "fakturuj_sablonu?id="+faktura_id);
}

function PrintFaktura(faktura_id) {
	$.ajax({
		url: '/get_faktura_html',
		type: "get",
		data: {id: faktura_id},
		datatype: "text",
		contentType : 'application/json',
		success: function(content) {
			var myWindow = window.open('','','width=1200,height=600');
			myWindow.document.write(content);

			myWindow.document.close();
			myWindow.print();
			myWindow.onafterprint = function(){
				myWindow.close();
		 }
		},
		error: function(xhr) {
			console.log(xhr);
		}
	});
}


function GetDalsiFaktury(from, to) {
	$.ajax({
		url: '/get_dalsi_faktury',
		type: "get",
		data: {from: from, to: to},
		datatype: "text",
		contentType : 'application/json',
		success: function(faktury) {
			faktury_obj = JSON.parse(faktury);
			console.log(faktury_obj);
			console.log(faktury_obj[0]);

			const fakturyTable = document.querySelector("#faktury-table");
			for (let faktura in faktury_obj) {
				let container = document.createElement("tr");
				container.setAttribute("onclick", "ShowFakturaPreview("+ faktury_obj[faktura]["id"] + ", this);")

				// Excel collumn
				let excelTr = document.createElement("td");
				excelTr.setAttribute("class", "table-icon");

				let excelA = document.createElement("a");
				excelA.setAttribute("href", "/get_faktura?id="+faktury_obj[faktura]["id"])
				excelA.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" fill="#FFF" stroke-miterlimit="10" stroke-width="2"> <path stroke="#979593" d="M67.1716,7H27c-1.1046,0-2,0.8954-2,2v78 c0,1.1046,0.8954,2,2,2h58c1.1046,0,2-0.8954,2-2V26.8284c0-0.5304-0.2107-1.0391-0.5858-1.4142L68.5858,7.5858 C68.2107,7.2107,67.702,7,67.1716,7z"/> <path fill="none" stroke="#979593" d="M67,7v18c0,1.1046,0.8954,2,2,2h18"/> <path fill="#C8C6C4" d="M51 61H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 60.5523 51.5523 61 51 61zM51 55H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 54.5523 51.5523 55 51 55zM51 49H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 48.5523 51.5523 49 51 49zM51 43H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 42.5523 51.5523 43 51 43zM51 67H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 66.5523 51.5523 67 51 67zM79 61H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 60.5523 79.5523 61 79 61zM79 67H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 66.5523 79.5523 67 79 67zM79 55H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 54.5523 79.5523 55 79 55zM79 49H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 48.5523 79.5523 49 79 49zM79 43H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 42.5523 79.5523 43 79 43zM65 61H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 60.5523 65.5523 61 65 61zM65 67H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 66.5523 65.5523 67 65 67zM65 55H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 54.5523 65.5523 55 65 55zM65 49H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 48.5523 65.5523 49 65 49zM65 43H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 42.5523 65.5523 43 65 43z"/> <path fill="#107C41" d="M12,74h32c2.2091,0,4-1.7909,4-4V38c0-2.2091-1.7909-4-4-4H12c-2.2091,0-4,1.7909-4,4v32 C8,72.2091,9.7909,74,12,74z"/> <path d="M16.9492,66l7.8848-12.0337L17.6123,42h5.8115l3.9424,7.6486c0.3623,0.7252,0.6113,1.2668,0.7471,1.6236 h0.0508c0.2617-0.58,0.5332-1.1436,0.8164-1.69L33.1943,42h5.335l-7.4082,11.9L38.7168,66H33.041l-4.5537-8.4017 c-0.1924-0.3116-0.374-0.6858-0.5439-1.1215H27.876c-0.0791,0.2684-0.2549,0.631-0.5264,1.0878L22.6592,66H16.9492z"/> </svg>';

				excelTr.appendChild(excelA);
				container.appendChild(excelTr);

				// PDF collumn
				let pdfTr = document.createElement("td");
				pdfTr.setAttribute("class", "table-icon");

				let pdfA = document.createElement("a");
				pdfA.setAttribute("href", "/get_faktura_pdf?id="+faktury_obj[faktura]["id"]);
				pdfA.innerHTML = '<?xml version="1.0" encoding="iso-8859-1"?><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 303.188 303.188" style="enable-background:new 0 0 303.188 303.188;" xml:space="preserve"> <g> <polygon style="fill:#E8E8E8;" points="219.821,0 32.842,0 32.842,303.188 270.346,303.188 270.346,50.525 	"/> <path style="fill:#FB3449;" d="M230.013,149.935c-3.643-6.493-16.231-8.533-22.006-9.451c-4.552-0.724-9.199-0.94-13.803-0.936 c-3.615-0.024-7.177,0.154-10.693,0.354c-1.296,0.087-2.579,0.199-3.861,0.31c-1.314-1.36-2.584-2.765-3.813-4.202 c-7.82-9.257-14.134-19.755-19.279-30.664c1.366-5.271,2.459-10.772,3.119-16.485c1.205-10.427,1.619-22.31-2.288-32.251 c-1.349-3.431-4.946-7.608-9.096-5.528c-4.771,2.392-6.113,9.169-6.502,13.973c-0.313,3.883-0.094,7.776,0.558,11.594 c0.664,3.844,1.733,7.494,2.897,11.139c1.086,3.342,2.283,6.658,3.588,9.943c-0.828,2.586-1.707,5.127-2.63,7.603 c-2.152,5.643-4.479,11.004-6.717,16.161c-1.18,2.557-2.335,5.06-3.465,7.507c-3.576,7.855-7.458,15.566-11.815,23.02 c-10.163,3.585-19.283,7.741-26.857,12.625c-4.063,2.625-7.652,5.476-10.641,8.603c-2.822,2.952-5.69,6.783-5.941,11.024 c-0.141,2.394,0.807,4.717,2.768,6.137c2.697,2.015,6.271,1.881,9.4,1.225c10.25-2.15,18.121-10.961,24.824-18.387 c4.617-5.115,9.872-11.61,15.369-19.465c0.012-0.018,0.024-0.036,0.037-0.054c9.428-2.923,19.689-5.391,30.579-7.205 c4.975-0.825,10.082-1.5,15.291-1.974c3.663,3.431,7.621,6.555,11.939,9.164c3.363,2.069,6.94,3.816,10.684,5.119 c3.786,1.237,7.595,2.247,11.528,2.886c1.986,0.284,4.017,0.413,6.092,0.335c4.631-0.175,11.278-1.951,11.714-7.57 C231.127,152.765,230.756,151.257,230.013,149.935z M119.144,160.245c-2.169,3.36-4.261,6.382-6.232,9.041 c-4.827,6.568-10.34,14.369-18.322,17.286c-1.516,0.554-3.512,1.126-5.616,1.002c-1.874-0.11-3.722-0.937-3.637-3.065 c0.042-1.114,0.587-2.535,1.423-3.931c0.915-1.531,2.048-2.935,3.275-4.226c2.629-2.762,5.953-5.439,9.777-7.918 c5.865-3.805,12.867-7.23,20.672-10.286C120.035,158.858,119.587,159.564,119.144,160.245z M146.366,75.985 c-0.602-3.514-0.693-7.077-0.323-10.503c0.184-1.713,0.533-3.385,1.038-4.952c0.428-1.33,1.352-4.576,2.826-4.993 c2.43-0.688,3.177,4.529,3.452,6.005c1.566,8.396,0.186,17.733-1.693,25.969c-0.299,1.31-0.632,2.599-0.973,3.883 c-0.582-1.601-1.137-3.207-1.648-4.821C147.945,83.048,146.939,79.482,146.366,75.985z M163.049,142.265 c-9.13,1.48-17.815,3.419-25.979,5.708c0.983-0.275,5.475-8.788,6.477-10.555c4.721-8.315,8.583-17.042,11.358-26.197 c4.9,9.691,10.847,18.962,18.153,27.214c0.673,0.749,1.357,1.489,2.053,2.22C171.017,141.096,166.988,141.633,163.049,142.265z M224.793,153.959c-0.334,1.805-4.189,2.837-5.988,3.121c-5.316,0.836-10.94,0.167-16.028-1.542 c-3.491-1.172-6.858-2.768-10.057-4.688c-3.18-1.921-6.155-4.181-8.936-6.673c3.429-0.206,6.9-0.341,10.388-0.275 c3.488,0.035,7.003,0.211,10.475,0.664c6.511,0.726,13.807,2.961,18.932,7.186C224.588,152.585,224.91,153.321,224.793,153.959z"/> <polygon style="fill:#FB3449;" points="227.64,25.263 32.842,25.263 32.842,0 219.821,0 	"/> <g> <path style="fill:#A4A9AD;" d="M126.841,241.152c0,5.361-1.58,9.501-4.742,12.421c-3.162,2.921-7.652,4.381-13.472,4.381h-3.643 v15.917H92.022v-47.979h16.606c6.06,0,10.611,1.324,13.652,3.971C125.321,232.51,126.841,236.273,126.841,241.152z M104.985,247.387h2.363c1.947,0,3.495-0.546,4.644-1.641c1.149-1.094,1.723-2.604,1.723-4.529c0-3.238-1.794-4.857-5.382-4.857 h-3.348C104.985,236.36,104.985,247.387,104.985,247.387z"/> <path style="fill:#A4A9AD;" d="M175.215,248.864c0,8.007-2.205,14.177-6.613,18.509s-10.606,6.498-18.591,6.498h-15.523v-47.979 h16.606c7.701,0,13.646,1.969,17.836,5.907C173.119,235.737,175.215,241.426,175.215,248.864z M161.76,249.324 c0-4.398-0.87-7.657-2.609-9.78c-1.739-2.122-4.381-3.183-7.926-3.183h-3.773v26.877h2.888c3.939,0,6.826-1.143,8.664-3.43 C160.841,257.523,161.76,254.028,161.76,249.324z"/> <path style="fill:#A4A9AD;" d="M196.579,273.871h-12.766v-47.979h28.355v10.403h-15.589v9.156h14.374v10.403h-14.374 L196.579,273.871L196.579,273.871z"/> </g> <polygon style="fill:#D1D3D3;" points="219.821,50.525 270.346,50.525 219.821,0 	"/> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> </svg>';

				pdfTr.appendChild(pdfA);
				container.appendChild(pdfTr);

				// Print collumn
				let printTr = document.createElement("td");
				printTr.setAttribute("class", "table-icon");
				printTr.setAttribute("onclick", "PrintFaktura("+faktury_obj[faktura]["id"]+");");
				printTr.innerHTML = '<svg version="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" enable-background="new 0 0 48 48"> <rect x="9" y="11" fill="#424242" width="30" height="3"/> <path fill="#616161" d="M4,25h40v-7c0-2.2-1.8-4-4-4H8c-2.2,0-4,1.8-4,4V25z"/> <path fill="#424242" d="M8,36h32c2.2,0,4-1.8,4-4v-8H4v8C4,34.2,5.8,36,8,36z"/> <circle fill="#00E676" cx="40" cy="18" r="1"/> <rect x="11" y="4" fill="#90CAF9" width="26" height="10"/> <path fill="#242424" d="M37.5,31h-27C9.7,31,9,30.3,9,29.5v0c0-0.8,0.7-1.5,1.5-1.5h27c0.8,0,1.5,0.7,1.5,1.5v0 C39,30.3,38.3,31,37.5,31z"/> <rect x="11" y="31" fill="#90CAF9" width="26" height="11"/> <rect x="11" y="29" fill="#42A5F5" width="26" height="2"/> <g fill="#1976D2"> <rect x="16" y="33" width="17" height="2"/> <rect x="16" y="37" width="13" height="2"/> </g> </svg>';
				container.appendChild(printTr);

				// Content collumns
				let cislotr = document.createElement("td");
				cislotr.innerText = faktury_obj[faktura]["cislo_faktury"]
				container.appendChild(cislotr);

				let dodavatelTr = document.createElement("td");
				dodavatelTr.innerText = faktury_obj[faktura]["dodavatel"]
				container.appendChild(dodavatelTr);

				let odberatelTr = document.createElement("td");
				odberatelTr.innerText = faktury_obj[faktura]["odberatel"]
				container.appendChild(odberatelTr);

				let datumVystaveniTr = document.createElement("td");
				datumVystaveniTr.innerText = faktury_obj[faktura]["datum_vystaveni"]
				container.appendChild(datumVystaveniTr);
				fakturyTable.appendChild(container);

				// Trash collumn
				let trashTr = document.createElement("td");
				trashTr.setAttribute("class", "faktury-trash-icon");
				trashTr.setAttribute("onclick", "PrintFaktura("+faktury_obj[faktura]["id"]+");");
				trashTr.innerHTML = '<svg version="1.1" style="width: 20px; height: 20px;" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="482.428px" height="482.429px" viewBox="0 0 482.428 482.429" style="enable-background:new 0 0 482.428 482.429;" xml:space="preserve"> <g> <g> <path d="M381.163,57.799h-75.094C302.323,25.316,274.686,0,241.214,0c-33.471,0-61.104,25.315-64.85,57.799h-75.098 c-30.39,0-55.111,24.728-55.111,55.117v2.828c0,23.223,14.46,43.1,34.83,51.199v260.369c0,30.39,24.724,55.117,55.112,55.117 h210.236c30.389,0,55.111-24.729,55.111-55.117V166.944c20.369-8.1,34.83-27.977,34.83-51.199v-2.828 C436.274,82.527,411.551,57.799,381.163,57.799z M241.214,26.139c19.037,0,34.927,13.645,38.443,31.66h-76.879 C206.293,39.783,222.184,26.139,241.214,26.139z M375.305,427.312c0,15.978-13,28.979-28.973,28.979H136.096 c-15.973,0-28.973-13.002-28.973-28.979V170.861h268.182V427.312z M410.135,115.744c0,15.978-13,28.979-28.973,28.979H101.266 c-15.973,0-28.973-13.001-28.973-28.979v-2.828c0-15.978,13-28.979,28.973-28.979h279.897c15.973,0,28.973,13.001,28.973,28.979 V115.744z"/> <path d="M171.144,422.863c7.218,0,13.069-5.853,13.069-13.068V262.641c0-7.216-5.852-13.07-13.069-13.07 c-7.217,0-13.069,5.854-13.069,13.07v147.154C158.074,417.012,163.926,422.863,171.144,422.863z"/> <path d="M241.214,422.863c7.218,0,13.07-5.853,13.07-13.068V262.641c0-7.216-5.854-13.07-13.07-13.07 c-7.217,0-13.069,5.854-13.069,13.07v147.154C228.145,417.012,233.996,422.863,241.214,422.863z"/> <path d="M311.284,422.863c7.217,0,13.068-5.853,13.068-13.068V262.641c0-7.216-5.852-13.07-13.068-13.07 c-7.219,0-13.07,5.854-13.07,13.07v147.154C298.213,417.012,304.067,422.863,311.284,422.863z"/> </g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> </svg>';
				container.appendChild(trashTr);
			}

			document.querySelector("#get-dalsi-faktury-btn").setAttribute('GetDalsiFaktury('+from + 5+','+ to + 5+')');
		},
		error: function(xhr) {
			console.log(xhr);
		}
	});
}


function GetDalsiSablony(from, to) {
	$.ajax({
		url: '/get_dalsi_sablony',
		type: "get",
		data: {from: from, to: to},
		datatype: "text",
		contentType : 'application/json',
		success: function(faktury) {
			console.log(faktury);
			faktury_obj = JSON.parse(faktury);
			console.log(faktury_obj);
			console.log(faktury_obj[0]);

			const fakturyTable = document.querySelector("#faktury-table");
			for (let faktura in faktury_obj) {
				let container = document.createElement("tr");
				container.setAttribute("onclick", "ShowFakturaPreview("+ faktury_obj[faktura]["id"] + ", this); ModifySablonaButton("+faktury_obj[faktura]["id"]+");")

				// Excel collumn
				let excelTr = document.createElement("td");
				excelTr.setAttribute("class", "table-icon");

				let excelA = document.createElement("a");
				excelA.setAttribute("href", "/get_faktura?id="+faktury_obj[faktura]["id"])
				excelA.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" fill="#FFF" stroke-miterlimit="10" stroke-width="2"> <path stroke="#979593" d="M67.1716,7H27c-1.1046,0-2,0.8954-2,2v78 c0,1.1046,0.8954,2,2,2h58c1.1046,0,2-0.8954,2-2V26.8284c0-0.5304-0.2107-1.0391-0.5858-1.4142L68.5858,7.5858 C68.2107,7.2107,67.702,7,67.1716,7z"/> <path fill="none" stroke="#979593" d="M67,7v18c0,1.1046,0.8954,2,2,2h18"/> <path fill="#C8C6C4" d="M51 61H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 60.5523 51.5523 61 51 61zM51 55H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 54.5523 51.5523 55 51 55zM51 49H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 48.5523 51.5523 49 51 49zM51 43H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 42.5523 51.5523 43 51 43zM51 67H41v-2h10c.5523 0 1 .4477 1 1l0 0C52 66.5523 51.5523 67 51 67zM79 61H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 60.5523 79.5523 61 79 61zM79 67H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 66.5523 79.5523 67 79 67zM79 55H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 54.5523 79.5523 55 79 55zM79 49H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 48.5523 79.5523 49 79 49zM79 43H69c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C80 42.5523 79.5523 43 79 43zM65 61H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 60.5523 65.5523 61 65 61zM65 67H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 66.5523 65.5523 67 65 67zM65 55H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 54.5523 65.5523 55 65 55zM65 49H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 48.5523 65.5523 49 65 49zM65 43H55c-.5523 0-1-.4477-1-1l0 0c0-.5523.4477-1 1-1h10c.5523 0 1 .4477 1 1l0 0C66 42.5523 65.5523 43 65 43z"/> <path fill="#107C41" d="M12,74h32c2.2091,0,4-1.7909,4-4V38c0-2.2091-1.7909-4-4-4H12c-2.2091,0-4,1.7909-4,4v32 C8,72.2091,9.7909,74,12,74z"/> <path d="M16.9492,66l7.8848-12.0337L17.6123,42h5.8115l3.9424,7.6486c0.3623,0.7252,0.6113,1.2668,0.7471,1.6236 h0.0508c0.2617-0.58,0.5332-1.1436,0.8164-1.69L33.1943,42h5.335l-7.4082,11.9L38.7168,66H33.041l-4.5537-8.4017 c-0.1924-0.3116-0.374-0.6858-0.5439-1.1215H27.876c-0.0791,0.2684-0.2549,0.631-0.5264,1.0878L22.6592,66H16.9492z"/> </svg>';

				excelTr.appendChild(excelA);
				container.appendChild(excelTr);

				// PDF collumn
				let pdfTr = document.createElement("td");
				pdfTr.setAttribute("class", "table-icon");

				let pdfA = document.createElement("a");
				pdfA.setAttribute("href", "/get_faktura_pdf?id="+faktury_obj[faktura]["id"]);
				pdfA.innerHTML = '<?xml version="1.0" encoding="iso-8859-1"?><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 303.188 303.188" style="enable-background:new 0 0 303.188 303.188;" xml:space="preserve"> <g> <polygon style="fill:#E8E8E8;" points="219.821,0 32.842,0 32.842,303.188 270.346,303.188 270.346,50.525 	"/> <path style="fill:#FB3449;" d="M230.013,149.935c-3.643-6.493-16.231-8.533-22.006-9.451c-4.552-0.724-9.199-0.94-13.803-0.936 c-3.615-0.024-7.177,0.154-10.693,0.354c-1.296,0.087-2.579,0.199-3.861,0.31c-1.314-1.36-2.584-2.765-3.813-4.202 c-7.82-9.257-14.134-19.755-19.279-30.664c1.366-5.271,2.459-10.772,3.119-16.485c1.205-10.427,1.619-22.31-2.288-32.251 c-1.349-3.431-4.946-7.608-9.096-5.528c-4.771,2.392-6.113,9.169-6.502,13.973c-0.313,3.883-0.094,7.776,0.558,11.594 c0.664,3.844,1.733,7.494,2.897,11.139c1.086,3.342,2.283,6.658,3.588,9.943c-0.828,2.586-1.707,5.127-2.63,7.603 c-2.152,5.643-4.479,11.004-6.717,16.161c-1.18,2.557-2.335,5.06-3.465,7.507c-3.576,7.855-7.458,15.566-11.815,23.02 c-10.163,3.585-19.283,7.741-26.857,12.625c-4.063,2.625-7.652,5.476-10.641,8.603c-2.822,2.952-5.69,6.783-5.941,11.024 c-0.141,2.394,0.807,4.717,2.768,6.137c2.697,2.015,6.271,1.881,9.4,1.225c10.25-2.15,18.121-10.961,24.824-18.387 c4.617-5.115,9.872-11.61,15.369-19.465c0.012-0.018,0.024-0.036,0.037-0.054c9.428-2.923,19.689-5.391,30.579-7.205 c4.975-0.825,10.082-1.5,15.291-1.974c3.663,3.431,7.621,6.555,11.939,9.164c3.363,2.069,6.94,3.816,10.684,5.119 c3.786,1.237,7.595,2.247,11.528,2.886c1.986,0.284,4.017,0.413,6.092,0.335c4.631-0.175,11.278-1.951,11.714-7.57 C231.127,152.765,230.756,151.257,230.013,149.935z M119.144,160.245c-2.169,3.36-4.261,6.382-6.232,9.041 c-4.827,6.568-10.34,14.369-18.322,17.286c-1.516,0.554-3.512,1.126-5.616,1.002c-1.874-0.11-3.722-0.937-3.637-3.065 c0.042-1.114,0.587-2.535,1.423-3.931c0.915-1.531,2.048-2.935,3.275-4.226c2.629-2.762,5.953-5.439,9.777-7.918 c5.865-3.805,12.867-7.23,20.672-10.286C120.035,158.858,119.587,159.564,119.144,160.245z M146.366,75.985 c-0.602-3.514-0.693-7.077-0.323-10.503c0.184-1.713,0.533-3.385,1.038-4.952c0.428-1.33,1.352-4.576,2.826-4.993 c2.43-0.688,3.177,4.529,3.452,6.005c1.566,8.396,0.186,17.733-1.693,25.969c-0.299,1.31-0.632,2.599-0.973,3.883 c-0.582-1.601-1.137-3.207-1.648-4.821C147.945,83.048,146.939,79.482,146.366,75.985z M163.049,142.265 c-9.13,1.48-17.815,3.419-25.979,5.708c0.983-0.275,5.475-8.788,6.477-10.555c4.721-8.315,8.583-17.042,11.358-26.197 c4.9,9.691,10.847,18.962,18.153,27.214c0.673,0.749,1.357,1.489,2.053,2.22C171.017,141.096,166.988,141.633,163.049,142.265z M224.793,153.959c-0.334,1.805-4.189,2.837-5.988,3.121c-5.316,0.836-10.94,0.167-16.028-1.542 c-3.491-1.172-6.858-2.768-10.057-4.688c-3.18-1.921-6.155-4.181-8.936-6.673c3.429-0.206,6.9-0.341,10.388-0.275 c3.488,0.035,7.003,0.211,10.475,0.664c6.511,0.726,13.807,2.961,18.932,7.186C224.588,152.585,224.91,153.321,224.793,153.959z"/> <polygon style="fill:#FB3449;" points="227.64,25.263 32.842,25.263 32.842,0 219.821,0 	"/> <g> <path style="fill:#A4A9AD;" d="M126.841,241.152c0,5.361-1.58,9.501-4.742,12.421c-3.162,2.921-7.652,4.381-13.472,4.381h-3.643 v15.917H92.022v-47.979h16.606c6.06,0,10.611,1.324,13.652,3.971C125.321,232.51,126.841,236.273,126.841,241.152z M104.985,247.387h2.363c1.947,0,3.495-0.546,4.644-1.641c1.149-1.094,1.723-2.604,1.723-4.529c0-3.238-1.794-4.857-5.382-4.857 h-3.348C104.985,236.36,104.985,247.387,104.985,247.387z"/> <path style="fill:#A4A9AD;" d="M175.215,248.864c0,8.007-2.205,14.177-6.613,18.509s-10.606,6.498-18.591,6.498h-15.523v-47.979 h16.606c7.701,0,13.646,1.969,17.836,5.907C173.119,235.737,175.215,241.426,175.215,248.864z M161.76,249.324 c0-4.398-0.87-7.657-2.609-9.78c-1.739-2.122-4.381-3.183-7.926-3.183h-3.773v26.877h2.888c3.939,0,6.826-1.143,8.664-3.43 C160.841,257.523,161.76,254.028,161.76,249.324z"/> <path style="fill:#A4A9AD;" d="M196.579,273.871h-12.766v-47.979h28.355v10.403h-15.589v9.156h14.374v10.403h-14.374 L196.579,273.871L196.579,273.871z"/> </g> <polygon style="fill:#D1D3D3;" points="219.821,50.525 270.346,50.525 219.821,0 	"/> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> </svg>';

				pdfTr.appendChild(pdfA);
				container.appendChild(pdfTr);

				// Print collumn
				let printTr = document.createElement("td");
				printTr.setAttribute("class", "table-icon");
				printTr.setAttribute("onclick", "PrintFaktura("+faktury_obj[faktura]["id"]+");");
				printTr.innerHTML = '<svg version="1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" enable-background="new 0 0 48 48"> <rect x="9" y="11" fill="#424242" width="30" height="3"/> <path fill="#616161" d="M4,25h40v-7c0-2.2-1.8-4-4-4H8c-2.2,0-4,1.8-4,4V25z"/> <path fill="#424242" d="M8,36h32c2.2,0,4-1.8,4-4v-8H4v8C4,34.2,5.8,36,8,36z"/> <circle fill="#00E676" cx="40" cy="18" r="1"/> <rect x="11" y="4" fill="#90CAF9" width="26" height="10"/> <path fill="#242424" d="M37.5,31h-27C9.7,31,9,30.3,9,29.5v0c0-0.8,0.7-1.5,1.5-1.5h27c0.8,0,1.5,0.7,1.5,1.5v0 C39,30.3,38.3,31,37.5,31z"/> <rect x="11" y="31" fill="#90CAF9" width="26" height="11"/> <rect x="11" y="29" fill="#42A5F5" width="26" height="2"/> <g fill="#1976D2"> <rect x="16" y="33" width="17" height="2"/> <rect x="16" y="37" width="13" height="2"/> </g> </svg>';
				container.appendChild(printTr);

				// Content collumns
				let cislotr = document.createElement("td");
				cislotr.innerText = faktury_obj[faktura]["nazev"]
				container.appendChild(cislotr);

				let dodavatelTr = document.createElement("td");
				dodavatelTr.innerText = faktury_obj[faktura]["cislo_faktury"]
				container.appendChild(dodavatelTr);

				let odberatelTr = document.createElement("td");
				odberatelTr.innerText = faktury_obj[faktura]["dodavatel"]
				container.appendChild(odberatelTr);

				let datumVystaveniTr = document.createElement("td");
				datumVystaveniTr.innerText = faktury_obj[faktura]["odberatel"]
				container.appendChild(datumVystaveniTr);
				fakturyTable.appendChild(container);

				// Trash collumn
				let trashTr = document.createElement("td");
				trashTr.setAttribute("class", "faktury-trash-icon");
				trashTr.setAttribute("onclick", "PrintFaktura("+faktury_obj[faktura]["id"]+");");
				trashTr.innerHTML = '<svg version="1.1" style="width: 20px; height: 20px;" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="482.428px" height="482.429px" viewBox="0 0 482.428 482.429" style="enable-background:new 0 0 482.428 482.429;" xml:space="preserve"> <g> <g> <path d="M381.163,57.799h-75.094C302.323,25.316,274.686,0,241.214,0c-33.471,0-61.104,25.315-64.85,57.799h-75.098 c-30.39,0-55.111,24.728-55.111,55.117v2.828c0,23.223,14.46,43.1,34.83,51.199v260.369c0,30.39,24.724,55.117,55.112,55.117 h210.236c30.389,0,55.111-24.729,55.111-55.117V166.944c20.369-8.1,34.83-27.977,34.83-51.199v-2.828 C436.274,82.527,411.551,57.799,381.163,57.799z M241.214,26.139c19.037,0,34.927,13.645,38.443,31.66h-76.879 C206.293,39.783,222.184,26.139,241.214,26.139z M375.305,427.312c0,15.978-13,28.979-28.973,28.979H136.096 c-15.973,0-28.973-13.002-28.973-28.979V170.861h268.182V427.312z M410.135,115.744c0,15.978-13,28.979-28.973,28.979H101.266 c-15.973,0-28.973-13.001-28.973-28.979v-2.828c0-15.978,13-28.979,28.973-28.979h279.897c15.973,0,28.973,13.001,28.973,28.979 V115.744z"/> <path d="M171.144,422.863c7.218,0,13.069-5.853,13.069-13.068V262.641c0-7.216-5.852-13.07-13.069-13.07 c-7.217,0-13.069,5.854-13.069,13.07v147.154C158.074,417.012,163.926,422.863,171.144,422.863z"/> <path d="M241.214,422.863c7.218,0,13.07-5.853,13.07-13.068V262.641c0-7.216-5.854-13.07-13.07-13.07 c-7.217,0-13.069,5.854-13.069,13.07v147.154C228.145,417.012,233.996,422.863,241.214,422.863z"/> <path d="M311.284,422.863c7.217,0,13.068-5.853,13.068-13.068V262.641c0-7.216-5.852-13.07-13.068-13.07 c-7.219,0-13.07,5.854-13.07,13.07v147.154C298.213,417.012,304.067,422.863,311.284,422.863z"/> </g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> </svg>';
				container.appendChild(trashTr);
			}

			document.querySelector("#get-dalsi-faktury-btn").setAttribute('GetDalsiFaktury('+from + 5+','+ to + 5+')');
		},
		error: function(xhr) {
			console.log(xhr);
		}
	});
}


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

function GetPopisky(text, parent) {
	$.ajax({
		url: '/get_popisky',
		type: "get",
		data: {search_text: text},
		datatype: "json",
		contentType : 'application/json',
		success: function(response) {
			HintPopisek(JSON.parse(response), parent);
		},
		error: function(xhr) {
			console.log(xhr);
		}
	});
}

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


function SetPopisek(value) {
	document.querySelector('input[name=\"description\"]').value = value["popisek"];
	document.querySelector('input[name=\"description_id\"]').value = value["id"];
}


function HintPopisek(popisky, parent) {
	let hints = parent.querySelectorAll(".hint-element");
	if (hints) {
		hints.forEach(function DeleteIt(hint) {
			hint.remove();
		});
	}

	let hintMenu = parent.querySelector("#hint-menu");
	popisky.forEach(function AddToHintTable(value) {
		let a = document.createElement("a");
		a.classList.add("dropdown-item");
		a.classList.add("hint-element");
		a.setAttribute("onclick", SetPopisek(value));
		a.textContent = value["nazev"];
		hintMenu.appendChild(a);
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


function DeleteAccountDataDoubleCheck(element) {
	if (element.innerText == "Určitě si přejete smazat všechna data? Kliknutě znovu pro smazání") {
		window.location.href = "/delete_everything";
	} else {
		element.innerText = "Určitě si přejete smazat všechna data? Kliknutě znovu pro smazání"
	}
}