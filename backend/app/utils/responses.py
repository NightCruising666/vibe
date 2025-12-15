from flask import jsonify


def success(data=None, message: str = "ok", status_code: int = 200):
    payload = {"message": message, "data": data}
    return jsonify(payload), status_code


def error(message: str, status_code: int = 400):
    payload = {"message": message}
    return jsonify(payload), status_code


def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404(_):
        return error("Not found", 404)

    @app.errorhandler(400)
    def handle_400(err):
        return error(str(err), 400)

    @app.errorhandler(500)
    def handle_500(err):
        return error(f"Server error: {err}", 500)
