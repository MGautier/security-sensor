for threads in threading.enumerate():

    test = Iptables(
        args=(1,),
        source={'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                'C': './secapp/kernel/conf/iptables-conf.conf'}
    )
    if type(threads) == type(test):
        exist_thread = True

if not exist_thread:
    thread_iptables = Iptables(
        args=(1,),
        source={'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                'C': './secapp/kernel/conf/iptables-conf.conf'}
    )
    thread_iptables.start()
