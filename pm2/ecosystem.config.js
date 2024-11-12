module.exports = {
  apps: [
    {
      name: "notify-server",
      script: "node",
      args: "server.js",
      cwd: "../dashboard/server",
    },
    {
      name: "kafka-consumer",
      script: "python",
      args: "push_to_mongodb.py",
      cwd: "../data_streaming/kafka",
    },
    {
      name: "game",
      script: "python",
      args: "game.py",
      cwd: "../game",
    },
  ],
};