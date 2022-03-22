import express from 'express';
import { createRequest, deleteRequest, getRequest, updateRequest, searchIdRequest} from '../controllers/request.js';

const router = express.Router();

// URL: /api/Request
router.get('/', getRequest)
router.post('/', createRequest)

router.get('/:id', searchIdRequest)

router.post('/update/:id', updateRequest)
router.post('/delete/:id', deleteRequest)

export default router;