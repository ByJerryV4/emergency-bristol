function showPopup(message = "Form submitted successfully!") {
  const popup = document.getElementById('popup');
  if (!popup) return;
  popup.textContent = message;
  popup.style.display = 'block';
  setTimeout(() => popup.style.display = 'none', 4000);
}