obj = Pygtail("/var/log/iptables.log")

while True:
    try:
        for line in obj:
            if len(line) > 1:
                self.process_line(line)
    except Exception as ex:
        print "Pygtail processing -> ", ex
