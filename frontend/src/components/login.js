import React, {useState, useEffect} from 'react';
import {Button, Input} from 'reactstrap'


const LoginForm = ({token, setToken, unsetToken, socket}) => {

    const [mail, setMail] = useState(localStorage.getItem('mail'))
    const [error, setError] = useState(null)
    const [password, setPassword] = useState("")

    useEffect(() => {
      if(token){
        socket.emit("login", token)
        socket.emit("join_room", token)
      }
    }, [])

    const loginUser = () => {
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: mail, password: password})
      };
      fetch('http://localhost:3000/auth/login/', requestOptions)
          .then(response => response.json())
          .then(data => {

            if(data["code"] == 200){

              setToken(data["data"])
              setError("")
              localStorage.setItem("mail", mail)

              // When user logs in, automatically join the chat room at the same time
              socket.emit("login", data["data"])
              socket.emit("join_room", data["data"])
              
            }
            else
            {
              setError(data["message"])
            }
            
          });
        }

    const logoutUser =() => {

      socket.emit("leave_room", token)
      unsetToken()
      setMail("")
      localStorage.removeItem("mail")

    }

    const getLoginForm = () => {
        return (
        <div>
          {error}<br/>
          LOGIN TO SEE DIFFERENT CHANNELS!<br/>
          <Input type="text" placeholder="Enter email" onChange={e => setMail(e.target.value)}/>
        <Input type="password" placeholder="Enter password" onChange={e => setPassword(e.target.value)} style={{marginTop:"5px"}}/>
        <Button color="success" onClick={loginUser} style={{marginTop:"5px"}}>Login</Button>
        </div>
        )
      }
  
      const showLogout = () => {
        
        return (<div style={{marginTop: "50px"}}>
          Hello <b>{mail}</b><br/>
          <Button color="primary" style={{marginTop: "20px"}}onClick={logoutUser}>Logout</Button>
        </div>)
      }
    return (
        <div style={{height: "300px"}}>
        {
          token ? showLogout() : getLoginForm() 
        }
        </div>
    )
}

export default LoginForm

/**
<div style={{marginTop: "20px"}}>
        {
          token ? showLogout() : getLoginForm() 
        }
        </div>
 */