import React from 'react';import{createRoot}from'react-dom/client';import App from './App';
if(!localStorage.getItem('token'))fetch((import.meta.env.VITE_API_URL||'http://localhost:8000/api/v1')+'/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:'learner@aspireos.example.com',password:'ChangeMe123!'})}).then(r=>r.json()).then(x=>localStorage.setItem('token',x.access_token)).catch(()=>{});
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
