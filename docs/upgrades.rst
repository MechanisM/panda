====================
Upgrading your PANDA
====================

Before you get started
======================

Although we strive to make upgrades as simple as possible, upgrading your PANDA will require that you know how to SSH into your server. If you need help with this see our guide to :doc:`Connecting with SSH <ssh>`. And don't be afraid to ask for help on the `PANDA Users Group <https://groups.google.com/forum/?fromgroups#!forum/panda-project-users>`_.

.. warning::

    Your PANDA will be unavailable while upgrading. Typically this will not last more than five minutes, but it will vary by release. You should plan to perform PANDA upgrades during off hours.

The following release are in **reverse** version order. They **must** be performed in sequence (from lowest version number to highest version number--reverse order on this page).

0.2.0 to 1.0.0
==============

To upgrade your PANDA from the 0.2.0 release to the 1.0.0 release, :doc:`SSH <ssh>` into your server and execute the following commands::

    wget https://raw.github.com/pandaproject/panda/1.0.0/scripts/migrations/0.2.0-to-1.0.0.sh
    sudo bash 0.2.0-to-1.0.0.sh

Your PANDA will be stopped, the upgrade will be applied and it will then be restarted. A log of this process will be put in ``/var/log/panda-upgrade-1.0.0.log``.

.. note::

    This upgrade will automatically upgrade your server's Ubuntu distrubution to version 12.04. This long-release version of Ubuntu will be supported by Canonical (the company behind Ubuntu) for five years. If you have made any customizations to your PANDA's server environment be away that this upgrade could have unintended consequences.

Check out the :ref:`changelog` to see all the new features and bug fixes in this release!

0.1.4 to 0.2.0
==============

To upgrade your PANDA from the 0.1.4 release to the 0.2.0 release, :doc:`SSH <ssh>` into your server and execute the following commands::

    wget https://raw.github.com/pandaproject/panda/0.2.0/scripts/migrations/0.1.4-to-0.2.0.sh
    sudo bash 0.1.4-to-0.2.0.sh

Your PANDA will be stopped, the upgrade will be applied and it will then be restarted. A log of this process will be put in ``/var/log/panda-upgrade-0.2.0.log``.

.. note::

    As part of this upgrade all existing activation keys will be voided. New activation keys can be generated via the admin.

Check out the :ref:`changelog` to see all the new features and bug fixes in this release!

0.1.3 to 0.1.4
==============

To upgrade your PANDA from the 0.1.3 release to the 0.1.4 release, :doc:`SSH <ssh>` into your server and execute the following commands::

    wget https://raw.github.com/pandaproject/panda/0.1.4/scripts/migrations/0.1.3-to-0.1.4.sh
    sudo bash 0.1.3-to-0.1.4.sh

Your PANDA will be stopped, the upgrade will be applied and it will then be restarted. A log of this process will be put in ``/var/log/panda-upgrade-0.1.4.log``.

.. note::

    This version adds an option to explicitly enable or disable sending email. If you've previously configured email you will need to visit the settings page for your PANDA (http://MY-PANDA/admin/settings) and check the "Enable email?" checkbox.

Check out the :ref:`changelog` to see all the new features and bug fixes in this release!

0.1.2 to 0.1.3
==============

To upgrade your PANDA from the 0.1.2 release to the 0.1.3 release, :doc:`SSH <ssh>` into your server and execute the following commands::

    wget https://raw.github.com/pandaproject/panda/0.1.3/scripts/migrations/0.1.2-to-0.1.3.sh
    sudo bash 0.1.2-to-0.1.3.sh

Your PANDA will be stopped, the upgrade will be applied and it will then be restarted. A log of this process will be put in ``/var/log/panda-upgrade-0.1.3.log``. 

Check out the :ref:`changelog` to see all the new features and bug fixes in this release!

0.1.1 to 0.1.2
==============

To upgrade your PANDA from the 0.1.1 release to the 0.1.2 release, :doc:`SSH <ssh>` into your server and execute the following commands::

    wget https://raw.github.com/pandaproject/panda/0.1.2/scripts/migrations/0.1.1-to-0.1.2.sh
    sudo bash 0.1.1-to-0.1.2.sh

Your PANDA will be stopped, the upgrade will be applied and it will then be restarted. A log of this process will be put in ``/var/log/panda-upgrade.log``. 

Check out the :ref:`changelog` to see all the new features and bug fixes in this release!

0.1.0 to 0.1.1
==============

To upgrade your PANDA from the first beta release to the 0.1.1 release, :doc:`SSH <ssh>` into your server and execute the following commands::

    wget https://raw.github.com/pandaproject/panda/0.1.1/scripts/migrations/0.1.0-to-0.1.1.sh
    sudo bash 0.1.0-to-0.1.1.sh

Your PANDA will be stopped, the upgrade will be applied and it will then be restarted. A log of this process will be put in ``/var/log/panda-upgrade.log``. 

Check out the :ref:`changelog` to see all the new features and bug fixes in this release!

