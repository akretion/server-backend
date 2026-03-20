# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models
from odoo.exceptions import AccessError


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    def _get_updatable_models(self):
        return [
            "discuss.channel.member",
        ]

    @api.model
    def check(self, model, mode="read", raise_exception=True):
        if model in self._get_updatable_models() or mode == "read" or self.env.su:
            return super().check(model, mode=mode, raise_exception=raise_exception)
        # allow wizards
        model_obj = self.env[model]
        if model_obj._transient:
            return super().check(model, mode=mode, raise_exception=raise_exception)
        is_readonly = self.env.user.has_group("user_readonly_mode.group_user_readonly")
        if mode != "read" and is_readonly:
            if raise_exception:
                raise AccessError(
                    self.env._(
                        "You have the readonly mode activated, you can't update the "
                        "document {model}"
                    ).format(model=model)
                )
            return False
        return super().check(model, mode=mode, raise_exception=raise_exception)
