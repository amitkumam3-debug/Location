from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def validate_imei(imei):
    imei = str(imei).replace(" ", "").replace("-", "")

    if len(imei) != 15 or not imei.isdigit():
        return False

    # Luhn checksum
    total = 0

    for i, digit in enumerate(imei):
        n = int(digit)

        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9

        total += n

    return total % 10 == 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_imei():
    data = request.get_json()
    imei = data.get("imei", "")

    imei = imei.replace(" ", "").replace("-", "")

    if validate_imei(imei):
        return jsonify({
            "valid": True,
            "message": "Valid IMEI number",
            "location": "Live location is not available from IMEI alone."
        })

    return jsonify({
        "valid": False,
        "message": "Invalid IMEI number",
        "location": None
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)