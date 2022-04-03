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
        case 'DOOR:CLOSE':
            return <span style={{color: "red"}}>Close</span>
        case 'DOOR:OPEN':
            return <span style={{color: "green"}}>OPEN</span>
        default:
            return <span style={{color: "blue"}}>SOMETHING WRONG??</span>
    }
}

function Bulb(props){
    if(props.option === 'LIGHT:OFF'){
        return <span style={{color: "red"}}>Off</span>
    }else if(props.option === 'LIGHT:ON'){
        return <span style={{color: "green"}}>On</span>
    }
}

const URL_BACKEND = 'http://localhost:5000/'
const TIMEZONE = "Asia/Ho_Chi_Minh"
const ADA_KEY = "aio_AgWg074IRFfEFP6quOIUQ8ruP5g7"

function convertDate(s){
    // s: string
    let date = moment(s)
    return date.tz(TIMEZONE).format('h:mm:ss A, DD/MM/YYYY')
}

export default function Main() {
    // Object + timestamp
    const [message, setMessage] = useState([])
    const [door, setDoor] = useState('DOOR:CLOSE')
    const [bulb, setBulb] = useState('LIGHT:OFF')
    const [colorDoor, setColorDoor] = useState('danger')
    const [colorBulb, setColorBulb] = useState('danger')

    useEffect(() => {

        axios.get(URL_BACKEND).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})

        axios.get("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-light").then(res => {
                console.log(res.data)
            }).catch(err => {console.log(err)})
    },[])

    useEffect(() => {
        let interval = null;
        let data_device;
        interval = setInterval(() => {
            axios.get(`https://io.adafruit.com/api/v2/GodOfThunderK19/feeds?x-aio-key=` + ADA_KEY).then(res => {
                data_device = res.data
                let newDoor = data_device.filter(item => item.key === 'swt-door')[0].last_value
                let newBulb = data_device.filter(item => item.key === 'swt-light')[0].last_value
                setDoor(newDoor)
                setBulb(newBulb)
                
                setColorDoor(newDoor === 'DOOR:OPEN' ? 'success' : 'danger')
                setColorBulb(newBulb === 'LIGHT:ON' ? 'success' : 'danger')
            }).catch(err => {console.log(err)})
        }, 750); 
        
        return () => clearInterval(interval);
      }, []);
    

    const message_item = message.map((item) => {
        return <Message key={item._id} message={item} />

    })

    async function handleDoor(){
        let obj = {
            subject: 0,
            action: 0,
            state: 0
        }
        await axios.post(URL_BACKEND, obj).catch(err => {console.log(err)})
        let newDoor = (door === 'DOOR:OPEN') ? 'DOOR:CLOSE' : 'DOOR:OPEN'
        axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-door/data", {"value": newDoor}, 
        {
            headers: {
                'X-AIO-Key': ADA_KEY
            }
        }
        ).catch(err => {console.log(err)})

        axios.get(URL_BACKEND).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})
    }

    async function handleBulb(){
        let obj = {
            subject: 0,
            action: 2,
            state: 0
        }
        await axios.post(URL_BACKEND, obj).catch(err => {console.log(err)})
        let newBulb = (bulb === 'LIGHT:OFF') ? 'LIGHT:ON' : 'LIGHT:OFF'
        await axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-light/data", {"value": newBulb},
        {
            headers: {
                'X-AIO-Key': ADA_KEY
            }
        }
        ).catch(err => {console.log(err)})

        axios.get(URL_BACKEND).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})

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
                        <Button variant={colorDoor} className="btn-1" onClick={() => handleDoor()}>Door Switcher</Button> 
                        <Button variant={colorDoor} className="btn-1" onClick={() => handleDoor()}>Mask Recognition Switcher</Button> 
                        <Button variant={colorBulb} className="btn-1" onClick={() => handleBulb()}>Bulb Switcher</Button>
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
