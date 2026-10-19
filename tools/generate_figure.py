from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
nodes=[("Parameters",75,"#2dd4bf"),("Build script",265,"#60a5fa"),("CAD artifacts",455,"#a78bfa"),("Manifest + hashes",645,"#f59e0b")]
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="320" viewBox="0 0 900 320">','<rect width="100%" height="100%" fill="#ffffff"/>','<text x="45" y="45" fill="#17212b" font-family="sans-serif" font-size="23" font-weight="700">Parametric CAD evidence chain</text>']
for i,(label,x,color) in enumerate(nodes):
    parts += [f'<rect x="{x}" y="125" width="155" height="76" rx="0" fill="white" stroke="{color}" stroke-width="2"/>',f'<text x="{x+77}" y="170" text-anchor="middle" fill="#17212b" font-family="sans-serif" font-size="15" font-weight="700">{label}</text>']
    if i<len(nodes)-1: parts.append(f'<path d="M {x+155} 163 L {x+185} 163" stroke="#59636d" stroke-width="3" marker-end="url(#a)"/>')
parts.insert(2,'<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#59636d"/></marker></defs>')
parts += ['<text x="75" y="245" fill="#4d5964" font-family="sans-serif" font-size="13">The manifest binds build inputs and outputs by SHA-256; it does not certify geometry correctness.</text>','</svg>']
(ROOT/"figures").mkdir(exist_ok=True)
(ROOT/"figures/evidence-chain.svg").write_text("\n".join(parts),encoding="utf-8")
