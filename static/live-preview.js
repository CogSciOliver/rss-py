// live-preview.js
document.addEventListener("DOMContentLoaded", function () {
	document.querySelectorAll("[id*='_input_']").forEach((input) => {
		input.addEventListener("input", function () {
			const preview = document.getElementById(this.id.replace("_input_", "_preview_"));

			if (preview) {
				preview.textContent = this.value;
			}
		});
	});
});
