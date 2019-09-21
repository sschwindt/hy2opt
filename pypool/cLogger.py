#!/usr/bin/python
try:
    import os, sys, logging
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, logging).")


class Logger:
    def __init__(self, *args):
        # args[0] = BOOL that states if an existing logfile should be deleted or not. Default is TRUE
        self.mdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.logging_start()

    def logging_start(self):
        # args[0] = BOOL that states if an existing logfile should be deleted or not. Default is TRUE

        logfilenames = ["errors.log", "logfile.log"]
        for fn in logfilenames:
            fn_full = os.path.join(self.mdir, fn)
            if os.path.isfile(fn_full):
                try:
                    os.remove(fn_full)
                except:
                    pass
        # start INFO logging
        self.logger = logging.getLogger("logfile")
        self.logger.setLevel(logging.DEBUG)
        info_formatter = logging.Formatter("%(asctime)s - %(message)s")
        # start ERROR logging
        self.elogger = logging.getLogger("errors")
        self.elogger.setLevel(logging.ERROR)

        # create console handler and set level to info
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(info_formatter)
        self.logger.addHandler(console_handler)
        self.elogger.addHandler(console_handler)
        # create error file handler and set level to error
        err_handler = logging.FileHandler(os.path.join(self.mdir, logfilenames[0]), "w", encoding=None, delay="true")
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(info_formatter)
        self.logger.addHandler(err_handler)
        self.elogger.addHandler(err_handler)
        # create debug file handler and set level to debug
        debug_handler = logging.FileHandler(os.path.join(self.mdir, logfilenames[1]), "w")
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(info_formatter)
        self.logger.addHandler(debug_handler)
        self.elogger.addHandler(debug_handler)

    def logging_stop(self):
        # stop logging and release logfile
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
        for handler in self.elogger.handlers:
            handler.close()
            self.elogger.removeHandler(handler)

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = Logger (%s)" % os.path.dirname(__file__))
        print(dir(self))
