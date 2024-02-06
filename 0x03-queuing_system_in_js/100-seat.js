import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const client = redis.createClient();
const clientGet = promisify(client.get).bind(client);
const queue = kue.createQueue();

let reservationEnabled = true;

function reserveSeat(number) {
    client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
    return await clientGet('available_seats');
}

reserveSeat(50);

app.get('/available_seats', async (req, res) => {
    const numberOfSeats = await getCurrentAvailableSeats();
    res.send({ numberOfAvailableSeats: numberOfSeats });
});

app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.send({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat');
    job.save((err) => {
        if (!err) {
            res.send({ status: 'Reservation in process' });
        } else {
            res.send({ status: 'Reservation failed' });
        }
    });

    job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
    job.on('failed', (error) => console.log(`Seat reservation job ${job.id} failed: ${error}`));
});

app.get('/process', async (req, res) => {
    res.send({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        const availableSeats = await getCurrentAvailableSeats();
        const newAvailableSeats = availableSeats - 1;

        if (newAvailableSeats === 0) {
            reservationEnabled = false;
        }

        if (newAvailableSeats >= 0) {
            reserveSeat(newAvailableSeats);
            done();
        } else {
            done(new Error('Not enough seats available'));
        }
    });
});

app.listen(1245, () => {
    console.log('Server is running on port 1245');
});
