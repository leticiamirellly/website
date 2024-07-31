import express from 'express';
import axios from 'axios';


const router = express.Router()

router.get('/posts', async (req, res) => {
	
		let response = await axios.get('https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@leticia-mirelly')
		if(response.status !== 200) {
			throw new Error('Não foi possível buscar posts')
		} 

		res.send(JSON.stringify(response.data))
	

})

export {router as currentPostsRouter}