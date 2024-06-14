function hideAlert() {
    const alerta = document.getElementById('custom-alert');
    alerta.classList.add('hide');
    setTimeout(hideAlert, 5000); // Ocultar después de n segundos (10000 ms)
}


