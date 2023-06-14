   import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
   import { getStorage } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-storage.js";

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
   const storage = getStorage(app);

   export default storage;