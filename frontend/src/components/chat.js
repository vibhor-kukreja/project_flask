import React, {useState, useEffect} from 'react'
import {Input, Button, Toast} from 'reactstrap'
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';  
import { getUsersAPI, validateMessage } from '../utilities/utils';
import { joinChat, sendMessage } from '../utilities/sockets';
import {socket} from '../App'


const ChatApp = ({token, unsetToken}) => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const toggle = () => setDropdownOpen(prevState => !prevState);

    const [receipent, setReceipent] = useState(null)
    const [onlineUsers, setOnlineUsers] = useState([])
    const [messageText, setMessageText] = useState("")
    const [receivedMessages, setReceivedMessages] = useState([])

    useEffect(() => {

        // if token exists, meaning user has logged in, hence get the user's friends from DB
        showUsers()
        joinChat(token)
          
    }, [token])

    useEffect(() => {

        // Whenever socket receives a new message, append it to the existing list of messages
        socket.on("new-message", msg => {
            setReceivedMessages([...receivedMessages, msg])
        })


    }, [receivedMessages.length])

    const showUsers = async () => {

        if(token){
            // get the users from DB, based on current logged in user
        let getUsersResponse = await getUsersAPI(token)
        if(getUsersResponse.code == 200){
            // if received users, display
            let users = JSON.parse(getUsersResponse["users"])
            // when token exists, join chat        
            setOnlineUsers(users)            
            
        }else{
            // if didn't receive, hence token expired, so unset it
            unsetToken()
        }
        }
    }


    const sendMessageToUser = () => {
        
        if(validateMessage(receipent, messageText)){

        //send message to specific user
        sendMessage(token, receipent, messageText)

        setMessageText("")
        setReceipent(null)
        }
        
    }

    const showReceivedMessages = () => {

        return <div style={{height: "100px", width: "400px", overflowY: "auto"}}>
            {receivedMessages.map((singleMessage) => {
                return <div>{singleMessage}</div>
            })}
        </div>

    }


    const showChatWindow = () => {

        return (
        <div>
            <Input 
            type="text" 
            placeholder="Write Here"
            onChange={e => setMessageText(e.target.value)} 
            style={{margin: "5px", width: "400px",}}  
            value={messageText}/>

            <Dropdown isOpen={dropdownOpen} toggle={toggle} style={{margin: "5px"}}>
            <DropdownToggle caret>
                {receipent ? receipent : "Choose Receipent"}
            </DropdownToggle>
            <DropdownMenu>
                {onlineUsers && onlineUsers.map((user) => {
                    return <DropdownItem onClick={e => setReceipent(e.target.value)} value={user}>{user}</DropdownItem>
                })}
                
            </DropdownMenu>
            </Dropdown>
            <Button color="primary" onClick={sendMessageToUser}>Send</Button>
            {receivedMessages && receivedMessages.length > 0 ? showReceivedMessages(): null}
        </div>)
    }
    
    return (
    
    <div>
        {token ? <p>SEND A HIE!</p> : <p>LOGIN TO CHAT</p>}
        {token ? showChatWindow() : null}
    </div>
    )
}

export default ChatApp
