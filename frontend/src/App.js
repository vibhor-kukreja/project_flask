import React, {useState, useEffect} from 'react';
import io from "socket.io-client"

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import LoginForm from './components/login'
import ChatRoom from './components/chat'
import NewsRoom from './components/news'
import { BACKEND_URL } from './utilities/constants';


// to establish socket connection
let endPoint = BACKEND_URL 
export let socket = io.connect(`${endPoint}`)
socket.on('connect', () => {
  socket.on('disconnected', () => {
    socket.emit('disconnect', localStorage.getItem('token'));
  })
});

const App = () => {


  const [token, setToken] = useState(localStorage.getItem('token'))

  const storeToken = (token) => {
    setToken(token)
    localStorage.setItem("token", token)
  }

  const unsetToken = () => {
    setToken("")
    localStorage.removeItem("token")
  }


    return (
      <div className="App">
        <header className="App-header">
        <LoginForm token={token} socket={socket} setToken={storeToken} unsetToken={unsetToken}/>
        <ChatRoom token={token} socket={socket} setToken={storeToken} unsetToken={unsetToken}/>
        <NewsRoom socket={socket}/>
        </header>
      </div>
    )
  }


export default App;
