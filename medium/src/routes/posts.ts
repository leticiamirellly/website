import express from 'express';
import axios from 'axios';
import fs, { writeFileSync } from 'fs';
import path from 'path'
import redis, { createClient } from 'redis';

const router = express.Router()

router.get('/posts', async (req, res) => {
	let response = await axios.get('https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@leticia-mirelly')
	if (response.status !== 200) {
		throw new Error('Não foi possível buscar posts')
	} else {
		const data = JSON.stringify(response.data);
		const dir = path.resolve(__dirname, '../../medium-posts');
		const filePath = path.join(dir, 'posts.json');


		if (!fs.existsSync(dir)) {
			fs.mkdirSync(dir, { recursive: true });
		}
		fs.writeFileSync(filePath, data);

		await nodeRedisDemo(JSON.parse(data).items)



		res.send(JSON.stringify(data));
	}
})

async function nodeRedisDemo(data: any) {
	const client = createClient({
		url: 'redis://redis-service:6379',
	});
	client.on('error', (err) => console.log('Redis Client Error', err));

	try {
		await client.connect();

		const jsonData = await client.get('posts');

		let existingPosts: any[] = [];
		const formattedData = JSON.stringify(data);
		if (jsonData) {
			try {
				const parsedValue = JSON.parse(jsonData);
				if (Array.isArray(parsedValue)) {
					existingPosts = [...parsedValue];
				} else {
					existingPosts = [];
				}
			} catch (parseErr) {
				existingPosts = [];
			}
		} else {
			
			await client.set('posts', formattedData);
			// await emitMessageBroker(formattedData)
		}
		
		

		const newItems = data.items || [];

		const newPosts = newItems.filter((item: any) => !existingPosts.some((existingPost: any) => existingPost.guid === item.guid));

		if (newPosts.length > 0) {
            const updatedPosts = [...existingPosts, ...newPosts];
            await client.set('posts', JSON.stringify(updatedPosts));
			// await emitMessageBroker(JSON.stringify(updatedPosts))
            console.log('Posts updated in Redis');
        } 

		await emitMessageBroker(formattedData)

	} catch (err) {
		console.error('Error in Redis operation:', err);
	} finally {
		await client.quit();
	}
}

const emitMessageBroker = async (newPosts: any) => {
	const messageClient = createClient({ url: 'redis://redis-service:6379' });
	await messageClient.connect();
	await messageClient.publish('new_posts_channel', newPosts);
	await messageClient.quit();
}

export { router as currentPostsRouter }
