import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
	console.log('Redis client connected to the server');
});

client.on('error', (err) => {
	console.error(`Redis client not connected to the server: ${err}`);
});

function setNewSchool(schoolName, value) {
	client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
	const resp = await client.get(schoolName);
	console.log(resp);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
