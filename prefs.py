from iaprefs import InteractivePrefs

class AppsearchPrefs(InteractivePrefs):
    def keys(self):
        return { 
                'lang': {
                    'desc': 'The Store which the workflow should search (en, de, uk, ...)',
                    'default' : 'en'
                }
        }