# -*- coding: utf-8 -*-
"""One-time migration record, already applied. Do not rerun on migrated HTML."""
from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parents[2]

def svg(body, title, height=330):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {}" role="img" aria-label="{}" style="display:block;width:100%;height:auto;font-family:Microsoft YaHei,Segoe UI,sans-serif"><title>{}</title>{}</svg>'.format(height, escape(title, quote=True), escape(title), body)

def text(x,y,s,size=16,fill='#202b36',anchor='start'):
    return '<text x="{}" y="{}" font-size="{}" fill="{}" text-anchor="{}">{}</text>'.format(x,y,size,fill,anchor,escape(str(s)))

def bars(items, title, minimum=0, maximum=1, band=None, integer=False):
    # Real baseline and explicit tick labels; raw values remain readable in the SVG.
    height=105+len(items)*55
    body=text(18,27,title,19)
    x0,w=155,490
    if band:
        left=x0+w*(band[0]-minimum)/(maximum-minimum)
        body+='<rect x="{}" y="45" width="{}" height="{}" fill="#e4ece9"/>'.format(left,w*(band[1]-band[0])/(maximum-minimum),len(items)*55)
    for j in range(5):
        val=minimum+(maximum-minimum)*j/4
        body+=text(x0+w*j/4,height-15,format(val,',.0f') if integer else '{:.2f}'.format(val),13,'#526274','middle')
    for i,(label,value) in enumerate(items):
        y=52+i*55
        width=w*(value-minimum)/(maximum-minimum)
        body+=text(140,y+23,label,17,anchor='end')
        body+='<rect x="{}" y="{}" width="{}" height="32" fill="{}"><title>{}: {}</title></rect>'.format(x0,y,max(1,width),'#16409e' if i==0 else '#6686af',escape(label),value)
        body+=text(x0+max(1,width)+10,y+23,format(value,',') if integer else '{:.4f}'.format(value),17)
    return svg(body,title,height)

def paired(counts,title):
    total=sum(counts)
    labels=['更高','同分','更低']
    body=text(18,28,title,19)
    start=20
    for i,(label,count,color) in enumerate(zip(labels,counts,['#16409e','#596a7c','#9b5140'])):
        width=760*count/total
        body+='<rect x="{}" y="55" width="{}" height="50" fill="{}"><title>{}：{:,}</title></rect>'.format(start,width,color,label,count)
        body+=text(start+width/2,87,'{:.1f}%'.format(count/total*100),16,'white','middle')
        body+=text(20+i*260,145,'{}：{:,}（{:.1f}%）'.format(label,count,count/total*100),16)
        start+=width
    return svg(body,title,175)

