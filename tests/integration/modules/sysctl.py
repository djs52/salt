# Import python libs
import sys

# Import salt libs
import integration
from saltunittest import skipIf


class SysctlModuleTest(integration.ModuleCase):
    def setUp(self):
        super(SysctlModuleTest, self).setUp()
        ret = self.run_function('cmd.has_exec', ['sysctl'])
        if not ret:
            self.skipTest('sysctl not found')

    def test_show(self):
        ret = self.run_function('sysctl.show')
        self.assertIsInstance(ret, dict, 'sysctl.show return wrong type')
        self.assertGreater(len(ret), 10, 'sysctl.show return few data')

    @skipIf(not sys.platform.startswith('linux'), 'Linux specific')
    def test_show_linux(self):
        ret = self.run_function('sysctl.show')
        self.assertIn('kernel.ostype', ret, 'kernel.ostype absent')

    @skipIf(not sys.platform.startswith('freebsd'), 'FreeBSD specific')
    def test_show_freebsd(self):
        ret = self.run_function('sysctl.show')
        self.assertIn('vm.vmtotal', ret, 'Multiline variable absent')
        self.assertGreater(ret.get('vm.vmtotal').splitlines(),
                           1,
                           'Multiline value was parsed wrong')


if __name__ == '__main__':
    from integration import run_tests
    run_tests(SysctlModuleTest)