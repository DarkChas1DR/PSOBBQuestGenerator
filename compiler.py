"""Deterministic Episode 1 BB compiler; exported quests require native tests."""
from pathlib import Path
import json,struct,subprocess,os,shutil,hashlib,math

def integer(v,lo,hi,name):
    if type(v) is not int or not lo<=v<=hi:raise ValueError(f'{name} must be {lo}..{hi}')
    return v

def vector(v,name):
    if not isinstance(v,list) or len(v)!=3 or any(type(x) not in (int,float) or not math.isfinite(x) or abs(x)>1e7 for x in v):raise ValueError('Invalid '+name)
    return v

def record(x,enemy=False):
    size=0x48 if enemy else 0x44;b=bytearray(size)
    typ=integer(x['type'],0,65535,'type');floor=integer(x['floor'],0,255,'floor');room=integer(x['room'],0,65535,'room')
    if enemy:struct.pack_into('<10H',b,0,typ,0,0,integer(x.get('children',0),0,65535,'children'),floor,0,room,integer(x.get('wave',0),0,65535,'wave'),integer(x.get('wave2',0),0,65535,'wave2'),0)
    else:struct.pack_into('<8H',b,0,typ,0,0,floor,0,integer(x.get('group',0),0,65535,'group'),room,0)
    offset=0x14 if enemy else 0x10;struct.pack_into('<3f',b,offset,*vector(x['position'],'position'))
    angles=x.get('angles',[0,0,0])
    if not isinstance(angles,list) or len(angles)!=3:raise ValueError('Invalid angles')
    struct.pack_into('<3I',b,offset+12,*[integer(a,0,0xFFFFFFFF,'angle') for a in angles])
    params=x.get('params',[0]* (7 if enemy else 6))
    if len(params)!=(7 if enemy else 6):raise ValueError('Incorrect parameter count')
    floats=params[:5 if enemy else 3]
    if any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>1e30 for v in floats):raise ValueError('Invalid float parameter')
    ints=params[len(floats):];bits=16 if enemy else 32
    for v in ints:integer(v,-(1<<(bits-1)),(1<<(bits-1))-1,'parameter')
    struct.pack_into('<5f2h' if enemy else '<3f3i',b,0x2C if enemy else 0x28,*params)
    return bytes(b)

def section(t,f,payload):return struct.pack('<4I',t,len(payload)+16,f,len(payload))+payload

def prepare(plan):
    # Planning schema validator is shared with the AI adapter.
    from server import validate
    plan=validate(json.loads(json.dumps(plan)))
    if not plan['waves']:raise ValueError('At least one wave is required')
    floors={w['floor'] for w in plan['waves']}
    if len(floors)!=1:raise ValueError('Compiler currently supports one combat floor per quest')
    floor=next(iter(floors))
    if floor==0:raise ValueError('Combat floor must not be Pioneer 2')
    v=plan['waves'][0];signature=lambda x:tuple(x[k] for k in ('floor','area','layout','entities','map','table'))
    for x in plan['waves']+plan['npcs']:
        if signature(x)!=signature(v):raise ValueError('All entries must share the selected combat map')
    return plan,floor,v

def script(plan,floor,v,events):
    q=lambda s:json.dumps(s,ensure_ascii=True)
    # r200 floor-start guard; r201 completion; r202 actor IDs; r210-212 switch polling.
    lines=['.version BB_V4','.quest_num '+str(plan.get('questNumber',65000)),'.name '+q(plan['name']),'.short_desc '+q('Generated encounter - test build'),'.long_desc '+q(plan['brief'][:200]),'.episode Episode1','.header_episode 0','.language E','.max_players '+str(plan['party']),'start@0x0000:','  set_episode 0','  set_qt_success success','  set_qt_failure failure','  set_floor_handler 0, blank',f'  set_floor_handler {floor}, floor_ready','  bb_map_designate 0, 0, 0, 0, 0',f"  bb_map_designate {floor}, {v['area']}, 0, {v['layout']}, {v['entities']}",f'  initial_floor {floor}','  leti r200, 0','  leti r201, 0','  leti r253, 0','  leti r255, 0','  thread completion_monitor','  ret','blank@0x0001:','  ret','success@0x000A:','  window_msg '+q('Mission complete.'),'  window_msg_end','  ret','failure@0x000B:','  window_msg '+q('Mission failed.'),'  window_msg_end','  ret','floor_ready@0x0014:','  jmpi_ne r200, 0, blank','  leti r200, 1','  get_client_id r202','  get_leader_id r203','  jmp_ne r202, r203, blank',f"  start_setevt {floor}, {events[0]['id']}",'  ret','completion_monitor@0x001E:','  sync','  jmpi_eq r200, 0, completion_monitor',f'  leti r210, {floor}','  leti r211, 250','  read_switch_flag_on_floor r210-r212','  jmpi_eq r212, 0, completion_monitor','  get_client_id r202','  get_leader_id r203','  jmp_ne r202, r203, wait_completion','  sync_register2 r201, 1',f'  set_switch_flag_sync {floor}, 250',*[f'  set_switch_flag_sync {floor}, {d["switch"]}' for d in plan.get('doors',[])],'wait_completion@0x001F:','  sync','  jmpi_eq r201, 0, wait_completion','  leti r255, 1','  window_msg '+q('All waves cleared. Speak to the researcher to finish.'),'  window_msg_end','  ret']
    for i,n in enumerate(plan['npcs']):
        lines += [f"npc_{i}@0x{n['handler']:04X}:",'  jmpi_ne r201, 0, finish', '  window_msg '+q(n['dialogue']),'  window_msg_end','  ret']
    lines += ['finish@0x0028:','  window_msg '+q('Mission complete. The test quest will now end.'),'  window_msg_end','  qexit','  ret']
    return '\n'.join(lines)+'\n'

