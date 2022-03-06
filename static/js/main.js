function SetToLS(name, data) {
    localStorage.setItem(name, data);
}

function FillInputsFromLS() {
    for (var i = 0; i < localStorage.length; i++){
        let itemId = localStorage.key(i)
        let itemValue = localStorage.getItem(localStorage.key(i));

        if (itemId == "seperator" || itemId == "mobile_keyboard" || itemId == "min_length_word" || itemId == "length") {
            document.getElementById(itemId).value = itemValue;
        } else {
            // Checkbox
            if (JSON.parse(itemValue)) {
                document.getElementById(itemId).checked = true;
            } else {
                document.getElementById(itemId).checked = false;
            }
        }
    }
}

function copyToClipboard(text) {
    const el = document.createElement('textarea');
    el.value = text;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}
