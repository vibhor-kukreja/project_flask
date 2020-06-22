import React, {useState, useEffect} from 'react'
import {Input, Button, Toast} from 'reactstrap'
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';  


const ChatApp = ({token, socket}) => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const toggle = () => setDropdownOpen(prevState => !prevState);
    const [receipent, setReceipent] = useState("")
    const [onlineUsers, setOnlineUsers] = useState([])
    const [messageText, setMessageText] = useState("")
    const [receivedMessages, setReceivedMessages] = useState([])

    useEffect(() => {
        // to run exactly once
        socket.on("user_joined", user => {
            let usersNow = getUser(user)
            setOnlineUsers(usersNow)
        })

        socket.on("user_left", user => {
            let usersNow = removeUser(user)
            setOnlineUsers(usersNow)
        })
      }, [onlineUsers.length])
    
    useEffect(() => {
        socket.on("message", msg => {
            setReceivedMessages([...receivedMessages, msg])
        })

    }, [receivedMessages.length])


    const removeUser = (user) => {
        let nowUsers = onlineUsers.filter((singleUser) => {
            return singleUser != user
        })
        return nowUsers
    }

    const getUser = (user) => {
        let nowUsers = onlineUsers.filter((singleUser) => {
            return singleUser!=user
        })
        nowUsers.push(user)
        return nowUsers
    }

    const sendMessage = () => {
        
        socket.emit("message", token, receipent, messageText)

        setMessageText(null)
    }

    const showReceivedMessages = () => {

        return <ul>
            {receivedMessages.map((singleMessage) => {
                return <li>{singleMessage}</li>
            })}
        </ul>

    }

    const showChatWindow = () => {
        return (
        <div>
            <Input type="text" placeholder="Send Text" onChange={e => setMessageText(e.target.value)} style={{margin: "5px"}}/>
            <Dropdown isOpen={dropdownOpen} toggle={toggle} style={{margin: "5px"}}>
            <DropdownToggle caret>
                {receipent ? receipent : "Choose Receipent"}
            </DropdownToggle>
            <DropdownMenu>
                {onlineUsers.map((user) => {
                    return <DropdownItem onClick={e => setReceipent(e.target.value)} value={user}>{user}</DropdownItem>
                })}
                
            </DropdownMenu>
            </Dropdown>
            <Button color="primary" onClick={sendMessage}>Send</Button>
        </div>)
    }
    
    return (
    
    <div>
        {token ? <p>SEND A HIE!</p> : <p>LOGIN TO CHAT</p>}
        {token ? showChatWindow() : null}
        {receivedMessages && receivedMessages.length > 0 ? showReceivedMessages(): null}
    </div>
    )
}

export default ChatApp

/**
 *<div style={{marginTop: "5px",display: "inline-block"}} >
          <Input type="text" placeholder="Send Text" onChange={e => setMessage(e.target.value)}/>
          <Input type="text" placeholder="Name" onChange={e => setReceiver(e.target.value)} style={{marginTop:"5px"}}/>
          <Button  color="danger" onClick={sendMessage} style={{marginTop:"5px"}}>Send</Button>
          </div>
          {receipent ? getReceipent(): null}
          
 */

 /**
  * Login -> token -> localStorage
  * connect -> with token -> connection with email
  * 
  */