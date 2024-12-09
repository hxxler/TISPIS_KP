const uploadContainer = document.querySelector('#upload-container');
const fileInput = document.querySelector('#id_content');
const descriptionInput = document.querySelector('#id_description');
const uploadError = document.querySelector('#upload-error');
const uploadedPhotos = [];

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    event.target.classList.add('highlight');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    event.target.classList.remove('highlight');
    const files = event.dataTransfer.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();
        if (file.size <= 4 * 1024 * 1024 && !isDuplicate(file) && uploadedPhotos.length < 4) {
            reader.onload = function (event) {
                const img = document.createElement('img');
                img.src = event.target.result;
                const uploadItem = document.createElement('div');
                uploadItem.classList.add('upload-item');
                uploadItem.appendChild(img);
                const deleteIcon = document.createElement('div');
                deleteIcon.classList.add('delete-icon');
                deleteIcon.textContent = 'x';
                uploadItem.appendChild(deleteIcon);
                uploadContainer.appendChild(uploadItem);
                hideError();
            }
            reader.readAsDataURL(file);
        } else {
            showError('Ошибка загрузки файла');
        }
    }
}

fileInput.addEventListener('change', function (event) {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();
        if (file.size <= 4 * 1024 * 1024 && !isDuplicate(file) && uploadedPhotos.length < 4) {
            reader.onload = function (event) {
                const img = document.createElement('img');
                img.src = event.target.result;
                const uploadItem = document.createElement('div');
                uploadItem.classList.add('upload-item');
                uploadItem.appendChild(img);
                const deleteIcon = document.createElement('div');
                deleteIcon.classList.add('delete-icon');
                deleteIcon.textContent = 'x';
                uploadItem.appendChild(deleteIcon);
                uploadedPhotos.push(file);
                uploadContainer.appendChild(uploadItem);
                hideError();
            }
            reader.readAsDataURL(file);
        } else {
            showError('Ошибка загрузки файла');
        }
    }
});

uploadContainer.addEventListener('dragover', handleDragOver);
uploadContainer.addEventListener('drop', handleDrop);
uploadContainer.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-icon')) {
        const uploadItem = event.target.parentNode;
        const index = Array.from(uploadContainer.children).indexOf(uploadItem);
        uploadedPhotos.splice(index, 1);
        uploadItem.parentNode.removeChild(uploadItem);
    }
});

function isDuplicate(file) {
    return uploadedPhotos.some(uploadedFile => (
        uploadedFile.name === file.name &&
        uploadedFile.size === file.size &&
        uploadedFile.type === file.type
    ));
}

function showError(message) {
    uploadError.textContent = message;
    uploadError.style.display = 'block';
}

function hideError() {
    uploadError.textContent = '';
    uploadError.style.display = 'none';
}

descriptionInput.addEventListener('focus', function () {
    if (!descriptionInput.classList.contains('input-filled')) {
        descriptionInput.value = '';
        descriptionInput.classList.add('input-filled');
    }
});