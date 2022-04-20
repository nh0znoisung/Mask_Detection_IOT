import express from 'express';
// import { createRequest, deleteRequest, getRequest, updateRequest, searchIdRequest} from '../controllers/request.js';
import {RequestController} from '../controllers/request.js';

const router = express.Router();

// URL: /api/Request
router.get('/', RequestController.getRequest)
router.post('/', RequestController.createRequest)

router.get('/:id', RequestController.searchIdRequest)

router.post('/update/:id', RequestController.updateRequest)
router.post('/delete/:id', RequestController.deleteRequest)

export default router;