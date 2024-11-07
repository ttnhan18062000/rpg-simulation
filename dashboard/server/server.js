// server.js
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const WebSocket = require('ws');

// Load the proto file with package definition
const packageDefinition = protoLoader.loadSync('notification.proto', {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});
const notifierProto = grpc.loadPackageDefinition(packageDefinition).notifier; // Adjusted to match proto package

// Create a WebSocket server
const wss = new WebSocket.Server({ port: 3001 });

function notifyUpdate(call, callback) {
    console.log("Receive notifyUpdate");
    const { message, type } = call.request;  // Access the message and type fields

    // Log the incoming message and type for debugging
    console.log(`Message: ${message}, Type: ${type}`);

    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ type, message }));  // Send both type and message
        }
    });

    callback(null, { success: true });
}

function main() {
    const server = new grpc.Server();
    // Add the correct service from notifierProto
    server.addService(notifierProto.Notifier.service, { notifyUpdate });
    server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
        server.start();
        console.log('gRPC server running on port 50051');
    });
}

// Setup WebSocket connection handling
wss.on('connection', (ws) => {
    console.log('New client connected');

    ws.on('message', (message) => {
        console.log(`Received message from client: ${message}`);
        // Handle incoming messages from clients if needed
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

main();
console.log('WebSocket server is running on ws://localhost:3001');