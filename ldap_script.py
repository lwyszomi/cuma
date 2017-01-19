#! /usr/bin/python

import sys
import ldap
from ldap.controls import SimplePagedResultsControl
from distutils.version import StrictVersion

# Check if we're using the Python "ldap" 2.4 or greater API
LDAP24API = StrictVersion(ldap.__version__) >= StrictVersion('2.4')

# If you're talking to LDAP, you should be using LDAPS for security!
LDAPSERVER = 'ldaps://ldaps.rescue.org'
BASEDN = 'OU=All Users,DC=theirc,DC=org'
LDAPUSER = 'CN=OTIS,OU=Box Service Accounts,OU=Service Accounts,DC=theirc,DC=org'
LDAPPASSWORD = 'P@ssw0rd'
PAGESIZE = 1
ATTRLIST = ['uid', 'mail', 'cn', 'sn', 'givenName', 'shadowLastChange', 'shadowMax', 'shadowExpire']
SEARCHFILTER = '(&(objectClass=user)(mail=*))'


def create_controls(pagesize):
    """Create an LDAP control with a page size of "pagesize"."""
    # Initialize the LDAP controls for paging. Note that we pass ''
    # for the cookie because on first iteration, it starts out empty.
    if LDAP24API:
        return SimplePagedResultsControl(True, size=pagesize, cookie='')
    else:
        return SimplePagedResultsControl(ldap.LDAP_CONTROL_PAGE_OID, True,
                                         (pagesize, ''))


def get_pctrls(serverctrls):
    """Lookup an LDAP paged control object from the returned controls."""
    # Look through the returned controls and find the page controls.
    # This will also have our returned cookie which we need to make
    # the next search request.
    if LDAP24API:
        return [c for c in serverctrls
                if c.controlType == SimplePagedResultsControl.controlType]
    else:
        return [c for c in serverctrls
                if c.controlType == ldap.LDAP_CONTROL_PAGE_OID]


def set_cookie(lc_object, pctrls, pagesize):
    """Push latest cookie back into the page control."""
    if LDAP24API:
        cookie = pctrls[0].cookie
        lc_object.cookie = cookie
        return cookie
    else:
        est, cookie = pctrls[0].controlValue
        lc_object.controlValue = (pagesize, cookie)
        return cookie


# This is essentially a placeholder callback function. You would do your real
# work inside of this. Really this should be all abstracted into a generator...
def process_entry(_, attrs):
    """Process an entry. The two arguments passed are the DN and
       a dictionary of attributes."""
    print attrs


# Ignore server side certificate errors (assumes using LDAPS and
# self-signed cert). Not necessary if not LDAPS or it's signed by
# a real CA.
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
# Don't follow referrals
ldap.set_option(ldap.OPT_REFERRALS, 0)

l = ldap.initialize(LDAPSERVER)
l.protocol_version = 3  # Paged results only apply to LDAP v3
try:
    l.simple_bind_s(LDAPUSER, LDAPPASSWORD)
except ldap.LDAPError as e:
    exit('LDAP bind failed: %s' % e)

# Create the page control to work from
lc = create_controls(PAGESIZE)

# Do searches until we run out of "pages" to get from
# the LDAP server.
while True:
    # Send search request
    try:
        # If you leave out the ATTRLIST it'll return all attributes
        # which you have permissions to access. You may want to adjust
        # the scope level as well (perhaps "ldap.SCOPE_SUBTREE", but
        # it can reduce performance if you don't need it).
        msgid = l.search_ext(BASEDN, ldap.SCOPE_ONELEVEL, SEARCHFILTER,
                             ATTRLIST, serverctrls=[lc])
    except ldap.LDAPError as e:
        sys.exit('LDAP search failed: %s' % e)

    # Pull the results from the search request
    try:
        rtype, rdata, rmsgid, serverctrls = l.result3(msgid)
    except ldap.LDAPError as e:
        sys.exit('Could not pull LDAP results: %s' % e)

    # Each "rdata" is a tuple of the form (dn, attrs), where dn is
    # a string containing the DN (distinguished name) of the entry,
    # and attrs is a dictionary containing the attributes associated
    # with the entry. The keys of attrs are strings, and the associated
    # values are lists of strings.
    for dn, attrs in rdata:
        process_entry(dn, attrs)

    # Get cookie for next request
    pctrls = get_pctrls(serverctrls)
    if not pctrls:
        print >> sys.stderr, 'Warning: Server ignores RFC 2696 control.'
        break

    # Ok, we did find the page control, yank the cookie from it and
    # insert it into the control for our next search. If however there
    # is no cookie, we are done!
    cookie = set_cookie(lc, pctrls, PAGESIZE)
    print(type(cookie))
    if not cookie:
        break

# Clean up
l.unbind()

# Done!
sys.exit(0)
