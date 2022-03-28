import React, {useState, useEffect} from 'react'
// import { Player } from 'video-react';
import {Button} from  'react-bootstrap';
import Header from '../Header';
import axios from 'axios';
// import moment from 'moment';
import moment from 'moment-timezone';


function Message(props){
    var s = props.message, subject, action;
    if(s.subject === 0){
        subject = "Admin"
    }else{
        subject = "Hệ thống AI"
    }

    if(s.action === 0){
        action = "mở cửa"
    }else if(s.action === 1){
        action = "đóng cửa"
    }else if(s.action === 2){
        action = "bật đèn"
    }else if(s.action === 3){
        action = "tắt đèn"
    }
    // Hệ thống AI đã yêu cầu mở cửa
    console.log(typeof(s.createdAt))
    return(
        <>
            <div className="message">
                {subject} đã yêu cầu {action} 
                <div className="time">{convertDate(s.createdAt)}</div>
            </div>
            
        </>
        
    )
}


function Door(props){
    switch(props.option){
        case '0':
            return <span style={{color: "red"}}>Close</span>
        // case '1':
            // return <span style={{color: "#EE6B4E"}}>OPENING...</span>
        case '1':
            return <span style={{color: "green"}}>OPEN</span>
        // case '3':
            // return <span style={{color: "#FFC300"}}>CLOSING...</span>
        default:
            return <span style={{color: "blue"}}>SOMETHING WRONG??</span>
    }
}

function Bulb(props){
    if(props.option === '0'){
        return <span style={{color: "red"}}>Off</span>
    }else{
        return <span style={{color: "green"}}>On</span>
    }
    
}

const url = 'http://localhost:9000/'
const TIMEZONE = "Asia/Ho_Chi_Minh"

function convertDate(s){
    // s: string
    let date = moment(s)
    return date.tz(TIMEZONE).format('h:mm:ss A, DD/MM/YYYY')
}

export default function Main() {
    // Object + timestamp
    const [message, setMessage] = useState([])

    
    const [door, setDoor] = useState('1')
    const [bulb, setBulb] = useState('0')
    
    useEffect(() => {
        axios.get("https://6b5d-115-75-191-17.ngrok.io/").then(res => {console.log(res.data)}).catch(err => {console.log(err)})

        axios.get(url).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})

        axios.get("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-light").then(res => {
                console.log(res.data)
            }).catch(err => {console.log(err)})
    },[])

    useEffect(() => {
        let interval = null;
        let data_device;
        interval = setInterval(() => {
            // /api/v2/{username}/feeds/{feed_key}/data
            // https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/hVNA81gluI7deGkFZK34L7zTRCdX/data
            // https://io.adafruit.com/api/v2/GodOfThunderK19/feeds?x-aio-key=aio_hVNA81gluI7deGkFZK34L7zTRCdX
            // https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-light/data
            axios.get("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds?x-aio-key=aio_hVNA81gluI7deGkFZK34L7zTRCdX").then(res => {
                data_device = res.data
                // console.log(data_device)
                setDoor(data_device.filter(item => item.key === 'swt-door')[0].last_value)
                setBulb(data_device.filter(item => item.key === 'swt-light')[0].last_value)
            }).catch(err => {console.log(err)})
        }, 750); 
        
        return () => clearInterval(interval);
      }, []);
    

    const message_item = message.map((item) => {
        return <Message key={item._id} message={item} />

    })

    async function handleDoor(){
        axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-door/data", {"value": 1-door}, 
        {
            headers: {
                'X-AIO-Key': 'aio_hVNA81gluI7deGkFZK34L7zTRCdX'
            }
        }
        ).catch(err => {console.log(err)})
    }

    async function handleBulb(){
        console.log("Bulb clicked")
        let obj = {
            subject: 0,
            action: 2,
            state: 0
        }
        await axios.post(url, obj).catch(err => {console.log(err)})

        await axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-light/data", {"value": 1-bulb},
        {
            headers: {
                'X-AIO-Key': 'aio_hVNA81gluI7deGkFZK34L7zTRCdX'
            }
        }
        ).catch(err => {console.log(err)})

        axios.get(url).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})

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
                    <img style={{height: "30vw", width:"54vw"}} alt="Video here" src="http://localhost:9999/video"></img>       
                    {/* </div> */}
                    <div className='info'>
                        <div className='door'>State of door:  <Door option={door} /></div>
                        <div className='bulb'>State of bulb:  <Bulb option={bulb} /></div>
                    </div>
                    <div className='control'>
                        <Button variant="danger" className="btn-1" onClick={() => handleDoor()}>Emergency open</Button> 
                        <input type="checkbox" className="toggle" id="rounded"></input>
                        <label  data-checked="Manual" className="round" data-unchecked="Auto"></label>  
                        <Button variant="info" className="btn-1" onClick={() => handleBulb()}>Bulb switcher</Button>
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
