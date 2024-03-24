// Открытие и закрытие всплывающих окон
const loginButton = document.querySelector('.btn-login');
const registerButton = document.querySelector('.btn-register');
const loginPopup = document.querySelector('#login-popup');
const registerPopup = document.querySelector('#register-popup');
loginButton.addEventListener('click', function() {
	loginPopup.style.display = 'flex';
});
registerButton.addEventListener('click', function() {
	registerPopup.style.display = 'flex';
});
loginPopup.addEventListener('click', function(event) {
	if(event.target === loginPopup) {
		loginPopup.style.display = 'none';
	}
});
registerPopup.addEventListener('click', function(event) {
	if(event.target === registerPopup) {
		registerPopup.style.display = 'none';
	}
});