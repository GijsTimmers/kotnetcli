[1mdiff --git a/browser.py b/browser.py[m
[1mindex 8deb694..f424388 100644[m
[1m--- a/browser.py[m
[1m+++ b/browser.py[m
[36m@@ -234,6 +234,8 @@[m [mclass DummyBrowser():[m
         time.sleep(0.1)[m
 [m
     def login_parse_results(self):[m
[32m+[m[32m        logger.debug("rccode is %s", self.rccode)[m
[32m+[m[41m        [m
         if self.rccode == 100:[m
             return (self.download, self.upload)[m
 [m
[1mdiff --git a/kotnetcli.py b/kotnetcli.py[m
[1mindex 316974f..f8ea48c 100755[m
[1m--- a/kotnetcli.py[m
[1m+++ b/kotnetcli.py[m
[36m@@ -84,7 +84,7 @@[m [mclass KotnetCLI(object):[m
     ## jo: we don't use argparse's mutually exclusive groups here as it doesn't[m
     ## support grouping in the help messages[m
     [m
[31m-    def __init__(self, descr="Script om in- of uit te loggen op KotNet"):[m
[32m+[m[32m    def __init__(self, descr="Script om in- of uit te loggen op KotNet", log_level_default = "warning"):[m
         self.parser = argparse.ArgumentParser(descr)[m
         self.workergroep = self.parser.add_argument_group("worker options")#, \[m
         #"specify the login action")[m
[36m@@ -92,20 +92,20 @@[m [mclass KotnetCLI(object):[m
         #"manage your credentials")[m
         self.communicatorgroep = self.parser.add_argument_group("communicator options") #, \[m
         #"a pluggable visualisation system for everyones needs")[m
[31m-        self.voegArgumentenToe()[m
[32m+[m[32m        self.voegArgumentenToe(log_level_default)[m
         argcomplete.autocomplete(self.parser)[m
     [m
[31m-    def voegArgumentenToe(self):[m
[32m+[m[32m    def voegArgumentenToe(self, log_level_default):[m
         ########## general flags ##########[m
         self.parser.add_argument("-v", "--version", action="version", version=version)[m
         self.parser.add_argument("-l", "--license", action=PrintLicenceAction, \[m
         help="show license info and exit", nargs=0)[m
[31m-        ## debug flag with optional (nargs=?) level; defaults to warning if option [m
[32m+[m[32m        ## debug flag with optional (nargs=?) level; defaults to LOG_LEVEL_DEFAULT if option[m[41m [m
         ## not present; defaults to debug if option present but no level specified[m
         self.parser.add_argument("-d", "--debug", help="specify the debug verbosity", \[m
         nargs="?", const="debug", metavar="LEVEL",[m
         choices=[ 'critical', 'error', 'warning', 'info', 'debug' ],[m
[31m-        action="store", default="warning")[m
[32m+[m[32m        action="store", default=log_level_default)[m
         [m
         ########## login type flags ##########[m
         self.workergroep.add_argument("-i", "--login",\[m
[1mdiff --git a/kotnetcli_test.py b/kotnetcli_test.py[m
[1mindex 2676223..367a915 100755[m
[1m--- a/kotnetcli_test.py[m
[1m+++ b/kotnetcli_test.py[m
[36m@@ -23,38 +23,39 @@[m [mfrom kotnetcli import KotnetCLI[m
 from worker import DummyLoginWorker, DummyLogoutWorker[m
 from communicator.fabriek import LoginCommunicatorFabriek, LogoutCommunicatorFabriek    ## Voor output op maat[m
 from credentials import DummyCredentials     ## Opvragen van nummer en wachtwoord[m
[31m-import testsuite[m
[32m+[m[32mfrom testsuite import LoginTestsuiteWorker[m
 [m
 import logging[m
 logger = logging.getLogger(__name__)[m
 [m
[32m+[m
 ## An extended KotnetCLI to allow dummy behavior for testing purposes[m
 class KotnetCLITester(KotnetCLI):[m
 [m
     def __init__(self):[m
         super(KotnetCLITester, self).__init__("dummy script " + \[m
[31m-        "om in- of uit te loggen op KotNet")[m
[31m-[m
[31m-    def voegArgumentenToe(self):[m
[31m-        super(KotnetCLITester, self).voegArgumentenToe()[m
[32m+[m[32m        "om in- of uit te loggen op KotNet", log_level_default="info")[m
[32m+[m[41m        [m
[32m+[m[32m    def voegArgumentenToe(self, log_level_default):[m
[32m+[m[32m        super(KotnetCLITester, self).voegArgumentenToe(log_level_default)[m
         [m
         self.parser.add_argument("-r", "--run-tests", \[m
[31m-        help="Run a bunch of tests and assertions", action=testsuite.RunTestsAction, nargs=0)[m
[32m+[m[32m        help="Run a bunch of tests and assertions", action="store_true")[m
     [m
     ## override with dummy behavior[m
     def parseActionFlags(self, argumenten):[m
         if argumenten.logout:[m
             logger.info("ik wil uitloggen voor spek en bonen")[m
[31m-            worker = DummyLogoutWorker()[m
[31m-            fabriek = LogoutCommunicatorFabriek()[m
[32m+[m[32m            return (DummyLogoutWorker(), LogoutCommunicatorFabriek())[m
[32m+[m[41m        [m
[32m+[m[32m        elif argumenten.run_tests:[m
[32m+[m[32m            logger.info("ik wil testen")[m
[32m+[m[32m            return (LoginTestsuiteWorker(), LoginCommunicatorFabriek())[m
             [m
         else:[m
             ## default option: argumenten.login[m
             logger.info("ik wil inloggen voor spek en bonen")[m
[31m-            worker = DummyLoginWorker()[m
[31m-            fabriek = LoginCommunicatorFabriek()[m
[31m-            [m
[31m-        return (worker, fabriek)[m
[32m+[m[32m            return (DummyLoginWorker(), LoginCommunicatorFabriek())[m
         [m
     def parseCredentialFlags(self, argumenten):[m
         logger.info("ik wil credentials ophalen voor spek en bonen")[m
[1mdiff --git a/testsuite.py b/testsuite.py[m
[1mindex 3563e86..807b0ba 100644[m
[1m--- a/testsuite.py[m
[1m+++ b/testsuite.py[m
[36m@@ -15,44 +15,24 @@[m
 ## send a letter to Creative Commons, PO Box 1866, Mountain View, [m
 ## CA 94042, USA.[m
 [m
[31m-import argparse[m
[31m-from worker import DummyLoginWorker, DummyLogoutWorker, EXIT_SUCCESS, EXIT_FAILURE[m
[31m-from communicator.fabriek import LoginCommunicatorFabriek, LogoutCommunicatorFabriek    ## Voor output op maat[m
[31m-from credentials import DummyCredentials     ## Opvragen van nummer en wachtwoord[m
[31m-[m
[31m-import sys[m
[32m+[m[32mfrom worker import DummyLoginWorker, DummyLogoutWorker, SuperWorker, EXIT_SUCCESS, EXIT_FAILURE[m
 [m
 from tools import log[m
 import logging[m
 logger = logging.getLogger(__name__)[m
 [m
[31m-## TODO assert for the correct fine grained exit code here (see corresponding issue)[m
[31m-class RunTestsAction(argparse.Action):[m
[31m-    def __call__(self, parser, namespace, values, option_string=None):[m
[31m-        log.init_logging("info")[m
[31m-        creds = DummyCredentials()[m
[31m-        fab = LoginCommunicatorFabriek()[m
[31m-        [m
[31m-        self.test_lazy_import(fab)[m
[31m-        co = fab.createColoramaCommunicator()   ## change this line to test another communicator[m
[32m+[m[32mclass LoginTestsuiteWorker(SuperWorker):[m
[32m+[m
[32m+[m[32m    def go(self, co, creds):[m
[32m+[m[32m        logger.info("running dummy login testsuite with communicator " + \[m
[32m+[m[32m        "'%s'\n", co.__class__.__name__)[m
         self.run_dummy_login_tests(co, creds)[m
[31m-        [m
[32m+[m[32m        logger.info("end of dummy login testsuite with communicator " + \[m
[32m+[m[32m        "'%s'", co.__class__.__name__)[m
         exit(0)[m
     [m
[31m-    def test_lazy_import(self, fab):[m
[31m-        logger.info("testing lazy importing of communicators...")[m
[31m-[m
[31m-        assert not ("colorama" in sys.modules.keys())[m
[31m-        fab.createPlaintextCommunicator()[m
[31m-        assert not ("colorama" in sys.modules.keys())[m
[31m-        fab.createColoramaCommunicator()[m
[31m-        assert "colorama" in sys.modules.keys()[m
[31m-[m
[31m-        logger.info("lazy importing of communicators seems OK")[m
[31m-    [m
[32m+[m[32m    ## TODO assert for the correct fine grained exit code here (see corresponding issue)[m
     def run_dummy_login_tests(self, co, creds):[m
[31m-        logger.info("running dummy login testsuite with communicator " + \[m
[31m-        "'%s'\n", co.__class__.__name__)[m
     [m
         logger.info("DEFAULT DUMMY LOGIN START")[m
         worker = DummyLoginWorker()[m
[36m@@ -128,7 +108,4 @@[m [mclass RunTestsAction(argparse.Action):[m
             assert (e.code == EXIT_FAILURE)[m
             logger.info("UNKNOWN RC (DEBUG OFF) DUMMY LOGIN END\n")[m
         [m
[31m-        logger.info("end of dummy login testsuite with communicator " + \[m
[31m-        "'%s'", co.__class__.__name__)[m
[31m-[m
[31m-## end class RunTestsAction[m
[32m+[m[32m## end class LoginTestsuiteWorker[m
[1mdiff --git a/worker.py b/worker.py[m
[1mindex ada31f8..df6557b 100644[m
[1m--- a/worker.py[m
[1m+++ b/worker.py[m
[36m@@ -53,6 +53,7 @@[m [mclass SuperWorker(object):[m
 class LoginWorker(SuperWorker):[m
     def go(self, co, creds):[m
         logger.debug("enter LoginWorker.go()")[m
[32m+[m[41m        [m
         self.check_kotnet(co)[m
         self.netlogin(co)[m
         #self.kies_kuleuven(co)[m
[36m@@ -60,6 +61,10 @@[m [mclass LoginWorker(SuperWorker):[m
         self.login_gegevensopsturen(co)[m
         self.login_resultaten(co)[m
         [m
[32m+[m[32m        co.beeindig_sessie()[m
[32m+[m[32m        logger.debug("LoginWorker: exiting with success")[m
[32m+[m[32m        sys.exit(EXIT_SUCCESS)[m[41m        [m
[32m+[m[41m        [m
     def netlogin(self, co):[m
         co.eventNetloginStart()[m
         try:[m
[36m@@ -104,9 +109,6 @@[m [mclass LoginWorker(SuperWorker):[m
         try:[m
             tup = self.browser.login_parse_results()[m
             co.eventLoginGeslaagd(tup[0], tup[1])[m
[31m-            co.beeindig_sessie()[m
[31m-            logger.debug("LoginWorker: exiting with success")[m
[31m-            sys.exit(EXIT_SUCCESS)[m
         except browser.WrongCredentialsException:[m
             co.beeindig_sessie(EXIT_FAILURE)[m
             logger.error("Uw logingegevens kloppen niet. Gebruik kotnetcli " + \[m
