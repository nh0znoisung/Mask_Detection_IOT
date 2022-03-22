import mongoose from "mongoose";

// 13 columns
const schema = new mongoose.Schema({
    subject: Number, //0: Admin, 1: AI
    action: Number, //0: Open door, 1: Close door, 2: Turn on bulb, 3: Turn off bulb
}, 
{timestamps: true}
);

export const RequestModel = mongoose.model('request', schema);