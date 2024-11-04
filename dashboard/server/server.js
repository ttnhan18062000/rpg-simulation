// server.js
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const WebSocket = require('ws');

const packageDefinition = protoLoader.loadSync('notification.proto', {});
const notifierProto = grpc.loadPackageDefinition(packageDefinition).notifier; // Match the package name here

const wss = new WebSocket.Server({ port: 3001 });

function notifyUpdate(call, callback) {
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ type: 'update' }));
        }
    });
    callback(null, { success: true });
}

function main() {
    const server = new grpc.Server();
    server.addService(notifierProto.Notifier.service, { notifyUpdate });
    server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
        server.start();
        console.log('gRPC server running on port 50051');
    });
}

main();