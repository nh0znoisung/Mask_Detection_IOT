import React, {useState} from 'react'

function Message(props){
    return(
        <div className="message">
            {props.message}
        </div>
    )
}

export default function Main() {
    // Object + timestamp
    const [message, setMessage] = useState(['Hệ thống AI đã xác nhận người', 'Hệ thống AI đã yêu cầu mở cửa', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp','Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Hệ thống AI đã yêu cầu mở cửa', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp','Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp', 'Admin đã yêu cầu mở cửa khẩn cáp'])
    const message_item = message.map((item) => {
        return <Message message={item} />
    })
    return (
        <div className='main'>
            <div className='main-container'>
                <div className='video'>
                    <video controls autostart autoPlay src="https://www.youtube.com/5bb52318-9f08-4c47-af6d-05ce4fdd8142" type="video/mp4" />            </div>
                <div className='control'>
                    State of door: Opening... Closing...  Close(Default) Open
                </div>
                <div className='chatbox input'>
                    <div className="title">
                        HISTORY REQUEST
                    </div
                    <div className='scroll-bar'>
                        {message_item}
                    </div>
                </div>
            </div>
        </div>
  )
}
