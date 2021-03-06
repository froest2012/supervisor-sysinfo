import subprocess, psutil, json, math, os, statvfs

from supervisor.supervisord import SupervisorStates
from supervisor.xmlrpc import Faults
from supervisor.xmlrpc import RPCError


from sys_info import ps, sys_info

API_VERSION = '0.1'

class SysInfoNamespaceRPCInterface:
    """ A Supervisor RPC interface that provides the ability 
    to cache abritrary data in the Supervisor instance as key/value pairs.
    """

    def __init__(self, supervisord):
        self.supervisord = supervisord

    def _update(self, text):
        self.update_text = text # for unit tests, mainly

        state = self.supervisord.get_state()

        if state == SupervisorStates.SHUTDOWN:
            raise RPCError(Faults.SHUTDOWN_STATE)

        
    # RPC API methods

    def getAPIVersion(self):
        """ Return the version of the RPC API used by supervisor_cache

        @return string  version
        """
        self._update('getAPIVersion')
        return API_VERSION

    def ps(self):
        """ Return keys for all data stored in the cache

        @return  json repr of a dict of process details keyed by pid.

        >>> rpc_proxy.sysinfo.ps()
           {
            u'30194': {u'command': u'/Users/thanos/supervisor-sysinfo/bin/python /Users/thanos/supervisor-sysinfo/bin/supervisord -c supervisor.conf',
                        u'cpu': u'0.0',
                        u'mem': u'0.1',
                        u'rss': u'5908',
                        u'started': u'5:21PM',
                        u'stat': u'Ss',
                        u'time': u'0:00.08',
                        u'tt': u'??',
                        u'user': u'thanos',
                        u'vsz': u'2448924'},
             u'30283': {u'command': u'python supervisor_sysinfo/test.py',
                        u'cpu': u'11.2',
                        u'mem': u'0.3',
                        u'rss': u'11008',
                        u'started': u'5:27PM',
                        u'stat': u'S+',
                        u'time': u'0:00.10',
                        u'tt': u's009',
                        u'user': u'thanos',
                        u'vsz': u'2444692'},
             u'30284': {u'command': u'ps aux',
                        u'cpu': u'0.0',
                        u'mem': u'0.0',
                        u'rss': u'620',
                        u'started': u'5:27PM',
                        u'stat': u'R',
                        u'time': u'0:00.00',
                        u'tt': u'??',
                        u'user': u'root',
                        u'vsz': u'2434820'},
             u'985': {u'command': u'/Applications/Utilities/Console.app/Contents/MacOS/Console -psn_0_381021',
                      u'cpu': u'0.0',
                      u'mem': u'0.4',
                      u'rss': u'15532',
                      u'started': u'Wed02PM',
                      u'stat': u'S',
                      u'time': u'11:25.89',
                      u'tt': u'??',
                      u'user': u'thanos',
                      u'vsz': u'2745052'}}
        """
        self._update('ps')
        return json.dumps(ps())






    def sysInfo(self):
        """
        @return  json string repr of dict.
        version XML-RPC unfortunately doesn't support 64-bit ints in the official standard so returns a json string.

        >>> rpc_proxy.sysinfo.sysInfo()

        {u'cpu_percent': 3.0,
         u'cpu_times': {u'idle': 4105971.75,
                        u'nice': 0.0,
                        u'system': 55322.1,
                        u'user': 92921.92},
         u'disk_partitions': [{u'disk_usage': {u'free': 309265399808.0,
                                               u'percent': 69.0,
                                               u'total': 999345127424.0,
                                               u'used': 689817583616.0
                                               u'ipercent': 7.0, 
                                               u'ifree': 491028, 
                                               u'inodes': 524288},
                               u'partition_info': {u'device': u'/dev/disk0s2',
                                                   u'mountpoint': u'/'}}],
         u'phymem_usage': {u'free': 44892160,
                           u'percent': 73.5,
                           u'total': 4294967296,
                           u'used': 4240707584}}
        """
        return json.dumps(sys_info())

def make_sysinfo_rpcinterface(supervisord, **config):
    return SysInfoNamespaceRPCInterface(supervisord)
