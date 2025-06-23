import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
 apiKey: "AIzaSyCKfkeH3FSWPMztu518Np1JiMcf7T7Rvwk",
  authDomain: "fsd-task-tracker-app.firebaseapp.com",
  projectId: "fsd-task-tracker-app",
  storageBucket: "fsd-task-tracker-app.firebasestorage.app",
  messagingSenderId: "218670803195",
  appId: "1:218670803195:web:f263c83a7cf3fb790de85e",
  measurementId: "G-YQ1HLDQFZY"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);