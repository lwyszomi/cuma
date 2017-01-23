import ldap


class LDAPClient(object):
    def __init__(self, server, base_dn, user, password):
        self.server = server
        self.base_dn = base_dn
        self.user = user
        self.password = password

    def run_query(self, search_filter, attr_list):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        ldap.set_option(ldap.OPT_REFERRALS, 0)

        l = ldap.initialize(self.server)
        l.protocol_version = 3  # Paged results only apply to LDAP v3
        l.simple_bind_s(self.user, self.password)

        msgid = l.search_ext(self.base_dn, ldap.SCOPE_ONELEVEL, search_filter, attr_list)

        results = []
        data = l.result3(msgid)[1]
        for _, attrs in data:
            for key in attrs:
                attrs[key] = attrs[key][0]
            results.append(attrs)
        l.unbind()
        return results
