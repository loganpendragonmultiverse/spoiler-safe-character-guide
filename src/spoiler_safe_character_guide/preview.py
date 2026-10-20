from __future__ import annotations

import json
from typing import Any


def render_html(report: dict[str, Any]) -> str:
    # Milestones may exceed JavaScript's exact Number range.
    preview = {
        **report,
        "through": str(report["through"]),
        "characters": [
            {
                **character,
                "introduced_at": str(character["introduced_at"]),
                "facts": [
                    {**fact, "milestone": str(fact["milestone"])} for fact in character["facts"]
                ],
                "aliases": [
                    {**alias, "milestone": str(alias["milestone"])}
                    for alias in character["aliases"]
                ],
            }
            for character in report["characters"]
        ],
    }
    if "relationships" in report:
        preview["relationships"] = [
            {**item, "milestone": str(item["milestone"])} for item in report["relationships"]
        ]
    payload = json.dumps(preview).replace("<", "\\u003c").replace("&", "\\u0026")
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Spoiler-safe character guide</title>
<style>body{font:17px system-ui;max-width:850px;margin:auto;padding:24px;background:#f5f1e8;color:#273643}
article{background:white;padding:18px;margin:18px 0;border:1px solid #b8c5cb;border-radius:10px}
input{font:inherit;padding:9px;box-sizing:border-box;max-width:100%}label{display:block;margin:12px 0}
@media print{.controls{display:none}article{break-inside:avoid}body{background:white}}</style>
<h1>Spoiler-safe character guide</h1><p>Only material permitted by the exported boundary is included in this file.</p>
<div class="controls"><label>Search visible names, aliases and facts <input id="search" type="search"></label>
<label>Preview earlier boundary <input id="boundary" type="text" inputmode="numeric" pattern="[0-9]*"></label></div>
<p id="status" role="status"></p><main id="cards"></main><script id="data" type="application/json">"""
        + payload
        + """</script>
<script>const data=JSON.parse(document.getElementById('data').textContent);
const boundary=document.getElementById('boundary');boundary.value=data.through;
const ceiling=BigInt(data.through);
function draw(){const raw=boundary.value.trim();const requested=/^[0-9]+$/.test(raw)?BigInt(raw):0n;
 const through=requested>ceiling?ceiling:requested;
 const query=document.getElementById('search').value.toLowerCase();const cards=document.getElementById('cards');cards.replaceChildren();let count=0;
 for(const relation of (data.relationships||[])){if(BigInt(relation.milestone)>through)continue;
 if(![relation.source,relation.target,relation.text].join(' ').toLowerCase().includes(query))continue;
 const p=document.createElement('p');p.textContent=relation.source+' — '+relation.target+': '+relation.text;cards.append(p);}
 for(const character of data.characters){if(BigInt(character.introduced_at)>through)continue;
 const facts=character.facts.filter(f=>BigInt(f.milestone)<=through);const aliases=character.aliases.filter(a=>BigInt(a.milestone)<=through);
 if(![character.name,...facts.map(f=>f.text),...aliases.map(a=>a.name)].join(' ').toLowerCase().includes(query))continue;
 const card=document.createElement('article');const title=document.createElement('h2');title.textContent=character.name;card.append(title);
 const names=document.createElement('p');names.textContent=aliases.length?'Aliases: '+aliases.map(a=>a.name).join(', '):'No aliases revealed';card.append(names);
 for(const fact of facts){const p=document.createElement('p');p.textContent=`${fact.text} (milestone ${fact.milestone})`;card.append(p);}cards.append(card);count++;
 }document.getElementById('status').textContent=`Boundary ${through}: ${count} visible characters. Export ceiling: ${data.through}.`;
}boundary.addEventListener('input',draw);document.getElementById('search').addEventListener('input',draw);draw();</script></html>"""
    )
