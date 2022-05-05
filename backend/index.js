// npm install express mongoose body-parser cors nodemon dotenv
import express from 'express';
// Using middleware
import bodyParser from 'body-parser';
import cors from 'cors';
// Using router for architechture 
import request from './routers/request.js';

// Using mongoose for database
import mongoose from 'mongoose';
// Dot env for config
import dotenv from 'dotenv';


dotenv.config();

const app = express();
const PORT = process.env.PORT || 50;

app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({ extended: true , limit: '50mb'}));
app.use(cors());

//More router divded into different files (Router Folder)
app.use('/', request)




// Connect to MongoDB. Return a promise
mongoose.connect(process.env.DATABASE_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        console.log('Connected to MongoDB');
        app.listen(PORT, ()=>{
            console.log(`Server is running on port ${PORT}`);
        })
    })
    .catch(err => console.log(err));


// $ git add .
// $ git commit -am "make it better"
// $ git push heroku master