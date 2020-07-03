#!/usr/bin/python
# encoding: utf-8
import sys
import time
import json
import re
from workflow import web
from workflow import Workflow
def strrepl(m):
    g = m.group()
    return '"' + g[0:-1] + '":'
def toJson(data):
    p = re.compile(r'\w+:')
    s = data.replace("\'", '"').replace('\n', " ")
    return json.loads(p.sub(strrepl, s))

def main(wf):
    if len(wf.args[1]) < 2:
        wf.add_item("At least two letters", subtitle="test", arg="At least two letters", valid=True)
        wf.send_feedback()
        return
    cmd = ''.join(wf.args[0])
    user_input = ''.join(wf.args)
    args = wf.args[1]
    args = ''.join(args).replace(" ", "")

    if wf.update_available:
        wf.add_item("An update is available!",
                    autocomplete='workflow:update', valid=False)
    results =  wf.cached_data('uib_'+cmd+'_'+args, max_age=60*60*24*7*52) # a year
    if results is None:
        url = ''
        if 'stav' in cmd:
            url = 'https://ordbok.uib.no/perl/lage_ordliste_liten_nr2000.cgi?spr=begge&query=' + args
        elif 'nn' in cmd:
            url = 'https://ordbok.uib.no/perl/lage_ordliste_liten_nr2000.cgi?spr=nynorsk&query=' + args
        elif 'bm' in cmd:
            url ='https://ordbok.uib.no/perl/lage_ordliste_liten_nr2000.cgi?spr=bokmaal&query=' + args
            # begge
        r = web.get(url)
        if r.status_code != 200:
            wf.add_item("No matches", arg="no matches", valid=True)
            wf.send_feedback()
            return
        results = toJson(r.text)
        data = results['suggestions']
        wf.cache_data('uib_'+cmd+'_'+args, data)
        results = data
    data = result
    if data:
        for unit in data:
            title = wf.decode(unit)
            #print(title)
            wf.add_item(title, arg=title, valid=True)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'mrlys/uibwf',
        'version': 'v0.1.0',
    })
    sys.exit(wf.run(main))

