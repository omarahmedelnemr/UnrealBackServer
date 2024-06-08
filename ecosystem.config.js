module.exports = {
    apps: [
      {
        name: "flask-app",
        script: "server.py",
        interpreter: "python3",
        exec_mode: "fork",
        instances: 1,
        watch: true,
        env: {
          "FLASK_ENV": "production"
        }
      }
    ]
  }
  