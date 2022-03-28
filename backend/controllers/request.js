// Use data from database (MongoDB) in Model folder
import { RequestModel } from "../models/RequestModel.js"; 

export const getRequest = async (req, res) => {
    try{
        const posts = await RequestModel.find();
        res.status(200).json(posts);
    }catch(err){
        res.status(500).json({message: err.message});
    }
};

export const searchIdRequest = async (req, res) => {
    try{
        const id = req.params.id;
        const posts = await RequestModel.findOne({_id: id});
        res.status(200).json(posts);

    }catch(err){
        res.status(500).json({message: err.message});
    }
};

export const createRequest = async (req, res) => {
    try {
        const newPost = req.body;

        const post = new RequestModel(newPost);
        post.save();    
        res.status(200).json(post);

    } catch (error) {
        res.status(500).json({ message: error.message });
    }        
};

export const updateRequest = async (req, res) => {
    try {
        const updatePost = req.body;

        const post = await RequestModel.findOneAndUpdate(
          { _id: updatePost._id },
          updatePost,
          { new: true }
        );
    
        res.status(200).json(post);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }        
};

export const deleteRequest = async (req, res) => {
    try {
        const id = req.params.id;
        const post = await RequestModel.deleteOne({_id: id}); // return in place and save

        res.status(200).json(post);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }        
};

