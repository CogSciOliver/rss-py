// live_preview.js
function linkInputToPreview(inputId, previewId) {
	// MUST CHNAGE TO CAPTURE CLASS OR ID OF THIS ACTIVE INPUTS AND PREVIEWS.
	const input = this.getElementById(inputId);
	// const input = document.getElementById(inputId);
	const preview = document.getElementById(previewId);
	if (input && preview) {
		input.addEventListener("input", () => {
			preview.textContent = input.value;
		});
	}
}

function initLivePreview(items) {
	items.forEach((item) => {
		Object.keys(item).forEach((field) => {
			const inputId = `${field}_input_${item.idx}`;
			const previewId = `${field}_preview_${item.idx}`;
			linkInputToPreview(inputId, previewId);
		});
	});
}
