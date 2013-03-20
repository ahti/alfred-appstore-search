# -*- coding: utf-8 -*-

import alp
import string
import sys

class InteractivePrefs(object):
    def keys(self):
        return {}
        
    
    def complete(self, query=""):
        split = query.split(None, 1)
        
        keys = self.keys()
        
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
            
        def add_change(key, dict, val, value_valid):
            desc, default = dict['desc'], dict['default']
            prev_val = prefs.get(key, default)
            
            if value_valid:
                title = 'Change {} to "{}" (current: "{}")'.format(key, val, prev_val)
            else:
                title = 'Invalid value for {} (curent: "{}")'.format(key, prev_val)
            
            item = alp.Item(title = title,
                        subtitle = desc,
                        uid = key,
                        valid = value_valid,
                        autocomplete = query,
                        arg = '{} {}'.format(key, val))
            items.append(item)
        
        if len(split) == 1 and not query.endswith(' '):
            # we have a (potentially incomplete) keyword
            # look for completions and direct matches and print
            # feedback items
            query_key = split[0].strip()
            
            if query_key in keys:
                add_item(query_key, keys[query_key])
            
            filtered = {key: val for key, val in keys.iteritems() if key.startswith(query_key) and key != query_key}
            
            if len(filtered) == 0 and not query_key in keys:
                add_no_matching(query_key)
            
            for key, dict in filtered.iteritems():
                add_item(key, dict)
                
            
        elif len(split) == 2 or len(split) == 1 and query.endswith(' '):
            # we have a keyword and possibly a value, verify keyword
            # and print a feedback to save the value
            query_key = split[0].strip()
            if len(split) == 2:
                query_val = split[1].strip()
            else:
                query_val = ''
            
            if not query_key in keys:
                add_no_matching(query_key)
            else:
                value_valid = self.validate_value(query_key, query_val)
                
                completions = self.completions(query_key)
                if completions == None:
                    completions = []
                completions = [a for a in completions if a.startswith(query_val) and a != query_val]
                
                if value_valid or not completions:
                    add_change(query_key, keys[query_key], query_val, value_valid)
                
                for completion in completions:
                    add_change(query_key, keys[query_key], completion, True)
            
        else:
            # we have nothing, just dump out all keys we have
            for key, dict in keys.iteritems():
                add_item(key, dict)
                
        alp.feedback(items)
        
    def execute(self, query):
        split = query.split(None, 1)
        
        key = split[0]
        
        if len(split) == 2:
            val = split[1]
        else:
            val = ''
             
        prefs = alp.Settings()
        
        args = { key: val }
        
        prefs.set(**args)
    
    def validate_value(self, key, value):
        return True
        
    def completions(self, key):
        return None