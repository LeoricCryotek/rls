# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models
from . import actions
from . import controllers


def _schedule_cron():
    models.UpdateDaysRemaining()._schedule_cron()

def post_init_hook(cr, registry):
    _schedule_cron()

