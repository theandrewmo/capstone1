   // Import the functions you need from the SDKs you need
   import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
   import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-analytics.js";
   import { getStorage, ref, uploadBytesResumable, getDownloadURL } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-storage.js";

   // TODO: Add SDKs for Firebase products that you want to use
   // https://firebase.google.com/docs/web/setup#available-libraries
   
   // Your web app's Firebase configuration
   // For Firebase JS SDK v7.20.0 and later, measurementId is optional
   const firebaseConfig = {
       apiKey: "AIzaSyBLbabHzOjBIa3SmtZjcpqQCh_jDfXYUHo",
       authDomain: "brewery-image-project.firebaseapp.com",
       projectId: "brewery-image-project",
       storageBucket: "brewery-image-project.appspot.com",
       messagingSenderId: "477972949446",
       appId: "1:477972949446:web:ac24143affd19295ceaac7",
       measurementId: "G-GC8R07X9R8"
   };
   
   // Initialize Firebase
   const app = initializeApp(firebaseConfig);
   const analytics = getAnalytics(app);

   window.uploadImage = function (event) {
       const file = event.target.files[0]; // Get the uploaded file

       // Create a storage reference and upload the file
       const storage = getStorage();
       const storageRef = ref(storage);
       const fileRef = ref(storage, file.name);
       const uploadTask = uploadBytesResumable(fileRef, file);

       // Create references for relevant elements 
       const photo_url = document.getElementById('photo_url');
       const saveReview = document.getElementById('saveReview');
       const uploadStatus = document.getElementById('uploadStatus');
       const uploadProgressBar = document.getElementById('uploadProgressBar');
       const uploadProgressContainer = document.getElementById('uploadProgressContainer');


       uploadTask.on('state_changed', (snapshot) => {
           // Observe state change events such as progress, pause, and resume
           // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
           saveReview.disabled = true;
           uploadStatus.innerText = 'Uploading image...';
           const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
           uploadProgressContainer.style.display = '';
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