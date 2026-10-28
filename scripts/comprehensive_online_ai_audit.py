# -*- coding: utf-8 -*-
"""
Comprehensive Online AI Writing Detection Auditor.
Audits every section of the manuscript across 3 live online AI checkers:
1. ZeroGPT (https://api.zerogpt.com/api/detect/detectText)
2. PirateXX RoBERTa Detector (https://piratexx-ai-content-detector.hf.space)
3. RADAR (NeurIPS 2023 SOTA) (https://trustsafeai-radar-ai-text-detector.hf.space)
"""

import re
import json
import uuid
import time
import requests
from pathlib import Path

def get_zerogpt_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    session.get('https://www.zerogpt.com/')
    return session

def query_zerogpt(text, session):
    headers = {
        'Origin': 'https://www.zerogpt.com',
        'Referer': 'https://www.zerogpt.com/',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    url = 'https://api.zerogpt.com/api/detect/detectText'
    try:
        r = session.post(url, json={'input_text': text}, headers=headers, timeout=25)
        if r.status_code == 200:
            res = r.json()
            if res.get('success'):
                data = res.get('data', {})
                return {
                    'ai_pct': data.get('fakePercentage', 0.0),
                    'is_human_pct': data.get('isHuman', 100.0),
                    'highlighted': data.get('h', []),
                    'text_words': data.get('textWords', 0),
                    'ai_words': data.get('aiWords', 0)
                }
        return {'error': f"HTTP {r.status_code}"}
    except Exception as e:
        return {'error': str(e)}

def query_piratexx(text):
    space_url = 'https://piratexx-ai-content-detector.hf.space'
    session_hash = str(uuid.uuid4())[:8]
    try:
        r = requests.post(f'{space_url}/queue/join', json={'data': [text], 'fn_index': 0, 'session_hash': session_hash}, timeout=15)
        if r.status_code != 200:
            return {'error': f"join HTTP {r.status_code}"}
        r2 = requests.get(f'{space_url}/queue/data?session_hash={session_hash}', stream=True, timeout=20)
        for line in r2.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if 'process_completed' in decoded:
                    payload = json.loads(decoded.replace('data: ', ''))
                    out_data = payload.get('output', {}).get('data', [])
                    if out_data and isinstance(out_data[0], list) and len(out_data[0]) > 0:
                        first_item = out_data[0][0]
                        if isinstance(first_item, dict):
                            real_prob = first_item.get('Real', 1.0)
                            fake_prob = first_item.get('Fake', 0.0)
                            return {'human_pct': real_prob * 100, 'ai_pct': fake_prob * 100}
    except Exception as e:
        return {'error': str(e)}
    return {'error': 'timeout/empty'}

def query_radar(text):
    space_url = 'https://trustsafeai-radar-ai-text-detector.hf.space'
    session_hash = str(uuid.uuid4())[:8]
    try:
        r = requests.post(f'{space_url}/queue/join', json={'data': [text], 'fn_index': 0, 'session_hash': session_hash}, timeout=15)
        if r.status_code != 200:
            return {'error': f"join HTTP {r.status_code}"}
        r2 = requests.get(f'{space_url}/queue/data?session_hash={session_hash}', stream=True, timeout=25)
        for line in r2.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if 'process_completed' in decoded:
                    payload = json.loads(decoded.replace('data: ', ''))
                    out_data = payload.get('output', {}).get('data', [])
                    if out_data and isinstance(out_data[0], dict):
                        confs = out_data[0].get('confidences', [])
                        human_conf = next((c['confidence'] for c in confs if c['label'] == 'Human-written'), 1.0)
                        ai_conf = next((c['confidence'] for c in confs if c['label'] == 'AI-generated'), 0.0)
                        return {'human_pct': human_conf * 100, 'ai_pct': ai_conf * 100}
    except Exception as e:
        return {'error': str(e)}
    return {'error': 'timeout/empty'}

def clean_latex_to_plain_text(latex_str):
    text = latex_str
    # Remove comments
    text = re.sub(r'%.*?\n', '\n', text)
    # Remove labels cleanly before any other commands
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    # Ensure subsection titles end with period and space
    text = re.sub(r'\\subsection\*?\{([^}]*)\}', r'\1. ', text)
    text = re.sub(r'\\paragraph\*?\{([^}]*)\}', r'\1. ', text)
    # Remove equations, figures, tables, algorithms
    text = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{figure\*?\}.*?\\end\{figure\*?\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{table\*?\}.*?\\end\{table\*?\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{algorithm\}.*?\\end\{algorithm\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\input\{[^}]*\}', ' ', text)
    text = re.sub(r'\$\$.*?\$\$', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\$.*?\$', ' ', text)
    # Remove citation, cross-ref, and URL commands
    text = re.sub(r'\\cite\{[^}]*\}', '', text)
    text = re.sub(r'\\ref\{[^}]*\}', '', text)
    text = re.sub(r'\\eqref\{[^}]*\}', '', text)
    text = re.sub(r'\\url\{[^}]*\}', '', text)
    text = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\[a-zA-Z]+', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_manuscript_sections(tex_path="paper/main.tex"):
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = {}
    
    # Abstract
    abs_start = content.find(r'\abstract{')
    if abs_start != -1:
        # find matching brace for abstract
        brace_count = 0
        abs_text_chars = []
        started = False
        for ch in content[abs_start+len(r'\abstract{')-1:]:
            if ch == '{':
                brace_count += 1
                if not started:
                    started = True
                    continue
            elif ch == '}':
                brace_count -= 1
                if started and brace_count == 0:
                    break
            if started:
                abs_text_chars.append(ch)
        raw_abstract = "".join(abs_text_chars)
        sections['Abstract'] = clean_latex_to_plain_text(raw_abstract)

    # Split by \section{...}
    sec_splits = re.split(r'\\section\*?\{([^}]+)\}', content)
    for i in range(1, len(sec_splits), 2):
        title = sec_splits[i].strip()
        body = sec_splits[i+1]
        if 'bibliography' in title.lower():
            continue
        cleaned = clean_latex_to_plain_text(body)
        if len(cleaned.split()) >= 30:
            sections[title] = cleaned

    return sections

if __name__ == '__main__':
    sections = parse_manuscript_sections()
    session = get_zerogpt_session()

    print(f"Loaded {len(sections)} sections from manuscript.")
    results = {}
    
    for title, text in sections.items():
        words = len(text.split())
        print(f"\n=======================================================")
        print(f"Auditing Section: {title} ({words} words)")
        print(f"=======================================================")
        
        sample_chunk = " ".join(text.split()[:250])
        
        z_res = query_zerogpt(sample_chunk, session)
        p_res = query_piratexx(sample_chunk)
        r_res = query_radar(sample_chunk)
        
        z_pct = z_res.get('ai_pct', 'ERR')
        p_pct = p_res.get('ai_pct', 0.0) if 'ai_pct' in p_res else 'ERR'
        r_pct = r_res.get('ai_pct', 0.0) if 'ai_pct' in r_res else 'ERR'
        
        print(f"1. ZeroGPT:     {z_pct}% AI  (Human: {z_res.get('is_human_pct', 'ERR')}%)")
        if z_res.get('highlighted'):
            print(f"   -> Flagged: {z_res['highlighted']}")
        if isinstance(p_pct, (int, float)):
            print(f"2. PirateXX:    {p_pct:.2f}% AI  (Human: {p_res.get('human_pct', 0.0):.2f}%)")
        else:
            print(f"2. PirateXX:    {p_pct}")
        if isinstance(r_pct, (int, float)):
            print(f"3. RADAR:       {r_pct:.2f}% AI  (Human: {r_res.get('human_pct', 0.0):.2f}%)")
        else:
            print(f"3. RADAR:       {r_pct}")
            
        results[title] = {
            'words': words,
            'zerogpt': z_res,
            'piratexx': p_res,
            'radar': r_res
        }
        time.sleep(1)

    with open("results/online_ai_audit_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nSaved comprehensive results to results/online_ai_audit_results.json")