def build(plan,dest,tool):
    # Validate without discarding the authored spatial records (AI validation clears coordinates).
    original=json.loads(json.dumps(plan));plan,floor,v=prepare(plan)
    integer(original.get('questNumber',65000),1,65535,'quest number')
    if len(plan['name'].encode('utf-16-le'))>62:raise ValueError('Quest name exceeds BB header capacity')
    spawns=original.get('spawns',[])
    if len(spawns)!=4 or {x.get('slot') for x in spawns}!={0,1,2,3}:raise ValueError('Provide four explicit player spawn records, slots 0–3')
    from server import REF
    area=next(a for a in REF['floors'] if a['area']==v['area'])
    variant=next(x for x in area['variants'] if x['object_basename']==v['map'] and x['table']==v['table'] and x['layout']==v['layout'] and x['entities']==v['entities'])
    rooms=next(g['section_ids'] for g in REF['geometry'] if g['map']==variant['setup_basename'])
    for x in spawns+original.get('doors',[]):
        if x.get('room') not in rooms:raise ValueError('Object/spawn room is not in the selected map')
    for w in original['waves']:
        entity=next(d for d in REF['entities'] if d['id']==w['type'])
        if entity['constructor'].startswith('TBoss'):raise ValueError('Boss encounters require a dedicated supported preset')
    objects=[]
    for x in spawns:
        if x.get('floor')!=floor:raise ValueError('Spawn floor mismatch')
        objects.append(record(dict(x,type=0,params=[float(x['slot']),1.,1.,0,0,0])))
    switches=[]
    for d in original.get('doors',[]):
        if d.get('floor')!=floor or d.get('type')!=0x80 or v['area'] not in (1,2):raise ValueError('Only Forest Door 0x80 supported in this compiler')
        sw=integer(d['switch'],0,249,'door switch');switches.append(sw)
        params=d.get('params',[1.,1.,1.,0,0,0]).copy();params[3]=(params[3]&~255)|sw
        objects.append(record(dict(d,params=params)))
    groups={};enemy=[]
    for w in original['waves']:
        positions=w.get('positions',[])
        if len(positions)!=w['count']:raise ValueError('Each monster needs an explicit placement; AI count alone cannot compile')
        key=(w['room'],w['wave']);groups.setdefault(key,len(groups)+1000)
        for x in positions:enemy.append(record(dict(x,type=w['type'],floor=floor,room=w['room'],wave=w['wave']),True))
    used={0,1,10,11,20,30,31,40}
    if not original['npcs']:raise ValueError('One researcher NPC is required for the finish interaction')
    for i,n in enumerate(original['npcs']):
        handler=integer(n['handler'],100,65535,'NPC handler')
        if handler in used:raise ValueError('Duplicate or reserved handler')
        used.add(handler)
        if n.get('coordinateSpace')!='room-local':raise ValueError('NPC requires explicitly authored room-local coordinates')
        enemy.append(record(dict(n,angles=[0,integer(n.get('facing',0),0,65535,'facing'),0],params=[0.,0.,0.,float(100+i),float(handler),0,0]),True))
    events=[dict(id=i,room=r,wave=w) for (r,w),i in groups.items()];actions=bytearray();entries=bytearray()
    for i,e in enumerate(events):
        entries+=struct.pack('<IHHHHII',e['id'],0,1,e['room'],e['wave'],30,len(actions))
        if i+1<len(events):actions+=b'\x0c'+struct.pack('<I',events[i+1]['id'])
        else:
            for sw in switches+[250]:actions+=b'\x0a'+struct.pack('<H',sw)
        actions+=b'\x01'
    evt=struct.pack('<4I',16+len(entries),16,len(events),0)+entries+actions
    dat=section(1,floor,b''.join(objects))+section(2,floor,b''.join(enemy))+section(3,floor,evt)+bytes(16)
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True);base=dest/'quest'
    (dest/'quest.dat.dec').write_bytes(dat);(dest/'quest.txt').write_text(script(original,floor,v,events),encoding='utf-8')
    def run(*args):
        p=subprocess.run([str(tool),*map(str,args)],capture_output=True,timeout=60)
        if p.returncode:raise ValueError('Compiler failed: '+p.stderr.decode('utf-8','replace')[-2000:])
    run('assemble-quest-script',dest/'quest.txt',dest/'quest.bin','--bb')
    run('compress-prs',dest/'quest.dat.dec',dest/'quest.dat')
    run('encode-qst',dest/'quest.bin',dest/'quest.qst','--bb')
    run('disassemble-quest-script',dest/'quest.bin',dest/'script-check.txt','--bb')
    run('disassemble-quest-map',dest/'quest.dat',dest/'map-check.txt','--bb')
    report=dict(status='compiled; QEdit and client tests pending',compiler=str(Path(tool).name),compiler_sha256=hashlib.sha256(Path(tool).read_bytes()).hexdigest(),floor=floor,area=v['area'],events=events,monster_records=sum(w['count'] for w in original['waves']),npc_records=len(original['npcs']),object_records=len(objects),limitations=['One combat floor; no boss support','Difficulty is design intent; select matching server difficulty','Initial non-city spawn requires matching Episode 1 drop configuration','Completion sets local success flag and researcher interaction exits game; no rewards','Door actions and multiplayer behavior require client tests','No safe runtime capacity limits are asserted'])
    report['files']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in dest.iterdir() if f.is_file()}
    (dest/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report
