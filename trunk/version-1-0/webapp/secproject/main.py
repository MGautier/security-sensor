import signal
import os
import manager

if __name__ == "__main__":

    manager_obj = manager.Manager()
    iptables = manager_obj.create_controller('iptables')
    print "IPTABLES - GET PARENT PID: ", iptables.get_parent_pid()
    print "IPTABLES - GET CHILD PID: ", iptables.get_child_pid()
    print "IPTABLES - GET SOURCE: ", iptables.get_source()
    print "IPTABLES - GET CONFIGURATION: ", iptables.get_configuration()
    print "IPTABLES - GET TYPE: ", iptables.get_type_source()
    print "IPTABLES - GET MODEL: ", iptables.get_model_source()
    print "IPTABLES - GET LOG: ", iptables.get_log_processing()

    set_threads = [ iptables.get_child_pid(), iptables.get_parent_pid()  ]

    while True:

        data_input = raw_input(' ')
        print "SET-THREADS: ", set_threads

        if data_input == 'exit':
            for pid in set_threads:
                # Primero matamas al proceso hijo y luego al padre
                # para que el hijo no entre en inanicion
                print "Matando al proceso: ", pid
                os.kill(pid,signal.SIGKILL)
            os._exit(0)
        elif data_input in set_threads:
            print "Matando al proceso: ", data_input
            os.kill(data_input, signal.SIGKILL)
