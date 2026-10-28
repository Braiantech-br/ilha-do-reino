# Monta o index.html (jogo num arquivo só, com as imagens embutidas).
# As imagens do Tiny Swords não ficam soltas no repositório (licença): se a pasta codigo/assets/ não existir,
# elas são tiradas do jogo publicado do Reino Pequeno (atualizacao/jogo.html), onde já viajam embutidas.
#   python3 codigo/build.py [caminho/para/Reino-Pequeno/atualizacao/jogo.html]
import base64, json, os, re, sys
R = os.path.dirname(os.path.abspath(__file__))
A_DIR = f'{R}/assets'
NEED = [f'b_{u}_{a}' for u in ['warrior','archer','lancer','monk'] for a in ['idle','run','atk']] + \
       ['b_pawn_idle','b_pawn_run','b_pawn_axe','sheep_idle','sheep_move','sheep_grass','tiles1','foam','dust'] + \
       [f'tree{i}' for i in range(1,5)] + ['gold3','gold4','gold5'] + [f'bush{i}' for i in range(1,5)] + \
       [f'rock{i}' for i in range(1,5)] + ['cloud1','cloud2','cloud3']
if not os.path.isdir(A_DIR):
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(R, '..', '..', 'Reino-Pequeno', 'atualizacao', 'jogo.html')
    html = open(src, encoding='utf-8').read()
    d = json.loads(re.search(r'window\.__A=(\{.*?\});function AS', html, re.S).group(1))
    os.makedirs(A_DIR)
    for k, u in d.items(): open(f'{A_DIR}/{k}.png', 'wb').write(base64.b64decode(u.split(',', 1)[1]))
meta = json.load(open(f'{R}/meta.json')); meta['tiles1'] = [576, 384, 1, 0, 0, 576, 384]
A = {k: 'data:image/png;base64,' + base64.b64encode(open(f'{A_DIR}/{k}.png', 'rb').read()).decode() for k in NEED}
M = {k: meta[k] for k in NEED}
page = open(f'{R}/src/jogo.html', encoding='utf-8').read()
page = page.replace('__ASSETS__', json.dumps(A, separators=(',', ':'))).replace('__META__', json.dumps(M, separators=(',', ':')))
page = page.replace('__THREE__', 'https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js')
open(f'{R}/../index.html', 'w', encoding='utf-8').write(page)
print('index.html:', len(page.encode()) // 1024, 'KB')
