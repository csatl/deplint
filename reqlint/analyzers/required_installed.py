from reqlint.model.advice import Advice
from reqlint.model.advice_list import AdviceList


class RequiredInstalledAnalyzer(object):
    '''
    Reports packages that are required and installed.
    '''

    def __init__(self, requirements_txt, installed_packages):
        self.requirements_txt = requirements_txt
        self.installed_packages = installed_packages

    def analyze(self):
        pkgs_required = self.requirements_txt.packages
        advice_list = []

        for pkg_req in pkgs_required:
            pkg_installed = self.installed_packages.get_by_name(pkg_req.name)
            if pkg_installed:
                advice = Advice(
                    analyzer=self,
                    severity='info',
                    message="Dependency '%s' is satisfied by '%s'" % (
                        pkg_req.as_display_name(),
                        pkg_installed.as_display_name(),
                    ),
                )
                advice_list.append(advice)

        return AdviceList(advice_list=advice_list)
