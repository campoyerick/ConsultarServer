from flask import Flask, render_template, request, jsonify
from mcstatus import JavaServer
import re

app = Flask(__name__)

def convert_minecraft_colors(motd):
    color_codes = {
        '§0': '<span style="color: #000000;">',
        '§1': '<span style="color: #0000AA;">',
        '§2': '<span style="color: #00AA00;">',
        '§e': '<span style="color: #FFAA00;">',
        '§f': '<span style="color: #FFFFFF;">',
    }
    for code, replacement in color_codes.items():
        motd = motd.replace(code, replacement)
    motd = re.sub(r'§.', '</span>', motd)
    return motd

@app.route('/status', methods=['GET', 'POST'])
def server_status():
    if request.method == 'POST':
        server_address = request.form['server_address']
        try:
            server = JavaServer.lookup(server_address)
            status = server.status()
            converted_motd = convert_minecraft_colors(status.description)
            return render_template('status.html', status={
                "server_address": server_address,
                "players_online": status.players.online,
                "max_players": status.players.max,
                "motd": converted_motd, 
                "version": status.version.name
            })
        except Exception as e:
            return render_template('status.html', error=str(e))
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True)
