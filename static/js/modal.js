document.addEventListener('DOMContentLoaded', function() {
    profileModalShow();
});

function profileModalShow() {
    const profileModalElement = document.getElementById('profile');
    const bodyElement = document.body;

    if (profileModalElement.classList.contains('show')) {
        profileModalElement.style.display = 'block';
        profileModalElement.ariaModal = 'true'
        profileModalElement.role = 'dialog'
        bodyElement.classList.add('modal-open')
        bodyElement.style.overflow = 'hidden';
        bodyElement.style.paddingRight = '0';
    }


    document.addEventListener('click', function(event) {
        if (event.target.matches('[data-bs-dismiss="modal"]')) {
            profileModalElement.style.display = 'none';
            profileModalElement.setAttribute('aria-modal', 'false');
            bodyElement.classList.remove('modal-open');
            bodyElement.style.overflow = 'auto';
            bodyElement.style.paddingRight = '0';
        }
    });
}
