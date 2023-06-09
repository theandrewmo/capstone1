import { ref, uploadBytesResumable, getDownloadURL } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-storage.js";
import storage from './firebase-init.js'

export function uploadImage(event) {
    const file = event.target.files[0]; // Get the uploaded file

    const storageRef = ref(storage);
    const fileRef = ref(storage, file.name);
    const uploadTask = uploadBytesResumable(fileRef, file);

    // Create references for relevant elements 
    const photo_url = document.getElementById('photo_url');
    const saveReview = document.getElementById('save-review');
    const uploadStatus = document.getElementById('upload-status');
    const uploadProgressBar = document.getElementById('upload-progress-bar');
    const uploadProgressContainer = document.getElementById('upload-progress-container');

    uploadTask.on('state_changed', (snapshot) => {
        // Observe state change events such as progress, pause, and resume
        // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
        saveReview.disabled = true;
        uploadStatus.innerText = 'Uploading image...';
        const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        uploadProgressContainer.classList.remove('d-none');
        uploadProgressBar.style.width = progress + '%';
        uploadStatus.innerText = 'Uploading: ' + Math.round(progress) + '%';
        
        switch (snapshot.state) {
            case 'paused':
                console.log('Upload is paused');
                break;

            case 'running':
                console.log('Upload is running');
                break;
        }
    },
    (error) => {
        console.error('error')
    },
    ()=> getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
        photo_url.value = downloadURL;
        saveReview.disabled = false;
        uploadStatus.innerText = 'Image uploaded successfully.';
    }))
}

const fileInput = document.getElementById('photo_file');
if (fileInput) {fileInput.addEventListener('change', uploadImage)}
