import React, {useState, useEffect} from 'react';
import io from "socket.io-client"
import {Button} from "reactstrap"
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import LoginForm from './components/login'
import ChatRoom from './components/chat'
import NewsRoom from './components/news'


let endPoint = "http://localhost:3000"
let socket = io.connect(`${endPoint}`)
socket.on('connect', () => {
  socket.on('disconnected', () => {
    socket.emit('disconnect', localStorage.getItem('token'));
  })
});

const App = () => {

  const [error, setError] = useState("")

  

  const [token, setToken] = useState(localStorage.getItem('token'))
  
  const [message, setMessage] = useState("")
  const [receiver, setReceiver] = useState("")
  const [receipent, setReceipent] = useState("")

  

  

  const sendMessage = () => {
    socket.emit("message", receiver, message)
  }    

  const getReceipent = () => {
    return <select name="cars" id="cars">
    {receipent.map((singleReceipent) => {
      return <option value={singleReceipent}>{singleReceipent}</option>
    })}
    </select>
  }

  const storeToken = (token) => {
    setToken(token)
    localStorage.setItem("token", token)
    socket.emit("login", token)
    socket.emit("join_room", token, "chat")
  }

  const unsetToken = () => {
    setToken("")
    localStorage.removeItem("token")
  }

    return (
      <div className="App">
        <header className="App-header">
        <LoginForm token={token} socket={socket} setToken={storeToken} unsetToken={unsetToken}/>
        <ChatRoom token={token} socket={socket}/>
        <NewsRoom socket={socket}/>
        </header>
      </div>
    )
  }


export default App;

/**
  
 */