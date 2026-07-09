#!/usr/bin/env python3
"""Analyze a Claude agent audit.jsonl for cost attribution and turn timelines.

Usage:
    python3 analyze_audit.py <audit.jsonl> [-o report.html]

Emits a per-agent cost/token summary to stdout and writes a self-contained
HTML report (no external dependencies) with a clickable agent explorer and
the main agent's turn timeline.
"""
import argparse
import collections
import datetime
import html
import json
import sys

# $/MTok: (input, output, cache_read, cache_write_5m, cache_write_1h)
PRICING = {
    "claude-sonnet-4-6": (3, 15, 0.30, 3.75, 6),
    "claude-sonnet-4-5": (3, 15, 0.30, 3.75, 6),
    "claude-haiku-4-5": (1, 5, 0.10, 1.25, 2),
    "claude-opus-4-8": (5, 25, 0.50, 6.25, 10),
    "claude-opus-4-1": (15, 75, 1.50, 18.75, 30),
    "claude-fable-5": (5, 25, 0.50, 6.25, 10),
}
WEB_SEARCH_FEE = 0.01
SUBAGENT_TOOLS = ("Task", "Agent")


def price_for(model):
    for prefix, p in PRICING.items():
        if model.startswith(prefix):
            return p
    print(f"warning: no pricing for model {model}, using sonnet rates", file=sys.stderr)
    return PRICING["claude-sonnet-4-6"]


