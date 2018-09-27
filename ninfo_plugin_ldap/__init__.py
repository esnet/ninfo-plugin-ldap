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
        second_pass_search = c.get('second_pass_search', '')
        strip       = c.get('strip', '')
        ignore_cert = 'ignore_cert' in c
        if ignore_cert:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)

        self.l = ldap.initialize(server)
        self.l.simple_bind_s(ldap_user, ldap_pw)
        self.dsn = dsn
        self.search = search
        self.second_pass_search = second_pass_search
        self.strip = strip

    def get_info(self, arg):
        search = self.search.replace("%s", arg)
        res = self.l.search_s(self.dsn, self.ldap.SCOPE_SUBTREE, search)
        if not res:
            return None

        if len(res) == 1 and res[0] and self.second_pass_search:
	        # We got exactly one result, and we wanted a two_pass query
	        cn = res[0][0]
	        second_pass_search = self.second_pass_search.replace("%s", cn)
	        second_pass_res = self.l.search_s(self.dsn, self.ldap.SCOPE_SUBTREE, second_pass_search)
	        if second_pass_res:
		        groups = [x[0] for x in second_pass_res]
		        res[0][1]['memberOf'] = groups

	if 'memberOf' in res[0][1]:
		res[0][1]['memberOf'].sort()
		
		        
	return {'records': res, 'strip': self.strip}
	

plugin_class = ldap_plugin
