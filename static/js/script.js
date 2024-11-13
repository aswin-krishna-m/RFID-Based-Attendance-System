//  alerts
function hideAlert(alert) {
    alert.classList.add('custom-alert-hide');
    setTimeout(function () {
        alert.style.display = 'none';
    }, 500); 
}

window.onload = function () {
    const alerts = document.querySelectorAll('.custom-alert');
    alerts.forEach(function (alert) {
        const closeBtn = alert.querySelector('.close-btn');
        closeBtn.addEventListener('click', function () {
            hideAlert(alert);
        });
        setTimeout(function () {
            hideAlert(alert);
        }, 5000);
    });
};
