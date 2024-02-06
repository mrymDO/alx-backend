import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
	console.log('Redis client connected to the server');
});

client.on('error', (err) => {
	console.error(`Redis client not connected to the server: ${err}`);
});

const subscriber = client.duplicate();

subscriber.subscribe('holberton school channel');

subscriber.on('message', (channel, message) => {
	if (channel === 'holberton school channel') console.log(message);
	if (message === 'KILL_SERVER') {
		subscriber.unsubscribe(channel);
		subscriber.quit();
	}
});
