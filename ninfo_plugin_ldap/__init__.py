from ninfo import PluginBase

class ldap_plugin(PluginBase):
    """This plugin looks up a user in ldap and returns their information"""

    name = "ldap"
    title = "LDAP"
    description = "LDAP Lookup"
    cache_timeout = 60*60
    types = ['username']

    def setup(self):
        c = self.plugin_config
        import ldap
        self.ldap = ldap
        ldap_user   = c['user']
        ldap_pw     = c['pw']
        server      = c['server']
        dsn         = c['dsn']
        search      = c.get('search', 'uid=%s')
        strip       = c.get('strip', '')
        ignore_cert = 'ignore_cert' in c
        if ignore_cert:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)

        self.l = ldap.initialize(server)
        self.l.simple_bind_s(ldap_user, ldap_pw)
        self.dsn = dsn
        self.search = search
        self.strip = strip

    def get_info(self, arg):
        search = self.search.replace("%s", arg)
        res = self.l.search_s(self.dsn, self.ldap.SCOPE_SUBTREE, search)
        if not res:
            return None
        
        return {'records': res, 'strip': self.strip}

plugin_class = ldap_plugin
