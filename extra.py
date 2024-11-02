from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Asegúrate de tener la carpeta 'downloads'
    }
    
    # Crear la carpeta de descarga si no existe
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Retornar el último archivo descargado
    downloaded_file = max([f for f in os.listdir('downloads')], key=lambda f: os.path.getctime(os.path.join('downloads', f)))
    return send_file(os.path.join('downloads', downloaded_file), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
