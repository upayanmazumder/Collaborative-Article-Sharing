import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyDgKhaEqjwzISMDZDJRgaly4nOw69pdXfs",
    authDomain: "cas-main-d320b.firebaseapp.com",
    projectId: "cas-main-d320b",
    storageBucket: "cas-main-d320b.firebasestorage.app",
    messagingSenderId: "379547223321",
    appId: "1:379547223321:web:103ef731cf8f72d3703188",
    measurementId: "G-Q0PX5SJ5JJ"
};

// Initialize Firebase App
const app = initializeApp(firebaseConfig);

// Export Auth
export const auth = getAuth(app);
