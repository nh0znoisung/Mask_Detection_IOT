import './App.css';
import Main from './components/Main';
import Login from './components/Login';
import PrivateRoute from './components/PrivateRoute';

import 'bootstrap/dist/css/bootstrap.min.css';
import "../node_modules/video-react/dist/video-react.css";
// @import "~video-react/styles/scss/video-react"; //for scss
import { Routes, Route } from 'react-router-dom';
import {AuthProvider} from './contexts/AuthContext';


function App() {
	return(
		<AuthProvider>
			{/* <Header /> */}
			<Routes>
				{/* <PrivateRoute exact path="/" component={Main} /> */}
				<Route path="/" exact element={
					<PrivateRoute>
						<Main />
					</PrivateRoute>
				} />

				{/* <PrivateRoute path="/update-profile" component={UpdateProfile} /> */}
				<Route path="/login" element={ <Login />} > </Route>
				{/* <Route path="/admin" element={<Main />} > </Route> */}
				{/* <Route path="/login" element={<Main />} > </Route> */}

				{/* <Route path="*" element={<NotFound />} /> */}
			</Routes>
		</AuthProvider>
	)
}

export default App;
