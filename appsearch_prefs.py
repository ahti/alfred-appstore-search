# -*- coding: utf-8 -*-

import alp
import string
import sys

def keys():
    return { 
            'lang': {
                'desc': 'The Store which the workflow should search (en, de, uk, ...)',
                'default' : 'en'
            }
    }
    

def complete(query):
    split = query.split(None, 1)
    
    prefs = alp.Settings()
    
    items = []
    
    def add_item(key, dict):
        desc, default = dict['desc'], dict['default']
        val = prefs.get(key, default)
           
        title = 'Change {} (current: "{}")'.format(key, val)
           
        item = alp.Item(title = title,
                        subtitle = desc,
                        uid = key,
                        valid = False,
                        autocomplete = key + ' ',
                        arg = '')
        items.append(item)
    
    def add_no_matching(key):
        item = alp.Item(title = 'No preference found',
                        subtitle = 'Sorry, there is no preference named {}.'.format(key),
                        uid = '',
                        valid = False,
                        autocomplete = '',
                        arg = '')
        items.append(item)
    
    if len(split) == 1:
        # we have a (potentially incomplete) keyword
        # look for completions and direct matches and print
        # feedback items
        query_key = split[0].strip()
        
        if query_key in keys():
            add_item(query_key, keys()[query_key])
        
        filtered = {key: val for key, val in keys().iteritems() if key.startswith(query_key) and key != query_key}
        
        if len(filtered) == 0 and not query_key in keys():
            add_no_matching(query_key)
        
        for key, dict in filtered.iteritems():
            add_item(key, dict)
            
        
    elif len(split) == 2:
        # we have a keyword and a value, verify keyword
        # and print a feedback to save the value
        query_key = split[0].strip()
        query_val = split[1].strip()
        
        if not query_key in keys():
            add_no_matching(query_key)
        else:
            dict = keys()[query_key]
            desc, default = dict['desc'], dict['default']
            val = prefs.get(query_key, default)
            
            title = 'Change {} to "{}" (current: "{}")'.format(query_key, query_val, val)
            
            item = alp.Item(title = title,
                        subtitle = desc,
                        uid = query_key,
                        valid = True,
                        autocomplete = query,
                        arg = '{} {}'.format(query_key, query_val))
            items.append(item)
        
    else:
        # we have nothing, just dump out all keys we have
        for key, dict in keys().iteritems():
            add_item(key, dict)
            
    alp.feedback(items)
    
def execute(query):
    key, val = query.split(None, 1)
    prefs = alp.Settings()
    
    args = { key: val }
    
    prefs.set(**args)
    
if __name__ == '__main__':
    execute(string.join(sys.argv[1:]))