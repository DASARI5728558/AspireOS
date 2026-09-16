const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
export type Content = {id:number;title:string;abstract:string;canonical_url:string;topics:string[];resource_type:string;licence:string};
export type Gap = {skill:string;current:number;target:number;gap:number;confidence:number};
export async function login(email:string,password:string){const r=await fetch(`${BASE}/auth/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});if(!r.ok)throw new Error('Login failed');return r.json()}
export async function api<T>(path:string):Promise<T>{const token=localStorage.getItem('token');const r=await fetch(`${BASE}${path}`,{headers:{Authorization:`Bearer ${token}`}});if(!r.ok)throw new Error(`Request failed: ${r.status}`);return r.json()}