def parse_ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def analyze(path):
    rows = [json.loads(line) for line in open(path) if line.strip()]
    result = next((r for r in rows if r.get("type") == "result"), None)
    model_usage = (result or {}).get("modelUsage", {})

    # Subagent names from Task/Agent tool_use blocks; report sizes from their tool_results.
    names, report_chars = {}, {}
    for r in rows:
        if r.get("type") != "assistant":
            continue
        for b in r["message"].get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b["name"] in SUBAGENT_TOOLS:
                names[b["id"]] = b["input"].get("description") or b["id"][-8:]
    for r in rows:
        if r.get("type") != "user" or r.get("parent_tool_use_id"):
            continue
        for b in r["message"].get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in names:
                c = b.get("content")
                size = sum(len(x.get("text", "")) for x in c if isinstance(x, dict)) if isinstance(c, list) else len(str(c))
                report_chars[b["tool_use_id"]] = size

    # Group assistant rows by agent (parent_tool_use_id), dedupe by request_id.
    # Streaming snapshots repeat a request with identical usage; input/cache
    # figures are exact, output_tokens is a start-of-stream placeholder.
    agents = collections.defaultdict(lambda: {
        "reqs": collections.OrderedDict(), "tools": collections.Counter(),
        "seen": set(), "first": None, "last": None, "model": None,
    })
    req_chars = collections.defaultdict(int)
    for r in rows:
        if r.get("type") != "assistant":
            continue
        p = r.get("parent_tool_use_id") or "MAIN"
        a = agents[p]
        m, rid, ts = r["message"], r.get("request_id"), r["timestamp"]
        u = m["usage"]
        a["model"] = m["model"]
        a["first"] = min(filter(None, [a["first"], ts]))
        a["last"] = max(filter(None, [a["last"], ts]))
        cc = u.get("cache_creation") or {}
        a["reqs"][rid] = {
            "t": ts, "inp": u["input_tokens"], "cr": u["cache_read_input_tokens"],
            "cc5": cc.get("ephemeral_5m_input_tokens", 0),
            "cc1": cc.get("ephemeral_1h_input_tokens", u["cache_creation_input_tokens"]),
            "tools": a["reqs"].get(rid, {}).get("tools", []),
        }
        chars = 0
        for b in m.get("content") or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text":
                chars += len(b.get("text", ""))
            elif b.get("type") == "thinking":
                chars += len(b.get("thinking", ""))
            elif b.get("type") == "tool_use":
                chars += len(json.dumps(b.get("input", {})))
                if (rid, b["id"]) not in a["seen"]:
                    a["seen"].add((rid, b["id"]))
                    a["tools"][b["name"]] += 1
                    label = b["name"]
                    if b["name"] in SUBAGENT_TOOLS:
                        label = f"{b['name']}: {b['input'].get('description', '')[:40]}"
                    a["reqs"][rid]["tools"].append(label)
        req_chars[(p, rid)] = max(req_chars[(p, rid)], chars)

    if not agents:
        sys.exit("no assistant records found — is this an audit.jsonl?")

    # Output-token estimation: per-request usage can't be trusted for output,
    # so distribute the authoritative modelUsage total by generated chars.
    # Subagent final reports live only in the parent's tool_results — fold in.
    chars_by_agent = collections.Counter()
    for (p, rid), c in req_chars.items():
        chars_by_agent[p] += c
    for tid, size in report_chars.items():
        if tid in agents:
            chars_by_agent[tid] += size
    total_chars = sum(chars_by_agent.values()) or 1
    main_model = agents["MAIN"]["model"]
    out_total = model_usage.get(main_model, {}).get("outputTokens", 0)

    # Server-side search model (e.g. Haiku behind WebSearch): appears only in
    # modelUsage, never as an agent. Split evenly across WebSearch calls.
    search_models = {m: mu for m, mu in model_usage.items()
                     if m != main_model and mu.get("webSearchRequests", 0) > 0}
    ws_by_agent = {p: a["tools"].get("WebSearch", 0) for p, a in agents.items()}
    ws_total = sum(ws_by_agent.values()) or 1

    t0 = min(parse_ts(a["first"]) for a in agents.values())
    summary = []
    for p, a in agents.items():
        inp = sum(q["inp"] for q in a["reqs"].values())
        cr = sum(q["cr"] for q in a["reqs"].values())
        cc5 = sum(q["cc5"] for q in a["reqs"].values())
        cc1 = sum(q["cc1"] for q in a["reqs"].values())
        out = round(chars_by_agent[p] / total_chars * out_total)
        pi, po, pcr, pw5, pw1 = price_for(a["model"])
        cost = (inp * pi + out * po + cr * pcr + cc5 * pw5 + cc1 * pw1) / 1e6
        n_ws = ws_by_agent[p]
        h_in = h_out = 0
        h_cost = 0.0
        for m, mu in search_models.items():
            share = n_ws / ws_total
            si, so = price_for(m)[:2]
            h_in += round(share * mu["inputTokens"])
            h_out += round(share * mu["outputTokens"])
            h_cost += (share * mu["inputTokens"] * si + share * mu["outputTokens"] * so) / 1e6
        h_cost += n_ws * WEB_SEARCH_FEE
        summary.append({
            "id": p, "name": "Main agent" if p == "MAIN" else names.get(p, p[-8:]),
            "model": a["model"], "requests": len(a["reqs"]),
            "inp": inp, "cr": cr, "cc": cc5 + cc1, "out_est": out,
            "ws": n_ws, "search_in": h_in, "search_out": h_out,
            "cost_agent": round(cost, 4), "cost_search": round(h_cost, 4),
            "cost": round(cost + h_cost, 4),
            "t0": round((parse_ts(a["first"]) - t0).total_seconds()),
            "t1": round((parse_ts(a["last"]) - t0).total_seconds()),
            "tools": dict(a["tools"]),
        })
    summary.sort(key=lambda x: (x["id"] != "MAIN", -x["cost"]))

    # Per-agent turn timelines. Per-request output is estimated by
    # distributing the agent's output share over its requests by chars.
    timelines = {}
    agent_out = {s["id"]: s["out_est"] for s in summary}
    for p, a in agents.items():
        req_char_total = sum(req_chars[(p, rid)] for rid in a["reqs"]) or 1
        tl = []
        for rid, q in a["reqs"].items():
            tl.append({
                "t": round((parse_ts(q["t"]) - t0).total_seconds()),
                "cr": q["cr"], "cc": q["cc5"] + q["cc1"], "inp": q["inp"],
                "out": round(req_chars[(p, rid)] / req_char_total * agent_out[p]),
                "tools": q["tools"] or ["(text only)"],
            })
        tl.sort(key=lambda x: x["t"])
        timelines[p] = tl
    timeline = timelines["MAIN"]

    total_actual = (result or {}).get("total_cost_usd")
    total_recon = round(sum(x["cost"] for x in summary), 4)
    return {
        "agents": summary, "timeline": timeline, "timelines": timelines,
        "total_cost_actual": total_actual, "total_cost_reconstructed": total_recon,
        "unattributed": round(total_actual - total_recon, 4) if total_actual else None,
        "num_turns": (result or {}).get("num_turns"),
        "duration_s": round((result or {}).get("duration_ms", 0) / 1000),
        "model_usage": model_usage,
    }


