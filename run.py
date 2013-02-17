import os

from flask import Flask, render_template, request, redirect
from flask_flatpages import FlatPages

from torcheck import check_tor_ip

UPLOAD_ONION_URL = "http://xyz.onion" # can this live in settings.cfg?

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
pages = FlatPages(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    def get_ip_from_request(request):
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
        else:
            return request.environ.get('REMOTE_ADDR')
    client_ip = get_ip_from_request(request)
    using_tor = check_tor_ip(client_ip)
    if using_tor:
        return redirect(UPLOAD_ONION_URL)
    else:
        return render_template('upload.html', using_tor=using_tor,
                client_ip=client_ip, upload_onion_url=UPLOAD_ONION_URL)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'default.html')
    return render_template(template, page=page)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
