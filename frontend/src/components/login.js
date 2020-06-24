import React, {useState, useEffect} from 'react';
import {Button, Input} from 'reactstrap'

import {loginUserAPI} from "../utilities/utils"
import { login, logout, leaveChat } from '../utilities/sockets';

const LoginForm = ({token, setToken, unsetToken}) => {

    const [mail, setMail] = useState(localStorage.getItem('mail'))
    const [error, setError] = useState(null)
    const [password, setPassword] = useState("")

    useEffect(() => {
      if(token){
        // if user has already logged in, try to login via socket into his room
        login(token)
      }
    }, [])

    const loginUser = async () => {
          let response = await loginUserAPI(mail, password)
          if(response.type == "success"){

                // if received token, hence the credentials were correct
                setToken(response.token)
                login(response.token)

                setError("")
                localStorage.setItem("mail", mail)

          }else{

                setError(response.error)

          }
        }



    const logoutUser =() => {

      // log user out of chat and remove his auth token from the localStorage
      logout(token)
      leaveChat(token)

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
