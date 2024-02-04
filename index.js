const WEB_SOCKET_URL = '0.0.0.0'
const WEB_SOCKET_PORT = 8081

console.log('from console Hello world!')

const ws = new WebSocket(`ws://${WEB_SOCKET_URL}:${WEB_SOCKET_PORT}`);

const textField = document.getElementById('textField');
const checkBox = document.getElementById('checkBox');
const additionalInfoText = document.getElementById('additionalInfoText');
const checkboxes = document.querySelector('.checkboxes');
const submitButton = document.querySelector('button[type="submit"]');
const subscribe = document.getElementById('subscribe');

formChat.addEventListener('submit', (e) => {
    e.preventDefault();

    let message;
    if (checkBox.checked) {
        const selectedCurrencies = Array.from(document.querySelectorAll('.checkboxes input:checked')).map(checkbox => checkbox.value);
        const selectedDays = document.getElementById('selectedDays').innerText;
        message = `exchange ${selectedDays} ${selectedCurrencies.join()}`;
    } else {
        input = textField.value.trim()
        if (!input) return alert("Please enter a message");
        message = textField.value.trim()
        // message = `Me: ${textField.value.trim()}`;
    }

    const elMsg = document.createElement('div');
    elMsg.innerHTML = `Me: ${message}`;
    console.log(`Me: ${message}`);
    subscribe.appendChild(elMsg);
    ws.send(message);

    textField.value = '';
});

checkBox.addEventListener('change', () => {
    if (!additionalInfoText) {
        additionalInfoText = document.createElement('span');
        document.querySelector('div').appendChild(additionalInfoText);
    }

    if (checkBox.checked) {
        textField.style.display = 'none';
        checkboxes.style.display = 'block';
        additionalInfoText.innerHTML = 'Additional information needed';
    } else {
        textField.style.display = 'block';
        checkboxes.style.display = 'none';
        additionalInfoText.innerHTML = '';
    }
    validateForm();
});

document.querySelectorAll('.checkboxes input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', validateForm);
});

function validateForm() {
    const selectedCurrencies = Array.from(document.querySelectorAll('.checkboxes input:checked')).length > 0;
    const isTextFieldValid = !checkBox.checked || (textField.value.trim() !== '');
    const isValid = checkBox.checked ? selectedCurrencies : isTextFieldValid;

    submitButton.disabled = !isValid;
    if (checkBox.checked) {
        additionalInfoText.innerHTML = !isValid ? 'Additional information needed' : '';
    }
}

ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}

ws.onmessage = (e) => {
    console.log(e.data)
    const text = e.data

    const elMsg = document.createElement('div')
    elMsg.innerHTML = text
    subscribe.appendChild(elMsg)
}

function showDate(value) {
    document.getElementById("selectedDays").innerText = value;
    validateForm();
}


