const toastController = () => {
    let options = {
        delay: 5000
    };
    let toastElementsList = [].slice.call(document.querySelectorAll('.toast'));
    for (const toast of toastElementsList) {
        toast.addEventListener('hidden.bs.toast', () => {
            if (toast) {
                toast.parentNode.removeChild(toast);
            }
        });
    }
    let toastsList = toastElementsList.map((toastElement) => {
        return new bootstrap.Toast(toastElement, options);
    });
    for (const toast of toastsList) {
        toast.show();
    }
};

window.onload = () => {
    document.querySelector('.navbar-toggler').addEventListener('click', () => {
        document.querySelector('.my-navbar-toggler-icon').classList.toggle('change');
    });
    feather.replace();
    toastController();
};