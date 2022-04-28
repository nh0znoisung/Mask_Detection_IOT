import React, {useState} from 'react'
import { Player } from 'video-react';
import {Button} from  'react-bootstrap';
import Header from '../Header';
import axios from 'axios';

function Message(props){
    return(
        <div className="message">
            {props.message}
        </div>
    )
}

function Door(props){
    switch(props.option){
        case '0':
            return <span style={{color: "red"}}>Close</span>
        case '1':
            return <span style={{color: "#EE6B4E"}}>OPENING...</span>
        case '2':
            return <span style={{color: "#00FF00"}}>OPEN</span>
        case '3':
            return <span style={{color: "#FFC300"}}>CLOSING...</span>
        default:
            return <span style={{color: "blue"}}>SOMETHING WRONG??</span>
    }
    // Opening... Closing...  Close(Default) Open
}

function Bulb(props){
    if(props.option === '0'){
        return <span style={{color: "red"}}>Off</span>
    }else{
        return <span style={{color: "#FFC300"}}>On</span>
    }
<<<<<<< Updated upstream
    
=======
}

const URL_BACKEND = 'http://localhost:5000/'
const TIMEZONE = "Asia/Ho_Chi_Minh"
const ADA_KEY = "aio_uTad06JQBJ5bWlXwstpYX1NEKE1l"

function convertDate(s){
    // s: string
    let date = moment(s)
    return date.tz(TIMEZONE).format('h:mm:ss A, DD/MM/YYYY')
>>>>>>> Stashed changes
}

export default function Main() {
    // Object + timestamp
    const [message, setMessage] = useState([]);
    // useState(['Hệ thống AI đã xác nhận người', 'Hệ thống AI đã yêu cầu mở cửa', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp','Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Hệ thống AI đã yêu cầu mở cửa', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp','Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp', 'Admin đã yêu cầu mở cửa khẩn cấp'])
    
    const [door, setDoor] = useState('1')
    const [bulb, setBulb] = useState('0')
    
    const message_item = message.map((item) => {
        return <Message message={item} />

    })

    function handleDoor(){
        setDoor()
    }
    return (
        <>
            <Header />
            <div className='main'>
                <div className='main-container'>
                    {/* <div className='video'> */}
                    {/* <Player
                        playsInline
                        poster="/assets/poster.png"
                        // src="https://media.w3.org/2010/05/sintel/trailer_hd.mp4"
                        src = "https://9be4-115-78-8-83.ngrok.io/video"
                    />    */}
                    <img style={{height: "30vw", width:"54vw"}} alt="Video here" src="https://acc6-115-78-8-83.ngrok.io/video"></img>       
                    {/* </div> */}
                    <div className='info'>
                        <div className='door'>State of door:  <Door option={door} /></div>
                        <div className='bulb'>State of bulb:  <Bulb option={bulb} /></div>
                    </div>
                    <div className='control'>
                        <Button variant="danger" className="btn-1" onClick={() => handleDoor()}>Emergency open</Button> 
                        <input type="checkbox" className="toggle" id="rounded"></input>
                        <label for="rounded" data-checked="Manual" className="round" data-unchecked="Auto"></label>  
                        <Button variant="info" className="btn-1">Bulb switcher</Button>
                    </div>
                    <div className='chatbox input'>
                        <div className="title">
                            HISTORY REQUEST
                        </div>
                        <div className='scroll-bar'>
                            {message_item}
                        </div>
                    </div>
                </div>
            </div>
        </>
  )
}
