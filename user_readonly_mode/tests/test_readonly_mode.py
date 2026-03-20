# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase


class TestUserReadonlyMode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 1. Création d'un utilisateur de test standard
        cls.test_user = cls.env["res.users"].create(
            {
                "name": "Test Readonly User",
                "login": "test_readonly",
                "groups_id": [(6, 0, [cls.env.ref("base.group_user").id])],
            }
        )
        cls.group_readonly = cls.env.ref("user_readonly_mode.group_user_readonly")

    def test_01_readonly_restriction(self):
        self.test_user.write({"groups_id": [(4, self.group_readonly.id)]})
        # On tente de créer un partenaire avec cet utilisateur
        with self.assertRaises(AccessError):
            self.env["res.partner"].with_user(self.test_user).create(
                {"name": "should fail"}
            )
            self.test_user.partner_id.with_user(self.test_user).write(
                {"street": "should fail"}
            )

    def test_02_incompatibility_constraint(self):
        group_admin = self.env.ref("base.group_system")
        with self.assertRaises(ValidationError):
            self.test_user.write(
                {"groups_id": [(4, self.group_readonly.id), (4, group_admin.id)]}
            )
