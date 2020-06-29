import { LOGIN_URL, GET_USERS_URL } from "./constants";

export const getUsersAPI = async (token) => {

    let APIResponse = null
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({token: token})
    };

    APIResponse = await fetch(GET_USERS_URL, requestOptions)    
    let response = await APIResponse.json()
    if (response.code == 200){
      return {
        "code": response.code,
        "users": response.data
      }
    }
    else
    {
      return {
        "code": response.code,
        "error": response.message
      }
    }
  }


export const loginUserAPI = async (mail, password) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: mail, password: password})
    };
    
    let APIResponse = await fetch(LOGIN_URL, requestOptions)
        .then(response => response.json())
        .then(data => {

          if(data["code"] == 200){
            
            return {
              "type": "success",
              "token": data["data"]
            }
          }
          else
          {
            return {
              "type": "error",
              "error": data["message"]
            }
          }     
        });
        return APIResponse
}


export const validateMessage = (receipent, messageText) => {
      let errorMessage = ""
      if(!receipent){
          errorMessage += "Please choose a recipent\n"
      }
      if(!messageText){
          
          errorMessage += "Please write something\n"
      }
      if(errorMessage){
          alert(errorMessage)
          return false
      }
      else{
          return true
      }
  }
  