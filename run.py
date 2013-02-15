from flask import Flask, render_template, request
from flask_flatpages import FlatPages

from torcheck import check_tor_ip

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
pages = FlatPages(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    def get_request_ip(request):
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
        else:
            return request.environ.get('REMOTE_ADDR')
    using_tor = check_tor_ip(get_request_ip(request))
    return render_template('upload.html', using_tor=using_tor)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'default.html')
    return render_template(template, page=page)

if __name__ == "__main__":
    app.run()
