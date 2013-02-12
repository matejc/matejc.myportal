# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from matejc.myportal.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of matejc.myportal into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if matejc.myportal is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('matejc.myportal'))

    def test_uninstall(self):
        """Test if matejc.myportal is cleanly uninstalled."""
        self.installer.uninstallProducts(['matejc.myportal'])
        self.assertFalse(self.installer.isProductInstalled('matejc.myportal'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IMatejcMyportalLayer is registered."""
        from matejc.myportal.interfaces import IMatejcMyportalLayer
        from plone.browserlayer import utils
        self.failUnless(IMatejcMyportalLayer in utils.registered_layers())
