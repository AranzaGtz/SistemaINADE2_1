(function(){


    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click',(e) => {
            const confirmacion = confirm('¿Seguro de eliminar al usuario?');
            if (!confirmacion){ 
                e.preventDefault();
            }
        })
    })

    const btnModificacion = document.querySelectorAll(".btnModificacion");

    btnModificacion.forEach(btn => {
        btn.addEventListener('click',(e) => {
            const confirmacion = confirm('¿Seguro de modificar al usuario?');
            if (!confirmacion){ 
                e.preventDefault();
            }
        })
    })

})();

