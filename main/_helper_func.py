_status = {
            'admin': 'admin',
            'driver': 'driver',
            'director': 'director',
            'engineer': 'engineer',
            'undefined': 'undefined',
        }

def _whoisit(user):
        
        if user.is_superuser:
            return(_status['admin'])
        
        elif hasattr(user, 'seniordriver'):
            return(_status['driver'])
        
        elif hasattr(user, 'director'):
            return(_status['director'])

        elif hasattr(user, 'engineer'):
            return(_status['engineer'])      

        else:
            return(_status['undefined'])