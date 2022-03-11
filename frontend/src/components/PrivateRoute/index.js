import React from "react"
import { Route, Navigate, Outlet } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"

export default function PrivateRoute({ children }) {
    let  { currentUser } = useAuth();
  
    if (!currentUser) {
      return <Navigate to="/login"  replace />;
    }
  
    return children;
}