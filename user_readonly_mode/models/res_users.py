# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    def _get_forbidden_readonly_groups(self):
        return [
            "base.group_system",
            "base.group_erp_manager",
        ]

    @api.constrains("groups_id")
    def _check_readonly_incompatibility(self):
        group_readonly = self.env.ref(
            "user_readonly_mode.group_user_readonly", raise_if_not_found=False
        )
        if not group_readonly:
            return

        forbidden_groups = self._get_forbidden_readonly_groups()

        for user in self:
            if group_readonly in user.groups_id:
                if user.id == self.env.uid:
                    raise ValidationError(
                        self.env._(
                            "You can't activate the readonly mode for your own user"
                        )
                    )

                for xml_id in forbidden_groups:
                    forbidden_group = self.env.ref(xml_id, raise_if_not_found=False)
                    if forbidden_group and forbidden_group in user.groups_id:
                        raise ValidationError(
                            self.env._(
                                "The user '{user_name}' can't have the readonly mode "
                                "and the group '{group_name}'."
                            ).format(
                                user_name=user.name, group_name=forbidden_group.name
                            )
                        )
