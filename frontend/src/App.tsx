import {useState} from 'react';import {Shell} from './components/Shell';import {Dashboard} from './pages/Dashboard';import './style.css';
export default function App(){const [tab,setTab]=useState('Overview');return <Shell tab={tab} setTab={setTab}><Dashboard tab={tab}/></Shell>}
