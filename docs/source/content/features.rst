Features
=============

If you haven't, create a superuser with the `Django createsuperuser command <https://docs.djangoproject.com/en/3.0/intro/tutorial02/#creating-an-admin-user>`_. Login with the admin user, and select ``Drips`` to manage them. You will be able to:

- View created drips.
- Create a new drip.
- Select and delete drips.

Create Drip
-----------
Click on the ``ADD DRIP +`` button to create a new Drip. In the creation you need to define the email that you want to send, and the queryset for the users that will receive it. To see more details, :ref:`click here <create-drip>`.

View timeline of a Drip
-----------------------

In the django admin, you can select a drip and then click on the ``VIEW TIMELINE`` button to view the emails expected to be sent with the corresponding receivers:

.. image:: ../../images/view_timeline.png
  :width: 400
  :alt: View timeline

Message class
-------------

By default, Django Drip creates and sends messages that are instances of Django’s ``EmailMultiAlternatives`` class.
If you want to customize in any way the message that is created and sent, you can do that by creating a subclass of ``EmailMessage`` and overriding any method that you want to behave differently.
For example:

.. code-block:: python

    from django.core.mail import EmailMessage
    from drip.drips import DripMessage

    class PlainDripEmail(DripMessage):

        @property
        def message(self):
            if not self._message:
                email = EmailMessage(self.subject, self.plain, self.from_email, [self.user.email])
                self._message = email
            return self._message

In that example, ``PlainDripEmail`` overrides the message property of the base ``DripMessage`` class to create a simple
``EmailMessage`` instance instead of an ``EmailMultiAlternatives`` instance.

In order to be able to specify that your custom message class should be used for a drip, you need to configure it in the ``DRIP_MESSAGE_CLASSES`` setting:

.. code-block:: python

    DRIP_MESSAGE_CLASSES = {
        'plain': 'myproj.email.PlainDripEmail',
    }

This will allow you to choose in the admin, for each drip, whether the ``default`` (``DripMessage``) or ``plain`` message class should be used for generating and sending the messages to users.

Send Drips
----------

To send the created and enabled Drips, run the command:

.. code-block:: python

    python manage.py send_drips

You can use cron to schedule the drips.


The Cron Scheduler
------------------

You may want to have an easy way to send drips periodically. It's possible to set a couple of parameters in your settings to do that.
First activate the scheduler by adding the ``DRIP_SCHEDULE_SETTINGS`` dictionary:

.. code-block:: python

    # your settings file
    DRIP_SCHEDULE_SETTINGS = {
        'DRIP_SCHEDULE': True,
    }

After that, choose:

- A day of the week: An integer value between ``0-6``, or a string: ``'mon'``, ``'tue'``, ``'wed'``, ``'thu'``, ``'fri'``, ``'sat'``, ``'sun'``. The name in the settings is ``DRIP_SCHEDULE_DAY_OF_WEEK`` (default is set to ``0``).
- An hour: An integer value between ``0-23``. The name in the settings is ``DRIP_SCHEDULE_HOUR`` (default is set to ``0``).
- A minute: An integer value between ``0-59``. The name in the settings is ``DRIP_SCHEDULE_MINUTE`` (default is set to ``0``).

With those values, a cron scheduler will execute the `send_drips` command every week in the specified day/hour/minute. The scheduler will use the timezone of your ``TIME_ZONE`` parameter in your settings (default is set to ``'UTC'``). For example, if you have:

.. code-block:: python

    DRIP_SCHEDULE_SETTINGS = {
        'DRIP_SCHEDULE': True,
        'DRIP_SCHEDULE_DAY_OF_WEEK': 'mon',
        'DRIP_SCHEDULE_HOUR': 13,
        'DRIP_SCHEDULE_MINUTE': 57,
    }

Then every Monday at 13:57 the ``send_drips`` command will be executed.  
Last but not least, add this line at the end of your main ``urls.py`` file to start the scheduler:

.. code-block:: python

    # your main urls.py file
    ...
    from drip.scheduler.cron_scheduler import cron_send_drips

    ...
    cron_send_drips()

We recommend you to do it there because we know for sure that it's a file that is executed once at the beginning.

Some tips:

- If you want to run the command every day in the week, hour, or minute, just set the corresponding parameter to ``'*'``.
- If you want to run the command more than a day in the week, just set the ``DRIP_SCHEDULE_DAY_OF_WEEK`` to more than one value. For example, if you set that to ``'mon-fri'`` the command will be executed from Monday to Friday.