def render_html(d):
    data = json.dumps({k: d[k] for k in ("agents", "timelines", "total_cost_actual",
                                         "unattributed", "num_turns", "duration_s")})
    total = d["total_cost_actual"] or d["total_cost_reconstructed"]
    n_req = sum(a["requests"] for a in d["agents"])
    n_ws = sum(a["ws"] for a in d["agents"])
    dur = f"{d['duration_s'] // 60}m {d['duration_s'] % 60}s"
    kpis = "".join(
        f'<div class="kpi"><div class="kl">{k}</div><div class="kv">{v}</div></div>'
        for k, v in [("Total cost", f"${total:.2f}"), ("Agents", len(d["agents"])),
                     ("API requests", n_req), ("Web searches", n_ws), ("Wall clock", dur)])
    return """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Agent cost report</title>
<style>
body{font-family:-apple-system,Segoe UI,sans-serif;max-width:880px;margin:2rem auto;padding:0 1rem;color:#1a1a19;background:#fff}
h2{font-size:18px;font-weight:600;margin:1.5rem 0 .5rem}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px}
.kpi{background:#f5f4ef;border-radius:8px;padding:1rem}.kl{font-size:13px;color:#898781}.kv{font-size:24px;font-weight:600}
.grid{display:grid;grid-template-columns:1.1fr 1fr;gap:16px;align-items:start}
.row{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:8px;cursor:pointer;border:1px solid transparent}
.row:hover{background:#f5f4ef}.row.sel{background:#f5f4ef;border-color:#c3c2b7}
.bar{flex:1;height:14px;background:#f0efec;border-radius:3px;overflow:hidden}.bar span{display:block;height:100%}
.card{background:#fff;border:1px solid #e1e0d9;border-radius:12px;padding:1rem 1.25rem;position:sticky;top:8px}
table{width:100%;font-size:13px;border-collapse:collapse}td{padding:3px 0}
.sw{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px}
.tl div.ev{display:flex;gap:10px;padding:4px 0;border-bottom:1px solid #eee;font-size:13px;align-items:baseline}
.mut{color:#898781}.sec{color:#52514e}svg{width:100%;height:auto}
</style></head><body>
<h1 style="font-size:22px">Agent session cost report</h1>
<div class="kpis">""" + kpis + """</div>
<h2>Agents — click to inspect</h2>
<div class="grid"><div id="list"></div><div id="detail" class="card"></div></div>
<h2 id="tlh">Turn timeline</h2>
<div id="ctx"></div><div id="tl" class="tl"></div>
<script>
const D=""" + data + """;
const A=D.agents;const COLORS={out:'#2a78d6',cc:'#6ba3e3',cr:'#b3cff0',inp:'#dce9f8',sin:'#1baf7a',sout:'#5cc9a0',fee:'#eda100'};
const RATES={'claude-sonnet':[3,15,.3,6],'claude-haiku':[1,5,.1,2],'claude-opus':[5,25,.5,10],'claude-fable':[5,25,.5,10]};
function rate(m){for(const k in RATES)if(m.startsWith(k))return RATES[k];return RATES['claude-sonnet']}
function comp(a){const[pi,po,pcr,pcw]=rate(a.model);return[
 ['Output (est.)',a.out_est*po/1e6,COLORS.out,a.out_est+' tk'],
 ['Cache write',a.cc*pcw/1e6,COLORS.cc,a.cc.toLocaleString()+' tk'],
 ['Cache read',a.cr*pcr/1e6,COLORS.cr,a.cr.toLocaleString()+' tk'],
 ['Fresh input',a.inp*pi/1e6,COLORS.inp,a.inp.toLocaleString()+' tk'],
 ['Search model input',a.search_in*1/1e6,COLORS.sin,a.search_in.toLocaleString()+' tk'],
 ['Search model output',a.search_out*5/1e6,COLORS.sout,a.search_out.toLocaleString()+' tk'],
 ['Web search fees',a.ws*0.01,COLORS.fee,a.ws+' calls']].filter(x=>x[1]>0)}
const max=Math.max(...A.map(a=>a.cost));
document.getElementById('list').innerHTML=A.map((a,i)=>
 '<div class="row" data-i="'+i+'"><span style="min-width:110px;font-size:13px">'+a.name+'</span>'+
 '<span class="bar"><span style="width:'+Math.round(a.cost/max*100)+'%;background:'+(a.id==='MAIN'?'#2a78d6':'#1baf7a')+'"></span></span>'+
 '<span style="min-width:48px;text-align:right;font-size:13px">$'+a.cost.toFixed(2)+'</span></div>').join('');
const mmss=s=>Math.floor(s/60)+':'+String(s%60).padStart(2,'0');
const fk=v=>v>=1000?(v/1000).toFixed(v>=10000?0:1)+'k':''+v;
function drawTimeline(a){
 const T=D.timelines[a.id]||[];
 document.getElementById('tlh').textContent=a.name+' — turn timeline ('+T.length+' API requests)';
 if(!T.length){document.getElementById('ctx').innerHTML='';document.getElementById('tl').innerHTML='<span class="mut">no logged requests for this agent</span>';return}
 let cum=0;const C=T.map(r=>cum+=r.out);
 const W=840,H=220,P=46;
 const mx=Math.max(...T.map(r=>Math.max(r.cr,r.cc)),cum,1);
 const x=i=>P+i*(W-P-10)/Math.max(1,T.length-1),y=v=>H-24-v/mx*(H-40);
 document.getElementById('ctx').innerHTML='<svg viewBox="0 0 '+W+' '+H+'">'+
  T.map((r,i)=>'<rect x="'+(x(i)-5)+'" y="'+y(r.cc)+'" width="10" height="'+Math.max(1,H-24-y(r.cc))+'" fill="#eda100"/>').join('')+
  '<polyline fill="none" stroke="#2a78d6" stroke-width="2" points="'+T.map((r,i)=>x(i)+','+y(r.cr)).join(' ')+'"/>'+
  T.map((r,i)=>'<circle cx="'+x(i)+'" cy="'+y(r.cr)+'" r="3" fill="#2a78d6"/>').join('')+
  '<polyline fill="none" stroke="#1baf7a" stroke-width="2" stroke-dasharray="5 3" points="'+C.map((v,i)=>x(i)+','+y(v)).join(' ')+'"/>'+
  '<text x="'+P+'" y="12" font-size="11" fill="#898781">blue: context reused (cache read) · amber bars: new context written · green dashed: cumulative output (est.) — peak '+fk(mx)+' tk</text></svg>';
 document.getElementById('tl').innerHTML=T.map((r,i)=>{
  const gap=i>0?r.t-T[i-1].t:0,dcr=i>0?r.cr-T[i-1].cr:r.cr;
  return (gap>60?'<div class="mut" style="padding:4px 0 4px 48px;font-size:12px">'+mmss(gap)+' elapsed (tools / subagents running)</div>':'')+
  '<div class="ev"><span class="mut" style="min-width:38px">'+mmss(r.t)+'</span><b style="min-width:190px;font-weight:600">'+r.tools.join(', ')+'</b>'+
  '<span class="sec" style="flex:1">ctx '+fk(r.cr)+(dcr>500?' <span style="color:#1baf7a">(+'+fk(dcr)+')</span>':'')+
  (r.cc>500?' · wrote '+fk(r.cc):'')+(r.out>100?' · out ~'+fk(r.out):'')+'</span></div>'}).join('');
}
function show(i){document.querySelectorAll('.row').forEach((e,j)=>e.classList.toggle('sel',i===j));
 const a=A[i],cs=comp(a),tot=cs.reduce((s,x)=>s+x[1],0);
 document.getElementById('detail').innerHTML=
 '<div style="display:flex;align-items:baseline"><b>'+a.name+'</b><span style="margin-left:auto;font-size:20px;font-weight:600">$'+a.cost.toFixed(2)+'</span></div>'+
 '<div class="mut" style="font-size:12px;margin:2px 0 10px">'+a.model+' · '+a.requests+' requests · '+(a.ws?a.ws+' searches · ':'')+(a.t1-a.t0)+'s active</div>'+
 '<div style="display:flex;height:16px;border-radius:4px;overflow:hidden;margin-bottom:12px">'+
 cs.map(x=>'<span style="width:'+(x[1]/tot*100)+'%;background:'+x[2]+'"></span>').join('')+'</div>'+
 '<table>'+cs.map(x=>'<tr><td><span class="sw" style="background:'+x[2]+'"></span>'+x[0]+'</td><td class="sec" style="text-align:right">'+x[3]+'</td><td style="text-align:right;min-width:56px">$'+x[1].toFixed(3)+'</td></tr>').join('')+'</table>';
 drawTimeline(a)}
document.getElementById('list').onclick=e=>{const r=e.target.closest('.row');if(r)show(+r.dataset.i)};show(0);
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audit", help="path to audit.jsonl")
    ap.add_argument("-o", "--out", default="agent_cost_report.html")
    ap.add_argument("--json", action="store_true", help="print full JSON instead of table")
    args = ap.parse_args()

    d = analyze(args.audit)
    if args.json:
        print(json.dumps(d, indent=1))
    else:
        print(f"total cost: ${d['total_cost_actual']:.3f} | reconstructed: "
              f"${d['total_cost_reconstructed']:.3f} | unattributed: ${d['unattributed'] or 0:.3f}")
        print(f"{'agent':<24}{'cost':>8}{'reqs':>6}{'ws':>4}{'cache read':>12}{'cache write':>12}{'out(est)':>10}")
        for a in d["agents"]:
            print(f"{a['name'][:23]:<24}{a['cost']:>8.3f}{a['requests']:>6}{a['ws']:>4}"
                  f"{a['cr']:>12,}{a['cc']:>12,}{a['out_est']:>10,}")
    with open(args.out, "w") as f:
        f.write(render_html(d))
    print(f"\nreport written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
