import React, {useState, useRef} from 'react'
import { Form, Alert} from "react-bootstrap"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"


export default function Login() {
    const emailRef = useRef()
    const passwordRef = useRef()
    const { login } = useAuth()
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate();

    async function handleSubmit(e){
        e.preventDefault()
        // console.log("handleSubmit")
        try {
          setError("")
          setLoading(true)
          await login(emailRef.current.value, passwordRef.current.value)
          navigate('/');
        } catch {
          setError("Failed to log in")
        }
    
        setLoading(false)
    }
  return (
    <section className="vh-100 gradient-custom">
        <div className="container py-5 h-100">
            <div className="row d-flex justify-content-center align-items-center h-100">
                <div className="col-12 col-md-8 col-lg-6 col-xl-5">
                <div className="card bg-dark text-white">
                    <div className="card-body p-5 text-center">
        
                    <div className="mb-md-3 mt-md-4">
        
                        <h2 className="fw-bold mb-2 text-uppercase">Đăng nhập</h2>
                        <p className="text-white-50 mb-5">Hãy điền tài khoản và mật khẩu của bạn!</p>
                        {error && <Alert variant="danger">{error}</Alert>}

                        <Form onSubmit={handleSubmit}>
                            <div className="form-outline form-white mb-4">
                            <input type="email" className="form-control form-control-lg" ref={emailRef} placeholder="Tài khoản" required />
                            </div>
            
                            <div className="form-outline form-white mb-4">
                            <input type="password" className="form-control form-control-lg" placeholder="Mật khẩu" ref={passwordRef} required />
                            </div>
                            
                            <button disabled={loading} className="btn btn-outline-light btn-lg px-5" type="submit">Đăng nhập</button>
                        </Form>
                        <p className="small mt-5 "></p>
                    </div>
                    </div>
                </div>
                </div>
            </div>
        </div>
    </section>
  )
}
