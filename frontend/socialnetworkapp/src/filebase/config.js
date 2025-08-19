// import firebase from "firebase/app";
// import "firebase/analytics";
// import "firebase/auth";
// import "firebase/firestore";

// const firebaseConfig = {
//   apiKey:  process.env.REACT_APP_API_KEY,
//   authDomain: "psychologicalsocialnetwork.firebaseapp.com",
//   projectId: "psychologicalsocialnetwork",
//   storageBucket: "psychologicalsocialnetwork.firebasestorage.app",
//   messagingSenderId: process.env.REACT_APP_MESS_SEND_ID,
//   appId: process.env.REACT_APP_APP_ID
// };

// // Initialize Firebase
// firebase.initializeApp(firebaseConfig);
// firebase.analytics();

// const auth = firebase.auth();
// const db = firebase.firestore();

// if (window.location.hostname === 'localhost') {
//   // auth.useEmulator('http://localhost:9099');
//   // db.useEmulator('localhost', '8080');
// }

// export { db, auth };
// export default firebase;


import { getApp, getApps, initializeApp } from "firebase/app";
import { getAuth, connectAuthEmulator } from "firebase/auth";
import { getFirestore, connectFirestoreEmulator } from "firebase/firestore";
import { getAnalytics, isSupported } from "firebase/analytics";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_API_KEY,
  authDomain: "psychologicalsocialnetwork.firebaseapp.com",
  projectId: "psychologicalsocialnetwork",
  storageBucket: "psychologicalsocialnetwork.appspot.com",
  messagingSenderId: process.env.REACT_APP_MESS_SEND_ID,
  appId: process.env.REACT_APP_APP_ID
};

// Initialize Firebase.. Chỉ khởi tạo 1 lần duy nhất
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

let analytics;
isSupported().then((ok) => {
  if (ok) analytics = getAnalytics(app);
});

const auth = getAuth(app);
const db = getFirestore(app);

if (window.location.hostname === "localhost") {
//   connectAuthEmulator(auth, "http://localhost:9099");
//   connectFirestoreEmulator(db, "localhost", 8080);
}

export { db, auth, analytics };
export default app;
