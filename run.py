from apps import create_app

app, socketio = create_app()

if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=True)