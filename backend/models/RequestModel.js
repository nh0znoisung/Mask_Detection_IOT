import mongoose from "mongoose";

// 13 columns
const schema = new mongoose.Schema({
    subject: Number, //0: Admin, 1: AI
    action: Number, //0: Open door, 1: Close door, 2: Turn on bulb, 3: Turn off bulb
    state: Number, // 0: In queue, 1: Pending, 2: Success, 2: Failed
}, 
{timestamps: true}
);

export const RequestModel = mongoose.model('request', schema);

