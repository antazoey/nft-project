import htmlmin
from flask import Flask

HTML = """
<!DOCTYPE html>
<html>
  <body>
    <h1>Here hit this!</h1>

    <iframe
      src="https://docs.google.com/forms/d/e/1FAIpQLSf8lwLcZOwmY2r7PiHy-CrtlJ41FAnsuUhZ6oK2pm66gey7Hg/viewform?embedded=true"
      width="640"
      height="407"
      frameborder="0"
      marginheight="0"
      marginwidth="0"
      >Loading…</iframe
    >
  </body>
</html>
"""
app = Flask(__name__)


@app.route("/")
def home():
    return htmlmin.minify(HTML.strip(), remove_empty_space=True)


def main():
    app.run(host="127.0.0.1", port=5000)
