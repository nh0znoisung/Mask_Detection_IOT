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
    }else if(s.action === 4){
        action = "bật hệ thống nhận diện khuôn mặt"
    }else if(s.action === 5){
        action = "tắt hệ thống nhận diện khuôn mặt"
    }
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
        case 'AUTHORITY:OFF':
            return <span style={{color: "red"}}>OFF</span>
        case 'AUTHORITY:ON':
            return <span style={{color: "green"}}>ON</span>
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
const ADA_KEY = "aio_HEPK82iCycd8fBUTW5uO8Aoey2tz"

function convertDate(s){
    // s: string
    let date = moment(s)
    return date.tz(TIMEZONE).format('h:mm:ss A, DD/MM/YYYY')
}

export default function Main() {
    // Object + timestamp
    const [message, setMessage] = useState([])
    const [door, setDoor] = useState('AUTHORITY:OFF')
    const [bulb, setBulb] = useState('LIGHT:OFF')
    const [mask, setMask] = useState('START:OFF')

    const [colorDoor, setColorDoor] = useState('danger')
    const [colorBulb, setColorBulb] = useState('danger')
    const [colorMask, setColorMask] = useState('danger')

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
                let newDoor = data_device.filter(item => item.key === 'btn-authority')[0].last_value
                let newBulb = data_device.filter(item => item.key === 'swt-light')[0].last_value
                let newMask = data_device.filter(item => item.key === 'btn-start')[0].last_value

                setDoor(newDoor)
                setBulb(newBulb)
                setMask(newMask)
                
                setColorDoor(newDoor === 'AUTHORITY:ON' ? 'success' : 'danger')
                setColorBulb(newBulb === 'LIGHT:ON' ? 'success' : 'danger')
                setColorMask(newMask === 'START:ON' ? 'success' : 'danger')
            }).catch(err => {console.log(err)})
        }, 750); 
        
        return () => clearInterval(interval);
      }, []);
    

    const message_item = message.map((item) => {
        return <Message key={item._id} message={item} />

    })

    async function handleDoor(){
        let newDoor = (door === 'AUTHORITY:ON') ? 'AUTHORITY:OFF' : 'AUTHORITY:ON'
        let obj = {
            subject: 0,
            action: newDoor === 'AUTHORITY:ON' ? 0 : 1,
            state: 0
        }
        await axios.post(URL_BACKEND, obj).catch(err => {console.log(err)})
        axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/btn-authority/data", {"value": newDoor}, 
        {
            headers: {
                'X-AIO-Key': ADA_KEY
            }
        }
        ).catch(err => {console.log(err)})

        axios.get(URL_BACKEND).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})
    }

    async function handleBulb(){
        
        let newBulb = (bulb === 'LIGHT:OFF') ? 'LIGHT:ON' : 'LIGHT:OFF'
        let obj = {
            subject: 0,
            action: (newBulb === 'LIGHT:ON') ? 2 : 3,
            state: 0
        }
        await axios.post(URL_BACKEND, obj).catch(err => {console.log(err)})
        await axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/swt-light/data", {"value": newBulb},
        {
            headers: {
                'X-AIO-Key': ADA_KEY
            }
        }
        ).catch(err => {console.log(err)})

        axios.get(URL_BACKEND).then(res => {setMessage(res.data)}).catch(err => {console.log(err)})

    }

    async function handleMask(){
        let newMask = (mask === 'START:OFF') ? 'START:ON' : 'START:OFF'
        let obj = {
            subject: 0,
            action: (newMask === 'START:ON') ? 4 : 5,
            state: 0
        }
        await axios.post(URL_BACKEND, obj).catch(err => {console.log(err)})
        await axios.post("https://io.adafruit.com/api/v2/GodOfThunderK19/feeds/btn-start/data", {"value": newMask},
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
                        <div className='door'>State of authority:  <Door option={door} /></div>
                        <div className='bulb'>State of bulb:  <Bulb option={bulb} /></div>
                    </div>
                    <div className='control'>
                        <Button variant={colorDoor} className="btn-1" onClick={() => handleDoor()}>Door Switcher</Button> 
                        <Button variant={colorMask} className="btn-1" onClick={() => handleMask()}>Mask Recognition Switcher</Button> 
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
