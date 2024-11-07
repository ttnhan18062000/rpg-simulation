// test_client.js
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

// Load the proto file
const packageDefinition = protoLoader.loadSync('notification.proto', {});
const notifierProto = grpc.loadPackageDefinition(packageDefinition).notifier;

function main() {
    const client = new notifierProto.notifier('localhost:50051', grpc.credentials.createInsecure());

    client.notifyUpdate({ message: 'Test notification' }, (error, response) => {
        if (error) {
            console.error('Error calling NotifyUpdate:', error);
        } else {
            console.log('NotifyUpdate response:', response);
        }
    });
}

main();
