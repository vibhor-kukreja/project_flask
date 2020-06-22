import React, {useState, useEffect} from 'react'
import {Button} from 'reactstrap'

const NewsRoom = ({socket}) => {

    const [room, setRoom] = useState("")

    const [allNews, setAllNews] = useState([])


  
  
  const getRoom = () => {
    socket.on("join", roomName => {
      setRoom(roomName)
      //setReceipent()
    })
  }


    useEffect(() => {
        setNews()
      }, [allNews.length])
    
    
      useEffect(() => {
        // to run exactly once
        getRoom()
      }, [])
    
    
      const setNews = () => {
    
        socket.on("news", msg => {
          let newNews = JSON.parse(msg)
          setAllNews([...newNews])
        })
      }


    const showRooms = (...channels) => {
        const channel = channels.map((singleChannel) => {
          return <Button  color="success" style={{marginLeft: "5px", marginRight:"5px"}} onClick={e => joinRoom(singleChannel)}>{singleChannel.toUpperCase()}</Button>
        })
        return channel
      }
    
      const syncNews = () => {
        socket.emit("sync")
      }

      const joinRoom = (channelName) => {

        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({channelName: channelName})
      };
      fetch('http://localhost:3000/news/', requestOptions)
          .then(response => response.json())
          .then(APIResponse => {
            setAllNews(JSON.parse(APIResponse['data']))
          });
        if(room){
          socket.emit("leave", room)
        }
        socket.emit("join", channelName)
        setRoom(channelName)
      }

    return (
        <div style={{marginTop: "10px"}}>
        <div style={{display:"block"}}>
        {showRooms("ndtv", "bbc", "times")}
        </div>
          <hr/>
          {allNews.length > 0 && allNews.map(news => (
            <div><a href={news['link']} target="_blank" style={{color: "#09d3ac"}}>{news['title']}</a></div>
        ))}
            <hr/>
          <button onClick={syncNews}>Sync</button>
          <hr/>
        </div>
    )
}

export default NewsRoom