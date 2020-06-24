import {socket} from '../App'

export const joinChat = (token) => {

    socket.emit("join_room", token)

}

export const leaveChat = (token) => {

    socket.emit("leave_room", token)

}

export const sendMessage = (token, recipent, messageText) => {

    socket.emit("message", token, recipent, messageText)
}

export const login = (token) => {

    socket.emit("login", token)

}

export const logout = (token) => {

    socket.emit("logout", token)

}

export const receiveMessage = () => {
    
    socket.on("message", msg => {
        return msg
    })

}
