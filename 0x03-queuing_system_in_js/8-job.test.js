import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job.js';

const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '41535158309',
    message: 'This is the code 1234 to verify your account'
  }
];

describe('createPushNotificationsJobs function', () => {
  let queue;

  before(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(null, queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    createPushNotificationsJobs(list, queue);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs.length).to.equal(2);
  });

  it('should have the expected data', () => {
    createPushNotificationsJobs(list, queue);
    expect(queue.testMode.jobs[0].data).to.eql({
      phoneNumber: '4153518780',
      message: 'This is the code 1234 to verify your account'
    });
    expect(queue.testMode.jobs[1].data).to.eql({
      phoneNumber: '41535158309',
      message: 'This is the code 1234 to verify your account'
    });
  });
});