CSS='''
:root{--paper:#f7f8f8;--ink:#18222d;--muted:#4c5d6d;--accent:#16409e;--wash:#eaf0f6}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 "Microsoft YaHei","Segoe UI",sans-serif;font-variant-numeric:tabular-nums}a{color:var(--accent);text-underline-offset:4px}a:hover{text-decoration-thickness:2px}button:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:4px}.wrap{width:min(1180px,100%);margin:auto;padding-left:32px;padding-right:32px}h1,h2,h3,p,figure{margin:0}h1{font-size:clamp(40px,6vw,76px);line-height:1.13;letter-spacing:-.03em}h2{font-size:clamp(27px,3vw,38px);line-height:1.3;margin-bottom:24px}h3{font-size:21px;margin-bottom:14px}p+p{margin-top:18px}code{overflow-wrap:anywhere;font-size:.88em}nav{display:flex;gap:24px;flex-wrap:wrap}.site-header,.hero-nav{display:flex;justify-content:space-between;align-items:center;gap:24px;padding-top:26px;padding-bottom:26px}.wordmark,.brand{font-weight:bold;font-size:21px}.hero{padding-top:64px;padding-bottom:64px}.hero.wrap{display:grid;grid-template-columns:1.2fr 1fr;gap:38px}.hero-copy p{max-width:590px;margin-top:28px}.primary-action,.hero-action{display:inline-block;margin-top:28px;padding:12px 22px;background:var(--accent);color:white;text-decoration:none}.hero-figure{display:grid;place-items:center;background:var(--wash);padding:36px}.sun-value{display:block;font-size:66px;line-height:1.3;font-weight:bold;color:var(--accent)}.sun-caption{display:block}.hero-caveat{grid-column:1/-1;color:var(--muted);font-size:15px}.hero-inner h1 span{display:block}.hero-nav{padding-top:0;margin-bottom:60px}.hero-bottom,.sample-inner,.ledger-values,.leaders{display:flex;justify-content:space-between;gap:32px}.hero-bottom{margin-top:40px}.hero-bottom strong,.sample-number strong,.sample-side>strong,.ledger-values strong{display:block;font-size:clamp(30px,4vw,48px);line-height:1.4}.hero-bottom span,.sample-number span,.ledger-values span{display:block}.hero-bottom p{max-width:500px}.section{padding-top:76px;padding-bottom:76px}.section-heading,.section-intro,.ledger-title{max-width:850px;margin-bottom:34px}.sample-band,.paired,.subset,.coverage,.questions{background:var(--wash)}.sample-band{padding:44px 0}.sample-inner>*{flex:1}.sample-side p{font-size:15px;margin-top:16px}.figure{margin-top:28px;background:white;padding:22px;min-width:0}.figure svg{max-width:100%}figcaption{font-size:14px;color:var(--muted);margin-top:18px}.paired-layout,.subset-layout,.coverage-layout,.figure-pair{display:grid;grid-template-columns:1fr 1.3fr;gap:38px;align-items:start}.paired.wrap{background:var(--paper)}.anomaly .figure-pair{grid-template-columns:1.4fr 1fr}.anomaly-note{padding-top:30px}.metric-demo,.metric-workspace{display:grid;grid-template-columns:1fr 1.5fr;gap:36px;margin-top:32px;background:white;padding:28px}.metric-buttons{display:flex;gap:10px;margin:20px 0;flex-wrap:wrap}button{font:inherit;padding:9px 15px;background:var(--wash);border:0;cursor:pointer;color:var(--ink)}button.is-active,button.active{background:var(--accent);color:white}button:disabled{opacity:.65;cursor:not-allowed}.metric-row{display:grid;grid-template-columns:92px 1fr 70px;gap:10px;align-items:center;margin:14px 0}.track{background:var(--wash);height:24px}.track i{display:block;height:100%;background:var(--accent)}.metric-note{font-size:15px;color:var(--muted)}.rankings>div{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid #dbe1e7}.leaders{padding:28px 0}.leaders>div{flex:1}.leaders span,.leaders strong,.leaders em{display:block}.leaders strong{font-size:30px}.leaders em{font-style:normal;color:var(--accent)}.method-grid,.method-steps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}.method strong{display:block;font-size:21px;margin-bottom:12px}.question-list details{padding:20px 0}summary{cursor:pointer;font-size:20px}details p{margin-top:16px}.qa{margin:28px 0}.daily-callout{margin-top:28px}.site-footer,.footer{background:#18222d;color:white;padding:42px 0}.footer-inner{display:flex;gap:32px;justify-content:space-between;align-items:start}.footer a,.site-footer a{color:#b9d2ff}.footer-inner>div a{display:block}.footer-inner p{font-size:15px;max-width:520px}.data-note{padding:16px;background:#edf2f7;color:#34465b;font-size:15px;margin-top:16px}.chart-scroll{overflow-x:auto}.chart-scroll>svg{min-width:620px}.reference-missing{padding:24px;background:#eef3f8}
@media(max-width:760px){.wrap{padding-left:18px;padding-right:18px}.site-header,.hero-nav,.footer-inner{flex-direction:column;align-items:flex-start}.hero.wrap,.paired-layout,.subset-layout,.coverage-layout,.figure-pair,.anomaly .figure-pair,.metric-demo,.metric-workspace{grid-template-columns:1fr}.hero{padding-top:32px;padding-bottom:40px}.section{padding-top:44px;padding-bottom:44px}.sample-inner,.hero-bottom,.ledger-values,.leaders{flex-direction:column;gap:24px}.sample-inner h2 br{display:none}.figure{padding:12px}.method-grid,.method-steps{grid-template-columns:1fr}.hero-nav{margin-bottom:36px}.hero-figure{padding:26px}.metric-demo,.metric-workspace{padding:18px}.metric-row{grid-template-columns:78px 1fr 65px;font-size:15px}nav{gap:16px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''

charts={
'pv-accuracy':{
'model-comparison':bars([('TFT',.8525),('日前最终',.8471),('LightGBM',.8450),('TimeXer',.8279)],'共同站点日 · RMSE 评分',.78,.88),
'paired-outcome':paired([148744,599942,194019],'日前最终相对 TFT · 942,705 个站点日'),
'low-score-window':bars([('10 月 20 日',.7964),('10 月 21 日',.7486),('10 月 22 日',.7950),('10 月 23 日',.8554)],'已知低分窗口 · RMSE 评分'),
'coverage':bars([('10 月 24 日',25424),('10 月 27 日',2275),('10 月 29 日',41984),('10 月 30 日',1)],'已知日期覆盖 · 站点数',0,50000,(43000,46000),True)},
'load-accuracy':{
'model-comparison':bars([('TimeXer',.7355),('最终标签',.7287),('DLinear',.7281),('Rule',.7225)],'共同站点日 · RMSE 评分',.70,.75),
'paired-timeXer':paired([375298,184059,500106],'最终标签相对 TimeXer · 1,059,463 个站点日'),
'grid-cohort':bars([('最终标签',.7519),('TimeXer',.7514),('DLinear',.7464),('GridXGB',.7396),('Rule',.7388)],'GridXGB 共同子集 · RMSE 评分',.72,.76),
'daily-trend':bars([('10 月 16 日',.7134),('10 月 20 日',.7412),('10 月 26 日',.7125),('10 月 29 日',.7245)],'已知四日 · RMSE 评分（非完整日序列）'),
'coverage':bars([('10 月 {} 日'.format(d),v) for d,v in zip(range(24,31),[31633,48185,48358,43561,48745,48770,5])],'去重后覆盖 · 站点数',0,55000,(44000,49000),True)}}

for name, figures in charts.items():
    path=ROOT/(name+'-20261031.html')
    source=path.read_text(encoding='utf-8')
    source=re.sub(r'  <link rel="stylesheet"[^>]+>',lambda m:'  <style>'+CSS+'</style>',source)
    source=re.sub(r'  <script src="[^"]+" defer></script>','',source)
    for filename,chart in figures.items():
        source=re.sub(r'<img\b[^>]*src="assets/'+name+'/'+filename+r'\.png"[^>]*>',lambda m:'<div class="chart-scroll">'+chart+'</div>',source)
    source=re.sub(r'<button type="button" data-metric="(mape|mae)" aria-pressed="false">',r'<button type="button" data-metric="\1" aria-pressed="false" disabled title="页面未保留完整四模型数据">',source)
    note='<p class="data-note">当前仅可核对完整 RMSE 排名；原始报告和脚本未随页面提供，MAPE / MAE 缺少四模型完整数据，因此暂不可切换。已有单项数值保留在正文中。</p>'
    source=source.replace('<div class="metric-buttons"',note+'<div class="metric-buttons"',1)
    source=source.replace('10月1至29日最终标签日均 RMSE 评分折线','已知四日的最终标签 RMSE 评分')
    source=source.replace('10 月 30 日仅有 5 站，未放入趋势线。趋势线中的日均分按当天去重后的站点等权计算。','仅展示页面保留的 16、20、26、29 日数值；其余日期没有原始数据，不连线、不插值。10 月 30 日仅有 5 站，未纳入。日均分按当天去重后的站点等权计算。')
    source=source.replace('图中横轴从 0.78 起','图中横轴从 0.78 起')
    path.write_text(source,encoding='utf-8')

# Existing detailed SVGs are stronger evidence than an invented reconstruction.
architecture=(ROOT/'pv-forecast 架构.html').read_text(encoding='utf-8')
source=(ROOT/'index.html').read_text(encoding='utf-8')
for filename,label in [('pv-timexer-architecture','TimeXer 结构'),('pv-tft-v9-architecture','TFT 的来源注意力结构'),('pv-lgbm-architecture','LightGBM 的逐点特征与树模型')]:
    match=re.search(r'<svg\b[^>]*aria-label="'+label+r'"[\s\S]*?</svg>',architecture)
    chart=match.group().replace('<svg ','<svg style="display:block;width:100%;min-width:780px;height:auto" ',1)
    source=re.sub(r'<img\b[^>]*src="assets/images/'+filename+r'\.svg"[^>]*>',lambda m:'<div style="overflow-x:auto">'+chart+'</div><p>复用《PV 预测架构》中的模型说明图。</p>',source)
    source=re.sub(r'<a href="assets/images/'+filename+r'\.svg">[^<]+</a>','<a href="pv-forecast 架构.html">查看模型架构详解</a>',source)

def flow(steps,title):
    body=text(24,30,title,22)
    for i,(heading,desc) in enumerate(steps):
        y=58+i*90
        body+='<rect x="24" y="{}" width="752" height="66" fill="{}"/>'.format(y,'#edf2f8' if i%2==0 else '#e2eaf4')
        body+=text(44,y+27,heading,19)+text(44,y+51,desc,15,'#4c5d6d')
        if i<len(steps)-1: body+=text(400,y+85,'↓',21,'#16409e','middle')
    return svg(body,title,70+90*len(steps))

for filename,steps,title in [
('load-business-architecture',[('任务入口','POST /load_prediction_station · station_id；旧节假日入口保留独立语义'),('算法服务准备数据','查询站点、本地日期、历史负荷、日历及节假日'),('批量预测','DLinear / TimeXer 加模型锁；XGBoost 权重失败时本地 fallback'),('选优与兜底','基础预测 → 选优 / fallback → 最终结果'),('异步输出','Kafka / Redis / DB；写入失败重试与追踪')],'LOAD 异步预测 · 按本页文字整理'),
('pv-business-architecture',[('任务入口','POST /pv_prediction_station · station_id + 定时调度'),('数据与输入对齐','历史 PV + 多源 NWP + 本地日期；缺失站点同步剔除'),('三路基础预测','TimeXer / TFT / LightGBM 各自生成基础预测'),('日前选优','近 7 天历史表现 → select_best_7；D1 / D2 分开选'),('覆盖与最终输出','积雪 / 融雪、clipping、EC 等覆盖路径；Kafka / Redis 输出')],'PV 业务主线 · 按本页文字整理')]:
    chart=flow(steps,title)
    source=re.sub(r'<img\b[^>]*src="assets/images/'+filename+r'\.svg"[^>]*>',lambda m:'<div style="overflow-x:auto;max-width:900px">'+chart+'</div>',source)
    source=re.sub(r'<a href="assets/images/'+filename+r'\.svg">[^<]+</a>','<span>图示已内嵌，可离线阅读；表示业务主线。</span>',source)
source=source.replace('<img class="arch-img" src="assets/images/tft-v5.png" alt="TFT v5 allweather 架构图">','<div class="note">原始 TFT v5 allweather 参考图未随仓库提供，现有文字不足以还原其结构。可先阅读相邻的 TFT v9 图；两个版本不能视为同一架构。</div>')
source=source.replace('<a href="assets/images/tft-v5.png">打开参考图</a>','<a href="#pv-tft">查看已有 TFT v9 图</a>')
(ROOT/'index.html').write_text(source,encoding='utf-8')
print('Restored 9 inline charts and 5 architecture figures; marked missing TFT v5 reference.')
